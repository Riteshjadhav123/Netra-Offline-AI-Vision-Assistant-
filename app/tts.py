"""
app/tts.py — Offline Text-to-Speech (TTS) module using pyttsx3 / Windows SAPI.
"""

from __future__ import annotations
import logging

log = logging.getLogger("netra.tts")


class TTSEngine:
    """Offline Text-to-Speech synthesis using Windows SAPI / pyttsx3."""

    def __init__(self):
        self._engine = None

    def _ensure_engine(self):
        if self._engine is None:
            import pyttsx3
            log.info("Initializing pyttsx3 TTS engine...")
            self._engine = pyttsx3.init()
            # Configure voice rate and volume for readability
            try:
                self._engine.setProperty("rate", 165)
                self._engine.setProperty("volume", 0.95)
            except Exception as e:
                log.warning(f"Could not set TTS properties: {e}")
            log.info("TTS engine initialized.")

    def speak(self, text: str) -> bool:
        """
        Synthesizes and speaks the given text string out loud.
        """
        if not text or not text.strip():
            return False

        try:
            self._ensure_engine()
            log.info(f"Speaking: '{text}'")
            self._engine.say(text)
            self._engine.runAndWait()
            return True
        except Exception as e:
            log.error(f"TTS Speech error: {e}")
            return False
