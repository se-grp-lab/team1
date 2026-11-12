"""Tests for VLC XML Response Parsing."""
import unittest
from src.controllers.vlc_http import VLCHTTPResponseParser

class TestVLCHTTPParser(unittest.TestCase):
    def test_parse_playing_xml(self):
        sample = """<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<root>
    <state>playing</state>
    <volume>256</volume>
    <time>120</time>
    <length>360</length>
</root>"""
        res = VLCHTTPResponseParser.parse_status_xml(sample)
        self.assertEqual(res["state"], "playing")
        self.assertEqual(res["volume_percent"], 50)
        self.assertEqual(res["position_sec"], 120)

    def test_parse_invalid_xml_graceful_fallback(self):
        res = VLCHTTPResponseParser.parse_status_xml("invalid xml")
        self.assertEqual(res["state"], "error")

if __name__ == '__main__':
    unittest.main()
