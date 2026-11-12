"""Import and Export Utility for Voice Alias Profiles."""
import json
from typing import Dict

class AliasProfileManager:
    @staticmethod
    def export_profile(aliases: Dict[str, str], filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0", "aliases": aliases}, f, indent=2)

    @staticmethod
    def import_profile(filepath: str) -> Dict[str, str]:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("aliases", {})
