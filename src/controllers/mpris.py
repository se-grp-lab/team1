"""Linux MPRIS2 D-Bus Media Controller Interface."""
from typing import Dict, Any, Optional

class MPRISMetadataParser:
    @staticmethod
    def parse_metadata(raw_metadata: Dict[str, Any]) -> Dict[str, str]:
        title = str(raw_metadata.get("xesam:title", "Unknown Title"))
        artist = str(raw_metadata.get("xesam:artist", ["Unknown Artist"])[0] if isinstance(raw_metadata.get("xesam:artist"), list) else raw_metadata.get("xesam:artist", "Unknown"))
        album = str(raw_metadata.get("xesam:album", "Unknown Album"))
        return {"title": title, "artist": artist, "album": album}
