"""Tests for HUD Screen Coordinates."""
import unittest
from src.ui.positioning import HUDPositioner

class TestHUDPositioner(unittest.TestCase):
    def test_centered_horizontal_position(self):
        x, y = HUDPositioner.calculate_pill_coordinates(1920, 1080, pill_width=300, pill_height=60, margin_bottom=40)
        self.assertEqual(x, (1920 - 300) // 2)
        self.assertEqual(y, 1080 - 60 - 40)

    def test_4k_display_coordinates(self):
        x, y = HUDPositioner.calculate_pill_coordinates(3840, 2160, pill_width=400, pill_height=80, margin_bottom=60)
        self.assertEqual(x, (3840 - 400) // 2)
        self.assertEqual(y, 2160 - 80 - 60)

if __name__ == '__main__':
    unittest.main()
