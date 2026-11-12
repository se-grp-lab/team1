"""Tests for Volume Normalization Scaler."""
import unittest
from src.controllers.volume_scaler import VolumeScaler

class TestVolumeScaler(unittest.TestCase):
    def test_percent_to_vlc_boundaries(self):
        self.assertEqual(VolumeScaler.percent_to_vlc(0), 0)
        self.assertEqual(VolumeScaler.percent_to_vlc(50), 256)
        self.assertEqual(VolumeScaler.percent_to_vlc(100), 512)
        self.assertEqual(VolumeScaler.percent_to_vlc(150), 512)

    def test_vlc_to_percent_boundaries(self):
        self.assertEqual(VolumeScaler.vlc_to_percent(0), 0)
        self.assertEqual(VolumeScaler.vlc_to_percent(256), 50)
        self.assertEqual(VolumeScaler.vlc_to_percent(512), 100)

if __name__ == '__main__':
    unittest.main()
