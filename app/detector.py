"""
app/detector.py — YOLOv8 Object Detection module with letterbox preprocessing & NMS postprocessing.
"""

from __future__ import annotations
import logging
from dataclasses import dataclass
import numpy as np
import cv2

from app.config import (
    DETECTOR_MODEL_NAME,
    DETECTOR_INPUT_SIZE,
    DETECTOR_CONF_THRESHOLD,
    DETECTOR_NMS_IOU_THRESHOLD,
    DETECTOR_MAX_LABELS,
    COCO_CLASSES,
)
from app.engine import NPUModel

log = logging.getLogger("netra.detector")


@dataclass
class DetectedObject:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]  # (x1, y1, x2, y2) in original frame pixels


class ObjectDetector:
    """YOLOv8-N ONNX object detector."""

    def __init__(self, model_filename: str = DETECTOR_MODEL_NAME):
        self.model = NPUModel(model_filename)

    def detect(self, frame: np.ndarray) -> tuple[list[str], list[DetectedObject], float, str]:
        """
        Runs object detection on a camera frame.
        Returns:
            - labels: List of unique detected object class names.
            - objects: List of DetectedObject instances (including bounding boxes).
            - latency_ms: Inference execution time in milliseconds.
            - provider: Name of ORT provider used.
        """
        model_input, scale, pad_x, pad_y = self._preprocess(frame)
        result = self.model.run(model_input)
        labels, objects = self._postprocess(result.outputs[0], frame.shape, scale, pad_x, pad_y)
        return labels, objects, result.latency_ms, result.provider_used

    def _preprocess(self, frame: np.ndarray) -> tuple[np.ndarray, float, int, int]:
        h, w = frame.shape[:2]
        scale = DETECTOR_INPUT_SIZE / max(h, w)
        new_h, new_w = int(round(h * scale)), int(round(w * scale))
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        canvas = np.full((DETECTOR_INPUT_SIZE, DETECTOR_INPUT_SIZE, 3), 114, dtype=np.uint8)
        pad_x, pad_y = (DETECTOR_INPUT_SIZE - new_w) // 2, (DETECTOR_INPUT_SIZE - new_h) // 2
        canvas[pad_y:pad_y + new_h, pad_x:pad_x + new_w] = resized

        rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        chw = np.transpose(rgb, (2, 0, 1))
        tensor = np.expand_dims(chw, axis=0)
        return tensor, scale, pad_x, pad_y

    def _postprocess(
        self, raw_output: np.ndarray, orig_shape: tuple, scale: float, pad_x: int, pad_y: int
    ) -> tuple[list[str], list[DetectedObject]]:
        predictions = np.squeeze(raw_output, axis=0).T  # shape: (8400, 84)

        boxes_xywh = predictions[:, :4]
        class_scores = predictions[:, 4:]
        class_ids = np.argmax(class_scores, axis=1)
        confidences = class_scores[np.arange(len(class_scores)), class_ids]

        keep = confidences > DETECTOR_CONF_THRESHOLD
        boxes_xywh = boxes_xywh[keep]
        class_ids = class_ids[keep]
        confidences = confidences[keep]

        if len(boxes_xywh) == 0:
            return [], []

        # Convert (cx, cy, w, h) -> (x, y, w, h) top-left for NMS
        boxes_tl = boxes_xywh.copy()
        boxes_tl[:, 0] -= boxes_xywh[:, 2] / 2
        boxes_tl[:, 1] -= boxes_xywh[:, 3] / 2

        indices = cv2.dnn.NMSBoxes(
            boxes_tl.tolist(), confidences.tolist(),
            DETECTOR_CONF_THRESHOLD, DETECTOR_NMS_IOU_THRESHOLD,
        )
        indices = np.array(indices).flatten() if len(indices) else []

        ranked = sorted(indices, key=lambda i: -confidences[i])
        orig_h, orig_w = orig_shape[:2]

        seen_labels = set()
        labels = []
        objects = []

        for i in ranked:
            c_id = class_ids[i]
            conf = float(confidences[i])
            label_name = COCO_CLASSES[c_id] if c_id < len(COCO_CLASSES) else f"object_{c_id}"

            # Un-pad and un-scale bounding box to original image coordinates
            cx, cy, bw, bh = boxes_xywh[i]
            x1 = int(round((cx - bw / 2 - pad_x) / scale))
            y1 = int(round((cy - bh / 2 - pad_y) / scale))
            x2 = int(round((cx + bw / 2 - pad_x) / scale))
            y2 = int(round((cy + bh / 2 - pad_y) / scale))

            # Clamp coordinates
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(orig_w, x2), min(orig_h, y2)

            objects.append(DetectedObject(label=label_name, confidence=conf, bbox=(x1, y1, x2, y2)))

            if label_name not in seen_labels:
                seen_labels.add(label_name)
                labels.append(label_name)
            if len(labels) >= DETECTOR_MAX_LABELS:
                break

        return labels, objects
