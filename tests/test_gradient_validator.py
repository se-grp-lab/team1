"""Tests for Gradient Validator."""
import unittest
import numpy as np
from src.learning.validator import GradientValidator

class TestGradientValidator(unittest.TestCase):
    def test_valid_gradient(self):
        vec = np.zeros(16)
        self.assertTrue(GradientValidator.validate_delta(vec, expected_dim=16))

    def test_dimension_mismatch(self):
        vec = np.zeros(8)
        self.assertFalse(GradientValidator.validate_delta(vec, expected_dim=16))

    def test_non_finite_rejection(self):
        vec = np.array([0.1, float("nan")])
        self.assertFalse(GradientValidator.validate_delta(vec, expected_dim=2))

if __name__ == '__main__':
    unittest.main()
