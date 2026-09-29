"""
app/response_composer.py — Lightweight local response composer for Netra.
Synthesizes detected objects and recognized text into natural spoken descriptions.
"""

from __future__ import annotations
import logging

log = logging.getLogger("netra.composer")


class LocalResponseComposer:
    """
    Composes natural spoken summaries from local object detection and OCR inputs.
    Note: This is a deterministic local response composer optimized for low latency
    and minimal storage footprint.
    """

    @staticmethod
    def compose(labels: list[str], ocr_text: str, user_question: str | None = None) -> str:
        """
        Synthesizes detected visual labels and OCR text into a spoken sentence.
        """
        if not labels and not ocr_text:
            return "I don't see any clear objects or text in front of you. Try pointing the camera closer."

        parts = []

        # Summarize objects
        if labels:
            if len(labels) == 1:
                obj_str = f"a {labels[0]}"
            elif len(labels) == 2:
                obj_str = f"a {labels[0]} and a {labels[1]}"
            else:
                formatted = [f"a {l}" for l in labels[:-1]]
                obj_str = ", ".join(formatted) + f", and a {labels[-1]}"
            parts.append(f"I see {obj_str}.")

        # Summarize OCR text
        if ocr_text:
            cleaned_text = ocr_text.strip()
            if len(cleaned_text) > 100:
                cleaned_text = cleaned_text[:100] + "..."
            parts.append(f"The visible text reads: '{cleaned_text}'.")

        response = " ".join(parts)
        return response
