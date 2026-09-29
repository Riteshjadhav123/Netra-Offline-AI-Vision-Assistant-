"""
app/ocr.py — Offline Text Recognition (OCR) module using EasyOCR.
"""

from __future__ import annotations
import logging
import time
import numpy as np

log = logging.getLogger("netra.ocr")


class OCRReader:
    """Offline EasyOCR text recognition engine."""

    def __init__(self, languages: list[str] = None):
        if languages is None:
            languages = ["en"]
        self.languages = languages
        self._reader = None

    def _ensure_loaded(self):
        if self._reader is None:
            import easyocr
            log.info("Initializing EasyOCR reader (CPU mode)...")
            self._reader = easyocr.Reader(self.languages, gpu=False)
            log.info("EasyOCR reader initialized.")

    def read_text(self, frame: np.ndarray, min_confidence: float = 0.4) -> tuple[str, float]:
        """
        Extracts visible text from a camera frame.
        Returns:
            - text: Consolidated string of recognized words/phrases.
            - latency_ms: Execution time in milliseconds.
        """
        try:
            self._ensure_loaded()
            start = time.perf_counter()
            results = self._reader.readtext(frame)  # [(bbox, text, confidence), ...]
            latency_ms = (time.perf_counter() - start) * 1000.0

            # Sort by confidence descending
            results.sort(key=lambda r: -r[2])
            valid_words = [text.strip() for _, text, conf in results if conf >= min_confidence and text.strip()]
            recognized_text = " ".join(valid_words).strip()
            return recognized_text, latency_ms
        except Exception as e:
            log.error(f"OCR execution error: {e}")
            return "", 0.0
