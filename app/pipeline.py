"""
app/pipeline.py — Authoritative Netra Production Pipeline.
Orchestrates Camera -> Detection -> OCR -> Local Response Composition -> TTS.
"""

from __future__ import annotations
import logging
import numpy as np

from app.detector import ObjectDetector, DetectedObject
from app.ocr import OCRReader
from app.response_composer import LocalResponseComposer
from app.tts import TTSEngine

log = logging.getLogger("netra.pipeline")


class NetraPipeline:
    """Production Netra pipeline linking all local vision, OCR, composition, and speech components."""

    def __init__(self):
        self._detector: ObjectDetector | None = None
        self._ocr: OCRReader | None = None
        self._composer = LocalResponseComposer()
        self._tts: TTSEngine | None = None

    def detector(self) -> ObjectDetector:
        if self._detector is None:
            self._detector = ObjectDetector()
        return self._detector

    def ocr(self) -> OCRReader:
        if self._ocr is None:
            self._ocr = OCRReader()
        return self._ocr

    def tts(self) -> TTSEngine:
        if self._tts is None:
            self._tts = TTSEngine()
        return self._tts

    def run_turn(
        self, frame: np.ndarray, user_question: str | None = None
    ) -> tuple[list[str], list[DetectedObject], str, str, dict]:
        """
        Executes a single "look and speak" turn.
        Returns:
            - labels: List of unique detected object labels.
            - objects: List of DetectedObject instances (including bounding box coordinates).
            - ocr_text: Text extracted from frame.
            - answer_text: Composed natural-language response.
            - metrics: Execution latency & provider metrics dictionary.
        """
        metrics = {}

        # Stage 1: Object Detection
        try:
            labels, objects, det_latency, provider = self.detector().detect(frame)
            metrics["det_latency_ms"] = det_latency
            metrics["provider"] = provider
        except Exception as e:
            log.error(f"Detector error in pipeline turn: {e}")
            labels, objects, det_latency, provider = [], [], 0.0, "CPUExecutionProvider"
            metrics["det_error"] = str(e)

        # Stage 2: Text Recognition (OCR)
        try:
            ocr_text, ocr_latency = self.ocr().read_text(frame)
            metrics["ocr_latency_ms"] = ocr_latency
        except Exception as e:
            log.error(f"OCR error in pipeline turn: {e}")
            ocr_text, ocr_latency = "", 0.0
            metrics["ocr_error"] = str(e)

        # Stage 3: Local Response Composition
        answer_text = self._composer.compose(labels, ocr_text, user_question)

        # Stage 4: Text-to-Speech Output
        try:
            self.tts().speak(answer_text)
            metrics["tts_status"] = "Success"
        except Exception as e:
            log.error(f"TTS error in pipeline turn: {e}")
            metrics["tts_status"] = f"Failed: {e}"

        return labels, objects, ocr_text, answer_text, metrics
