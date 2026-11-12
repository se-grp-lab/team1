"""Tests for Unified Player Status Schema."""
import unittest
from src.controllers.status import UnifiedPlayerStatus

class TestUnifiedPlayerStatus(unittest.TestCase):
    def test_schema_instantiation(self):
        st = UnifiedPlayerStatus(
            player_name="mpv",
            is_playing=True,
            volume=75,
            position_seconds=45.2,
            duration_seconds=180.0,
            track_title="Sample Video"
        )
        self.assertEqual(st.player_name, "mpv")
        self.assertTrue(st.is_playing)
        self.assertEqual(st.volume, 75)
        self.assertEqual(st.rate, 1.0)

if __name__ == '__main__':
    unittest.main()
