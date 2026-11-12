"""Linear Volume Scaler for Heterogeneous Player Ranges."""
class VolumeScaler:
    @staticmethod
    def percent_to_vlc(percent: int) -> int:
        clamped = max(0, min(100, percent))
        return int((clamped / 100.0) * 512)

    @staticmethod
    def vlc_to_percent(vlc_units: int) -> int:
        clamped = max(0, min(512, vlc_units))
        return int((clamped / 512.0) * 100)
