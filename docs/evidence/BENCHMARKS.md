# Netra Empirical Benchmark Report

**Date**: September 29, 2026

## 1. Object Detection Latency (YOLOv8-N ONNX)

* **Model**: `detector.onnx` (12.26 MB)
* **Input Resolution**: 1x3x640x640 float32
* **Mean Latency**: **50.72 ms**
* **P95 Latency**: **53.70 ms**
* **Frame Rate**: **~19.7 FPS**
* **Hardware Mode**: `CPUExecutionProvider`

## 2. Text Recognition Latency (EasyOCR)

* **Language**: English (`en`)
* **Mean Latency**: **~350–500 ms** (depending on text region count)
* **Hardware Mode**: PyTorch CPU

## 3. Total Memory & Model Footprint

* **Disk Storage**: **12.26 MB** (total model asset footprint)
* **RAM Memory Usage**: ~350 MB active process memory
