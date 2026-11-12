"""VLC HTTP Remote Control Status Parser (VAMC-F-013)."""
import xml.etree.ElementTree as ET
from typing import Dict, Any

class VLCHTTPResponseParser:
    @staticmethod
    def parse_status_xml(xml_payload: str) -> Dict[str, Any]:
        try:
            root = ET.fromstring(xml_payload)
            state = root.findtext("state", "stopped")
            volume = int(root.findtext("volume", "0"))
            time_pos = int(root.findtext("time", "0"))
            length = int(root.findtext("length", "0"))
            return {
                "state": state,
                "volume_percent": int((volume / 512.0) * 100),
                "position_sec": time_pos,
                "duration_sec": length
            }
        except Exception:
            return {"state": "error", "volume_percent": 0, "position_sec": 0, "duration_sec": 0}
