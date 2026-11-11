"""Differentially private federated weight synchronization (VAMC-F-022).

Clients share only a clipped, Gaussian-noised weight delta (DP-FedAvg style).
Raw audio, transcripts and the unperturbed delta never leave the device. A
simple accountant tracks cumulative epsilon and refuses to sync past the budget.
"""

import math
from typing import Callable, List, Optional

import numpy as np


class PrivacyBudgetExceeded(RuntimeError):
    """Raised when another sync round would exceed the epsilon budget."""


def clip_update(delta: np.ndarray, clip_norm: float) -> np.ndarray:
    """Scales `delta` so its L2 norm is at most `clip_norm`."""
    if not isinstance(clip_norm, (int, float)) or isinstance(clip_norm, bool) or not math.isfinite(clip_norm) or clip_norm <= 0:
        raise ValueError("clip_norm must be a finite positive number")
    if not isinstance(delta, np.ndarray) or delta.dtype.kind != "f":
        raise TypeError("delta must be a float numpy array")
    if not np.all(np.isfinite(delta)):
        raise ValueError("delta must contain only finite numbers (no NaN or Inf)")
    norm = float(np.linalg.norm(delta))
    return delta if norm <= clip_norm else delta * (clip_norm / norm)


def aggregate(updates: List[np.ndarray]) -> np.ndarray:
    """Server-side federated averaging of client updates."""
    if not updates:
        raise ValueError("no client updates to aggregate")
    for u in updates:
        if not isinstance(u, np.ndarray) or u.dtype.kind != "f":
            raise TypeError("all updates must be float numpy arrays")
        if not np.all(np.isfinite(u)):
            raise ValueError("all updates must contain only finite numbers (no NaN or Inf)")
    return np.mean(np.stack(updates), axis=0)


class FederatedClient:
    """Prepares and uploads differentially private updates."""

    def __init__(self, clip_norm: float = 1.0, noise_multiplier: float = 1.1, delta: float = 1e-5,
                 epsilon_budget: float = 20.0, seed: Optional[int] = None,
                 uploader: Optional[Callable[[np.ndarray], None]] = None):
        if (not isinstance(clip_norm, (int, float)) or isinstance(clip_norm, bool)
                or not math.isfinite(clip_norm) or clip_norm <= 0):
            raise ValueError("clip_norm must be a finite positive number")
        if (not isinstance(noise_multiplier, (int, float)) or isinstance(noise_multiplier, bool)
                or not math.isfinite(noise_multiplier) or noise_multiplier <= 0):
            raise ValueError("noise_multiplier must be a finite positive number")
        if (not isinstance(delta, (int, float)) or isinstance(delta, bool)
                or not math.isfinite(delta) or not (0 < delta < 1)):
            raise ValueError("delta must be a finite number strictly between 0 and 1")
        if (not isinstance(epsilon_budget, (int, float)) or isinstance(epsilon_budget, bool)
                or not math.isfinite(epsilon_budget) or epsilon_budget <= 0):
            raise ValueError("epsilon_budget must be a finite positive number")
        self.clip_norm = float(clip_norm)
        self.noise_multiplier = float(noise_multiplier)
        self.delta = float(delta)
        self.epsilon_budget = float(epsilon_budget)
        self.epsilon_spent = 0.0
        self.rounds = 0
        self._rng = np.random.default_rng(seed)
        self._uploader = uploader

    @property
    def epsilon_per_round(self) -> float:
        """Gaussian-mechanism epsilon for one round at the configured noise multiplier."""
        return math.sqrt(2.0 * math.log(1.25 / self.delta)) / self.noise_multiplier

    def prepare_update(self, weight_delta: np.ndarray) -> np.ndarray:
        """Clips and noises a local weight delta, charging the privacy budget."""
        if not isinstance(weight_delta, np.ndarray) or weight_delta.dtype.kind != "f":
            raise TypeError("only float weight deltas may be synchronized (never audio or text)")
        if not np.all(np.isfinite(weight_delta)):
            raise ValueError("weight_delta must contain only finite numbers (no NaN or Inf)")
        if self.epsilon_spent + self.epsilon_per_round > self.epsilon_budget:
            raise PrivacyBudgetExceeded(
                f"epsilon budget {self.epsilon_budget} exhausted after {self.rounds} rounds"
            )
        clipped = clip_update(weight_delta, self.clip_norm)
        noise = self._rng.normal(0.0, self.noise_multiplier * self.clip_norm, size=clipped.shape)
        self.epsilon_spent += self.epsilon_per_round
        self.rounds += 1
        return clipped + noise

    def sync(self, weight_delta: np.ndarray) -> np.ndarray:
        """Prepares a private update and uploads it. Returns what was sent."""
        private = self.prepare_update(weight_delta)
        if self._uploader:
            self._uploader(private)
        return private
