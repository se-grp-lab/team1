"""Tests for Compound Voice Commands."""
import unittest
from src.nlu.compound_commands import CompoundCommandSplitter

class TestCompoundCommands(unittest.TestCase):
    def test_single_command_intact(self):
        self.assertEqual(CompoundCommandSplitter.split("pause playback"), ["pause playback"])

    def test_and_then_conjunction(self):
        res = CompoundCommandSplitter.split("pause the video and then set volume to 50%")
        self.assertEqual(res, ["pause the video", "set volume to 50%"])

    def test_multiple_clauses(self):
        res = CompoundCommandSplitter.split("unmute and fullscreen then speed up")
        self.assertEqual(res, ["unmute", "fullscreen", "speed up"])

if __name__ == '__main__':
    unittest.main()
