# Netra Technical Architecture

## System Architecture Diagram

```
                 ┌────────────────────────────────────────────┐
                 │              Netra Desktop App             │
                 │        (OpenCV Accessible Dashboard)       │
                 └───────────────┬────────────────────────────┘
                                 │ Camera Frame
        ┌────────────────────────┴────────────────────────┐
        ▼                                                 ▼
 ┌───────────────────────────┐                     ┌───────────────────────────┐
 │   Object Detector (ONNX)  │                     │   Text Reader (EasyOCR)   │
 │   YOLOv8-N (640x640 input)│                     │     (Text Recognition)    │
 └──────────────┬────────────┘                     └─────────────┬─────────────┘
                │ Detected Class Labels & Boxes                  │ Recognized Text
                └────────────────────────┬───────────────────────┘
                                         ▼
                        ┌─────────────────────────────────┐
                        │     Local Response Composer     │
                        │ (Natural Language Synthesis)    │
                        └────────────────┬────────────────┘
                                         ▼
                        ┌─────────────────────────────────┐
                        │     Text-to-Speech Engine       │
                        │    (pyttsx3 / Windows SAPI)     │
                        └────────────────┬────────────────┘
                                         ▼
                             🔊 Spoken Audio Response
```

## Component Breakdown

1. **`app/engine.py`**: Wraps ONNX Runtime. Attempts to load `QNNExecutionProvider` with `QnnHtp.dll` burst mode settings for Snapdragon Hexagon NPU. Falls back to `CPUExecutionProvider` if QNN EP is absent.
2. **`app/detector.py`**: Runs YOLOv8-N ONNX inference (`detector.onnx`, 12.26 MB). Performs 640x640 letterbox preprocessing, confidence filtering (threshold 0.4), and OpenCV NMS box calculation.
3. **`app/ocr.py`**: Executes EasyOCR text extraction on CPU, filtering results above 40% confidence.
4. **`app/response_composer.py`**: Synthesizes visual labels and read text into concise, natural spoken descriptions.
5. **`app/tts.py`**: Converts synthesized response into audible spoken audio via Windows SAPI / `pyttsx3`.
6. **`app/main.py`**: High-contrast dashboard overlay displaying status, bounding boxes, recognized text, and spoken response.
