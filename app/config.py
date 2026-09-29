"""
app/config.py — Configuration and relative path resolution for Netra.
"""

import os
from pathlib import Path

# Project Root Directory (robust relative path resolution)
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
MODELS_DIR = PROJECT_ROOT / "assets" / "models"

# Detection settings
DETECTOR_MODEL_NAME = "detector.onnx"
DETECTOR_INPUT_SIZE = 640
DETECTOR_CONF_THRESHOLD = 0.40
DETECTOR_NMS_IOU_THRESHOLD = 0.45
DETECTOR_MAX_LABELS = 6

# COCO 80-Class Labels
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush",
]

# UI Settings
OVERLAY_HEIGHT = 160
FONT_SCALE = 0.55
