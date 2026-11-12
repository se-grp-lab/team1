"""Tests for HUD Design Tokens and Theming Profiles."""
import unittest
from src.ui.theme import DEFAULT_THEME, HIGH_CONTRAST_THEME

class TestHUDTheming(unittest.TestCase):
    def test_default_theme_properties(self):
        self.assertEqual(DEFAULT_THEME.border_radius_px, 24)
        self.assertIn("rgba", DEFAULT_THEME.background_rgba.lower() if "rgba" in DEFAULT_THEME.background_rgba else "#")
        self.assertEqual(DEFAULT_THEME.auto_dismiss_delay_ms, 2500)

    def test_high_contrast_theme_accessibility(self):
        self.assertEqual(HIGH_CONTRAST_THEME.text_color, "#ffffff")
        self.assertEqual(HIGH_CONTRAST_THEME.accent_color, "#ffff00")
        self.assertGreater(HIGH_CONTRAST_THEME.font_size_pt, DEFAULT_THEME.font_size_pt)

if __name__ == '__main__':
    unittest.main()
