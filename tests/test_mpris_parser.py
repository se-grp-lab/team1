"""Tests for MPRIS2 D-Bus Metadata."""
import unittest
from src.controllers.mpris import MPRISMetadataParser

class TestMPRISParser(unittest.TestCase):
    def test_parse_valid_mpris_metadata(self):
        data = {
            "xesam:title": "Midnight City",
            "xesam:artist": ["M83"],
            "xesam:album": "Hurry Up, We're Dreaming"
        }
        res = MPRISMetadataParser.parse_metadata(data)
        self.assertEqual(res["title"], "Midnight City")
        self.assertEqual(res["artist"], "M83")

    def test_parse_empty_metadata_defaults(self):
        res = MPRISMetadataParser.parse_metadata({})
        self.assertEqual(res["title"], "Unknown Title")

if __name__ == '__main__':
    unittest.main()
