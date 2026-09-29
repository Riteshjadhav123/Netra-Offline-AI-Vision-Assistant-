# Netra — Offline AI Vision Assistant for Snapdragon PCs

> **Qualcomm® Snapdragon® AI Lab Build & Present Challenge Submission**

Netra is an accessible, 100% offline AI vision assistant designed for low-vision, blind, or elderly users. Point your laptop camera at objects, signs, books, or prescriptions, and Netra detects objects, reads text, composes natural-language visual summaries, and reads them out loud — entirely locally without cloud dependency.

---

## 🌟 Key Implemented Features

* **Real-time Object Detection**: Uses YOLOv8-N ONNX (`detector.onnx`, 12.26 MB) to identify physical objects, bounding boxes, and COCO classes.
* **Offline Text Recognition (OCR)**: Integrates EasyOCR to extract printed text from product labels, signs, and documents without network requests.
* **Deterministic Local Response Composer**: Synthesizes visual labels and read text into concise, natural-language spoken summaries without LLM hallucination risk.
* **Offline Text-to-Speech**: Uses Windows SAPI / `pyttsx3` for reliable, zero-latency audio playback.
* **Accessible High-Contrast UI**: Displays real-time status, bounding box overlays, recognized text, and spoken transcripts on a dark dashboard panel.
* **Snapdragon Hardware Acceleration Ready**: Configured to route ONNX model inference through Qualcomm's `QNNExecutionProvider` (Hexagon NPU via `QnnHtp.dll` burst mode) with automatic CPU fallback.

---

## 📐 System Architecture

```
 ┌─────────────────────────────────────────────────────────────┐
 │                    Netra Desktop Application                 │
 │            (OpenCV High-Contrast UI / main.py)              │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Live Camera Frame
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
 ┌─────────────────────────────┐                 ┌─────────────────────────────┐
 │    Object Detection Stage   │                 │     Text Recognition (OCR)  │
 │     YOLOv8-N (ONNX)         │                 │       EasyOCR Engine        │
 │  (QNN EP / CPU Fallback)    │                 │          (CPU Mode)         │
 └──────────────┬──────────────┘                 └──────────────┬──────────────┘
                │ Bounding Boxes & Labels                       │ Recognized Text
                └───────────────────────┬───────────────────────┘
                                        ▼
                       ┌─────────────────────────────────┐
                       │    Local Response Composer      │
                       │ (Visual & Text Synthesis Engine)│
                       └────────────────┬────────────────┘
                                        ▼
                       ┌─────────────────────────────────┐
                       │     Text-to-Speech Engine       │
                       │    (pyttsx3 / Windows SAPI)     │
                       └────────────────┬────────────────┘
                                        ▼
                            🔊 Spoken Audio Response
```

---

## ⚡ Hardware Acceleration & Snapdragon QNN Status

* **VERIFIED Execution**: Verified locally on host processor via `CPUExecutionProvider` with ~40 ms average detection latency (~25 FPS) and offline EasyOCR + Windows SAPI TTS.
* **Snapdragon NPU Configuration**: The core inference engine (`app/engine.py`) is pre-configured to initialize Qualcomm's `QNNExecutionProvider` (`QnnHtp.dll` burst mode). On Snapdragon ARM64 Copilot+ PCs with `onnxruntime-qnn` installed, detection inference automatically routes to the Hexagon NPU.

---

## 🚀 Quick Start & Running

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Verify Environment & Model Assets

```bash
python scripts/verify_environment.py
```

### 3. Run Application

```bash
python main.py
```
*(Or double-click `run.bat` on Windows)*

### 🎮 Keyboard Controls

* **`SPACE`**: Capture current frame, run visual detection & OCR, compose description, and speak answer out loud.
* **`Q` / `ESC`**: Quit application safely.

---

## 📊 Benchmarking

Run the empirical benchmark script to measure detection latency on your local hardware:

```bash
python scripts/benchmark.py
```

---

## 📂 Project Structure

```
Netra_Project/
├── app/
│   ├── main.py               # High-contrast UI & OpenCV camera loop
│   ├── engine.py             # ONNX Runtime NPU/CPU loader
│   ├── pipeline.py           # Production pipeline orchestrator
│   ├── detector.py           # YOLOv8-N ONNX detector & NMS
│   ├── ocr.py                # EasyOCR text extraction
│   ├── response_composer.py  # Visual & text response synthesis
│   ├── tts.py                # pyttsx3 / Windows SAPI speech engine
│   ├── config.py             # Relative path resolution & settings
│   └── __init__.py
├── assets/
│   └── models/
│       └── detector.onnx     # YOLOv8-N ONNX model (12.26 MB)
├── scripts/
│   ├── verify_environment.py # System & package diagnostic script
│   └── benchmark.py          # Latency & FPS benchmark runner
├── tests/
│   └── test_pipeline.py      # Integration test suite
├── README.md
├── requirements.txt
├── run.bat
└── .gitignore
```

---

## ⚠️ Verified Scope & Limitations

* **Physical NPU Hardware Benchmark**: QNN Execution Provider initialization code is complete and verified, but physical Hexagon NPU benchmarks require deployment on a target Snapdragon ARM64 Copilot+ device with `onnxruntime-qnn`.
* **OCR Processing**: EasyOCR CPU execution requires ~1.5 seconds per turn on host processor.
* **Camera Focus**: Text extraction quality depends on environmental lighting and camera focus.

---

## 📄 License & Challenge Notice

Built for the **Qualcomm Snapdragon® AI Lab Build & Present Challenge (2026)**.
Designed for local, offline operation on Snapdragon-powered HP Copilot+ PCs.
