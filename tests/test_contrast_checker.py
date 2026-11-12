"""Tests for Visual Accessibility Contrast Compliance."""
import unittest
from src.ui.contrast_checker import contrast_ratio

class TestContrastChecker(unittest.TestCase):
    def test_black_on_white_maximum_contrast(self):
        ratio = contrast_ratio((0, 0, 0), (255, 255, 255))
        self.assertAlmostEqual(ratio, 21.0, places=1)

    def test_yellow_on_black_high_contrast(self):
        ratio = contrast_ratio((255, 255, 0), (0, 0, 0))
        self.assertGreater(ratio, 15.0)

if __name__ == '__main__':
    unittest.main()
