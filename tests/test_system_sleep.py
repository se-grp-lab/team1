"""Tests for System Sleep Media Pause."""
import unittest
from src.controllers.system_sleep import SystemSleepHandler

class TestSystemSleep(unittest.TestCase):
    def test_triggers_pause_on_sleep(self):
        paused = False
        def on_pause():
            nonlocal paused
            paused = True
        h = SystemSleepHandler(on_pause)
        h.on_prepare_for_sleep(True)
        self.assertTrue(paused)
        self.assertTrue(h.is_suspended)

if __name__ == '__main__':
    unittest.main()
