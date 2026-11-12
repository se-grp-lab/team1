"""Tests for Alias Profile Importer & Exporter."""
import unittest
import tempfile
import os
from src.config.alias_exporter import AliasProfileManager

class TestAliasProfileManager(unittest.TestCase):
    def test_round_trip_export_import(self):
        aliases = {"work": "mute", "chill": "volume 20%"}
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            path = f.name
        try:
            AliasProfileManager.export_profile(aliases, path)
            loaded = AliasProfileManager.import_profile(path)
            self.assertEqual(aliases, loaded)
        finally:
            if os.path.exists(path):
                os.remove(path)

if __name__ == '__main__':
    unittest.main()
