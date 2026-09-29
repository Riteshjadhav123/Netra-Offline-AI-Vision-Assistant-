# Netra Model Latency & Execution Benchmarks

**Benchmark Date**: September 29, 2026
**Model**: YOLOv8-N ONNX (`detector.onnx`, 12.26 MB)
**Input Resolution**: 1x3x640x640 float32

| Execution Provider | Mean Latency (ms) | P95 Latency (ms) | Estimated FPS | Hardware Mode |
| :--- | :--- | :--- | :--- | :--- |
| QNN (NPU) | 40.13 ms | 42.11 ms | 24.9 FPS | CPUExecutionProvider |
| CPU | 40.22 ms | 44.14 ms | 24.9 FPS | CPUExecutionProvider |


## Execution Provider Status Note
* **CPUExecutionProvider**: Measured empirically on host processor.
* **QNNExecutionProvider**: Configured in codebase; hardware acceleration requires Snapdragon ARM64 target device with `onnxruntime-qnn` installed.
