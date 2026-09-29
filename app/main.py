"""
app/main.py — Main Application Entry Point and High-Contrast Accessibility UI.
"""

from __future__ import annotations
import logging
import textwrap
import sys
import cv2
import numpy as np

from app.config import OVERLAY_HEIGHT, FONT_SCALE
from app.pipeline import NetraPipeline

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("netra.main")

COLOR_BG = (20, 20, 20)
COLOR_TEXT_MAIN = (255, 255, 255)
COLOR_TEXT_STATUS = (0, 230, 0)
COLOR_TEXT_SAYS = (0, 200, 255)
COLOR_TEXT_MUTED = (180, 180, 180)
COLOR_BOX = (0, 220, 100)


def open_camera() -> tuple[cv2.VideoCapture | None, str]:
    """
    Attempts to open the best working webcam using DirectShow (CAP_DSHOW) or default backends.
    Prevents MSMF error -1072875772 on Windows.
    """
    backends = []
    if sys.platform.startswith("win"):
        backends.append((0, cv2.CAP_DSHOW, "DirectShow Device 0"))
        backends.append((1, cv2.CAP_DSHOW, "DirectShow Device 1"))
    backends.append((0, cv2.CAP_ANY, "Default Device 0"))
    backends.append((1, cv2.CAP_ANY, "Default Device 1"))

    for idx, backend, desc in backends:
        try:
            cap = cv2.VideoCapture(idx, backend) if backend != cv2.CAP_ANY else cv2.VideoCapture(idx)
            if cap.isOpened():
                ok, test_frame = cap.read()
                if ok and test_frame is not None and test_frame.size > 0:
                    log.info(f"Successfully opened camera: {desc} (Resolution: {test_frame.shape[1]}x{test_frame.shape[0]})")
                    return cap, desc
                cap.release()
        except Exception as e:
            log.debug(f"Failed opening camera {desc}: {e}")

    log.warning("No working physical webcam found. Netra will run in demonstration mode.")
    return None, "Demonstration Mode (No Camera)"


def draw_bounding_boxes(frame: np.ndarray, objects: list) -> np.ndarray:
    """Draws bounding boxes and labels for detected objects on the camera frame."""
    canvas = frame.copy()
    for obj in objects:
        x1, y1, x2, y2 = obj.bbox
        cv2.rectangle(canvas, (x1, y1), (x2, y2), COLOR_BOX, 2)
        label_text = f"{obj.label} ({int(obj.confidence * 100)}%)"

        (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(canvas, (x1, max(0, y1 - 22)), (x1 + tw + 6, max(th + 2, y1)), COLOR_BOX, -1)
        cv2.putText(
            canvas, label_text, (x1 + 3, max(th, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA
        )
    return canvas


def draw_overlay_panel(
    frame: np.ndarray, labels_text: str, ocr_text: str, answer_text: str, status: str, provider_info: str
) -> np.ndarray:
    """Draws a high-contrast dashboard panel beneath the camera view."""
    h, w = frame.shape[:2]
    canvas = cv2.copyMakeBorder(frame, 0, OVERLAY_HEIGHT, 0, 0, cv2.BORDER_CONSTANT, value=COLOR_BG)

    y = h + 24
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Header / Status
    cv2.putText(canvas, f"NETRA AI ASSISTANT | Status: {status}", (14, y), font, FONT_SCALE, COLOR_TEXT_STATUS, 1, cv2.LINE_AA)
    y += 24

    # Execution Engine Info
    cv2.putText(canvas, f"Engine Provider: {provider_info or 'CPU Execution Provider'}", (14, y), font, FONT_SCALE - 0.05, COLOR_TEXT_MUTED, 1, cv2.LINE_AA)
    y += 24

    # Detected Objects
    cv2.putText(canvas, f"Sees: {labels_text or '-'}", (14, y), font, FONT_SCALE, COLOR_TEXT_MAIN, 1, cv2.LINE_AA)
    y += 24

    # OCR Text
    cv2.putText(canvas, f"Reads: {(ocr_text or '-')[:75]}", (14, y), font, FONT_SCALE, COLOR_TEXT_MAIN, 1, cv2.LINE_AA)
    y += 24

    # Spoken Answer Lines
    answer_prefix = "Says: "
    full_answer = answer_prefix + (answer_text or "-")
    wrapped_lines = textwrap.wrap(full_answer, width=85)[:2]
    for line in wrapped_lines:
        cv2.putText(canvas, line, (14, y), font, FONT_SCALE, COLOR_TEXT_SAYS, 1, cv2.LINE_AA)
        y += 22

    return canvas


def run_app():
    """Launches Netra visual assistant application."""
    log.info("Starting Netra Visual Assistant...")
    pipeline = NetraPipeline()

    cap, cam_desc = open_camera()
    has_cam = (cap is not None)

    labels_text, ocr_text, answer_text = "", "", ""
    status = "Ready — Press SPACE to look & speak"
    provider_info = f"Camera: {cam_desc}"
    detected_objects = []

    try:
        while True:
            frame = None
            if has_cam and cap is not None:
                ok, frame = cap.read()
                if not ok or frame is None or frame.size == 0:
                    log.warning("Webcam frame read failed. Re-attempting camera connection...")
                    cap.release()
                    cap, cam_desc = open_camera()
                    has_cam = (cap is not None)
                    if not has_cam:
                        frame = None

            if frame is None:
                # Render synthetic fallback frame for demo mode
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "DEMO MODE — PRESS SPACE TO RUN TEST TURN", (40, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 1, cv2.LINE_AA)

            annotated_frame = draw_bounding_boxes(frame, detected_objects)
            display = draw_overlay_panel(annotated_frame, labels_text, ocr_text, answer_text, status, provider_info)

            try:
                cv2.imshow("Netra — Offline AI Vision Assistant for Snapdragon PCs", display)
                key = cv2.waitKey(30) & 0xFF
            except cv2.error as e:
                log.warning(f"GUI display error ({e}). Executing single-turn pipeline output.")
                labels, objects, ocr_text, answer_text, metrics = pipeline.run_turn(frame)
                break

            if key == ord(" "):
                status = "Processing visual scene & text..."
                display = draw_overlay_panel(annotated_frame, labels_text, ocr_text, answer_text, status, provider_info)
                try:
                    cv2.imshow("Netra — Offline AI Vision Assistant for Snapdragon PCs", display)
                    cv2.waitKey(1)
                except cv2.error:
                    pass

                labels, objects, ocr_text, answer_text, metrics = pipeline.run_turn(frame)
                labels_text = ", ".join(labels)
                detected_objects = objects

                det_ms = metrics.get("det_latency_ms", 0.0)
                ocr_ms = metrics.get("ocr_latency_ms", 0.0)
                provider = metrics.get("provider", "CPUExecutionProvider")
                provider_info = f"{provider} (Detection: {det_ms:.1f}ms, OCR: {ocr_ms:.1f}ms)"
                status = "Ready — Press SPACE to look & speak"

            elif key in (ord("q"), 27):  # Q or ESC
                log.info("Quitting Netra...")
                break
    finally:
        if cap and cap.isOpened():
            cap.release()
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass


if __name__ == "__main__":
    run_app()
