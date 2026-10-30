"""Edge-based private acoustic adaptation (VAMC-F-021).

Learns the user's recurring ASR mistakes entirely on-device. When the user
corrects a misheard command, the (heard -> intended) pair is recorded locally;
once a pair has enough support it is applied automatically to future
transcriptions. A small weight vector (hashed token features) is also kept as
the local model state that federated sync (VAMC-F-022) can share as a delta.
No audio and no text ever leave the device from this module.
"""

import json
import os
import zlib
from collections import Counter
from typing import Dict, Optional, Tuple

import numpy as np

FEATURE_DIM = 64


def _features(text: str) -> np.ndarray:
    vec = np.zeros(FEATURE_DIM, dtype=np.float64)
    for tok in text.lower().split():
        vec[zlib.crc32(tok.encode("utf-8")) % FEATURE_DIM] += 1.0
    return vec


class AcousticAdapter:
    """On-device correction memory with a hashed-feature weight vector."""

    def __init__(self, min_support: int = 2, store_path: Optional[str] = None, learning_rate: float = 0.1):
        self.min_support = min_support
        self.store_path = store_path
        self.learning_rate = learning_rate
        self._pairs: Counter = Counter()
        self.weights = np.zeros(FEATURE_DIM, dtype=np.float64)
        if store_path and os.path.exists(store_path):
            self._load()

    def observe(self, heard: str, intended: str) -> None:
        """Records a user correction and nudges the local weights toward the intended phrase."""
        heard, intended = heard.lower().strip(), intended.lower().strip()
        if not heard or not intended or heard == intended:
            return
        self._pairs[(heard, intended)] += 1
        self.weights += self.learning_rate * (_features(intended) - _features(heard))
        self._save()

    def correct(self, heard: str) -> str:
        """Returns the learned correction for `heard`, or the text unchanged."""
        key = heard.lower().strip()
        best: Tuple[int, Optional[str]] = (0, None)
        for (h, i), n in self._pairs.items():
            if h == key and n >= self.min_support and n > best[0]:
                best = (n, i)
        return best[1] if best[1] else heard

    def weight_vector(self) -> np.ndarray:
        return self.weights.copy()

    def _save(self) -> None:
        if not self.store_path:
            return
        data = {
            "pairs": [[h, i, n] for (h, i), n in self._pairs.items()],
            "weights": self.weights.tolist(),
        }
        tmp = self.store_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        os.replace(tmp, self.store_path)

    def _load(self) -> None:
        with open(self.store_path, encoding="utf-8") as fh:
            data = json.load(fh)
        self._pairs = Counter({(h, i): n for h, i, n in data["pairs"]})
        self.weights = np.array(data["weights"], dtype=np.float64)

    def stats(self) -> Dict[str, int]:
        return {"pairs": len(self._pairs), "corrections_seen": sum(self._pairs.values())}
