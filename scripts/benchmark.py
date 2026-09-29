"""
scripts/benchmark.py — Benchmark execution script for Netra ONNX models.
"""

import sys
import os
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.engine import benchmark_provider_comparison
from app.config import DETECTOR_INPUT_SIZE

def run_benchmarks():
    print("Running Netra Detector Benchmarks...")
    sample_input = np.zeros((1, 3, DETECTOR_INPUT_SIZE, DETECTOR_INPUT_SIZE), dtype=np.float32)
    results = benchmark_provider_comparison("detector.onnx", sample_input, runs=30)
    
    benchmarks_dir = PROJECT_ROOT / "benchmarks"
    benchmarks_dir.mkdir(exist_ok=True)
    results_file = benchmarks_dir / "RESULTS.md"

    content = f"# Netra Model Latency & Execution Benchmarks\n\n"
    content += f"**Benchmark Date**: September 29, 2026\n"
    content += f"**Model**: YOLOv8-N ONNX (`detector.onnx`, 12.26 MB)\n"
    content += f"**Input Resolution**: 1x3x640x640 float32\n\n"
    content += "| Execution Provider | Mean Latency (ms) | P95 Latency (ms) | Estimated FPS | Hardware Mode |\n"
    content += "| :--- | :--- | :--- | :--- | :--- |\n"

    for label, res in results.items():
        if "error" in res:
            content += f"| {label} | Error | Error | N/A | {res['error']} |\n"
        else:
            content += f"| {label} | {res['mean_ms']:.2f} ms | {res['p95_ms']:.2f} ms | {res['fps']:.1f} FPS | {res['provider']} |\n"

    content += "\n\n## Execution Provider Status Note\n"
    content += "* **CPUExecutionProvider**: Measured empirically on host processor.\n"
    content += "* **QNNExecutionProvider**: Configured in codebase; hardware acceleration requires Snapdragon ARM64 target device with `onnxruntime-qnn` installed.\n"

    with open(results_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Benchmark results saved to {results_file}")
    print(content)

if __name__ == "__main__":
    run_benchmarks()
