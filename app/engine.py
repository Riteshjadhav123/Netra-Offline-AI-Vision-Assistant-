"""
app/engine.py — ONNX Runtime Engine with Qualcomm QNN EP support and CPU fallback.
"""

from __future__ import annotations
import time
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import onnxruntime as ort

from app.config import MODELS_DIR

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("netra.engine")


@dataclass
class InferenceResult:
    outputs: list
    latency_ms: float
    provider_used: str


class NPUModel:
    """Loads an ONNX model, attempting QNN Execution Provider first, falling back to CPU."""

    def __init__(self, model_filename: str, prefer_npu: bool = True):
        model_path = MODELS_DIR / model_filename
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file missing: {model_path}\n"
                f"Please place {model_filename} in assets/models/ directory."
            )

        providers = self._build_provider_list(prefer_npu)
        self.session = ort.InferenceSession(str(model_path), providers=providers)
        self.active_provider = self.session.get_providers()[0]
        self.input_name = self.session.get_inputs()[0].name

        log.info(f"Loaded {model_filename} on provider: {self.active_provider}")

    @staticmethod
    def _build_provider_list(prefer_npu: bool) -> list:
        available = ort.get_available_providers()
        providers = []
        if prefer_npu and "QNNExecutionProvider" in available:
            providers.append((
                "QNNExecutionProvider",
                {
                    "backend_path": "QnnHtp.dll",
                    "htp_performance_mode": "burst",
                    "htp_graph_finalization_optimization_mode": "3",
                },
            ))
        else:
            if prefer_npu:
                log.info("QNNExecutionProvider not present — running on CPUExecutionProvider.")
        providers.append("CPUExecutionProvider")
        return providers

    def run(self, input_array: np.ndarray) -> InferenceResult:
        start = time.perf_counter()
        outputs = self.session.run(None, {self.input_name: input_array})
        latency_ms = (time.perf_counter() - start) * 1000.0
        return InferenceResult(outputs=outputs, latency_ms=latency_ms, provider_used=self.active_provider)


def benchmark_provider_comparison(model_filename: str, sample_input: np.ndarray, runs: int = 20) -> dict:
    """Benchmarks model latency across available providers."""
    results = {}
    for prefer_npu, label in [(True, "QNN (NPU)"), (False, "CPU")]:
        try:
            model = NPUModel(model_filename, prefer_npu=prefer_npu)
            # Warmup run
            model.run(sample_input)
            latencies = [model.run(sample_input).latency_ms for _ in range(runs)]
            results[label] = {
                "provider": model.active_provider,
                "mean_ms": float(np.mean(latencies)),
                "p95_ms": float(np.percentile(latencies, 95)),
                "fps": float(1000.0 / np.mean(latencies)),
            }
        except Exception as e:
            results[label] = {"error": str(e)}
    return results
