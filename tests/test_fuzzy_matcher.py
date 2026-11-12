"""Tests for Fuzzy Keyword Matching."""
import unittest
from src.nlu.fuzzy_matcher import FuzzyKeywordMatcher

class TestFuzzyKeywordMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = FuzzyKeywordMatcher(["pause", "play", "fullscreen", "subtitles", "volume"])

    def test_exact_matches(self):
        self.assertEqual(self.matcher.match("pause"), "pause")
        self.assertEqual(self.matcher.match("play"), "play")

    def test_fuzzy_whisper_matches(self):
        self.assertEqual(self.matcher.match("paws"), "pause")
        self.assertEqual(self.matcher.match("fulscreen"), "fullscreen")
        self.assertEqual(self.matcher.match("volum"), "volume")

    def test_unmatched_tokens(self):
        self.assertIsNone(self.matcher.match("randomword"))

if __name__ == '__main__':
    unittest.main()
