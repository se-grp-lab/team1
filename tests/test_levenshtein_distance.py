"""Tests for Levenshtein Distance Matrix."""
import unittest
from src.learning.distance import levenshtein_distance

class TestLevenshteinDistance(unittest.TestCase):
    def test_identical_strings(self):
        self.assertEqual(levenshtein_distance("pause", "pause"), 0)

    def test_one_substitution(self):
        self.assertEqual(levenshtein_distance("paws", "pause"), 2)

    def test_insertions_and_deletions(self):
        self.assertEqual(levenshtein_distance("play", "playing"), 3)

if __name__ == '__main__':
    unittest.main()
