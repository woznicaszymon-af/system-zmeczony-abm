from __future__ import annotations

from dataclasses import dataclass
import numpy as np


def clip01(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))


def safe_mean(values) -> float:
    arr = np.array(list(values), dtype=float)
    return float(arr.mean()) if arr.size else 0.0


def safe_corr(x, y) -> float:
    x = np.array(list(x), dtype=float)
    y = np.array(list(y), dtype=float)
    if x.size < 2 or y.size < 2:
        return 0.0
    if np.isclose(np.std(x), 0.0) or np.isclose(np.std(y), 0.0):
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def gini(values) -> float:
    """Gini coefficient in [0, 1] for non-negative values."""
    x = np.array(list(values), dtype=float)
    if x.size == 0:
        return 0.0
    x = np.clip(x, 0.0, None)
    if np.isclose(x.sum(), 0.0):
        return 0.0
    x = np.sort(x)
    n = x.size
    index = np.arange(1, n + 1)
    return float((2 * (index * x).sum() / (n * x.sum())) - (n + 1) / n)


def logistic(z: float) -> float:
    z = float(z)
    return float(1.0 / (1.0 + np.exp(-z)))


@dataclass(frozen=True)
class EndState:
    status: str  # "running" | "reform" | "collapse" | "max_steps"
    step: int
    resolution_event: bool
    mean_coord: float
    exit_share: float
