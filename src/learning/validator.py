"""Gradient Delta Shape and Norm Validator for Federated Clients."""
import numpy as np

class GradientValidator:
    @staticmethod
    def validate_delta(delta: np.ndarray, expected_dim: int, max_l2_norm: float = 5.0) -> bool:
        if not isinstance(delta, np.ndarray) or delta.shape != (expected_dim,):
            return False
        if not np.all(np.isfinite(delta)):
            return False
        if float(np.linalg.norm(delta)) > max_l2_norm:
            return False
        return True
