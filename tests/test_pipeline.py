"""
tests/test_pipeline.py — Integration test for Netra pipeline.
"""

import sys
import unittest
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.pipeline import NetraPipeline

class TestNetraPipeline(unittest.TestCase):

    def test_pipeline_turn_synthetic_frame(self):
        pipeline = NetraPipeline()
        # Create a synthetic 640x480 frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        labels, objects, ocr_text, answer_text, metrics = pipeline.run_turn(frame)

        self.assertIsInstance(labels, list)
        self.assertIsInstance(objects, list)
        self.assertIsInstance(ocr_text, str)
        self.assertIsInstance(answer_text, str)
        self.assertIn("det_latency_ms", metrics)
        print("Integration Test Passed! Response text:", answer_text)

if __name__ == "__main__":
    unittest.main()
