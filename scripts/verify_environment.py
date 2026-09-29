"""
scripts/verify_environment.py — Diagnostic environment check script for Netra.
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def check_system():
    print("=" * 60)
    print("NETRA ENVIRONMENT & COMPONENT VERIFICATION")
    print("=" * 60)

    print(f"Python Version: {sys.version}")
    print(f"Executable: {sys.executable}")
    print(f"Project Root: {PROJECT_ROOT}\n")

    # 1. Check ONNX Runtime & Providers
    print("[1] Checking ONNX Runtime & Hardware Providers...")
    try:
        import onnxruntime as ort
        print(f"  ONNX Runtime Version: {ort.__version__}")
        providers = ort.get_available_providers()
        print(f"  Available Providers: {providers}")
        if "QNNExecutionProvider" in providers:
            print("  [SUCCESS] Qualcomm QNN Execution Provider IS available!")
        else:
            print("  [INFO] QNN Execution Provider not found. Operating in CPU Fallback mode.")
    except Exception as e:
        print(f"  [ERROR] ONNX Runtime check failed: {e}")

    # 2. Check Model Assets
    print("\n[2] Checking Model Assets...")
    model_path = PROJECT_ROOT / "assets" / "models" / "detector.onnx"
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"  [SUCCESS] detector.onnx found at {model_path} ({size_mb:.2f} MB)")
    else:
        print(f"  [ERROR] detector.onnx missing at {model_path}")

    # 3. Check OCR Engine (EasyOCR)
    print("\n[3] Checking EasyOCR Installation...")
    try:
        import easyocr
        print(f"  [SUCCESS] EasyOCR package is installed ({easyocr.__version__})")
    except Exception as e:
        print(f"  [ERROR] EasyOCR check failed: {e}")

    # 4. Check Text-to-Speech (pyttsx3)
    print("\n[4] Checking Text-to-Speech (pyttsx3 / Windows SAPI)...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("  [SUCCESS] pyttsx3 / Windows SAPI initialized successfully.")
    except Exception as e:
        print(f"  [ERROR] pyttsx3 initialization failed: {e}")

    # 5. Check OpenCV & Camera Device
    print("\n[5] Checking Camera & OpenCV...")
    try:
        import cv2
        print(f"  OpenCV Version: {cv2.__version__}")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("  [SUCCESS] Camera device 0 opened successfully.")
            cap.release()
        else:
            print("  [WARNING] Camera device 0 could not be opened. Connect a webcam for live testing.")
    except Exception as e:
        print(f"  [ERROR] OpenCV check failed: {e}")

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    check_system()
