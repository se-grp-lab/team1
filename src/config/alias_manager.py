"""Configurable Custom Voice Alias Mapping (VAMC-F-006).

Allows users to define custom voice phrases mapped to complex multimedia actions,
persisting mappings in local JSON configuration.
"""

import json
import os
from typing import Dict, Optional


class AliasManager:
    """Manages custom voice command aliases."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "config",
                "default_aliases.json",
            )
        self.config_path = config_path
        self.aliases: Dict[str, str] = {}
        self.load_aliases()

    def load_aliases(self) -> None:
        """Loads aliases from the local configuration file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.aliases = json.load(f)
            except Exception:
                self.aliases = {}
        else:
            self.aliases = {}

    def save_aliases(self) -> None:
        """Persists current aliases to disk."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.aliases, f, indent=2)

    def add_alias(self, alias: str, canonical_command: str) -> None:
        """Adds or updates a custom voice alias."""
        self.aliases[alias.lower().strip()] = canonical_command.strip()
        self.save_aliases()

    def remove_alias(self, alias: str) -> bool:
        """Removes a custom voice alias."""
        key = alias.lower().strip()
        if key in self.aliases:
            del self.aliases[key]
            self.save_aliases()
            return True
        return False

    def resolve(self, text: str) -> str:
        """Resolves an alias to its canonical multimedia command if matched."""
        cleaned = text.lower().strip()
        # Direct phrase match
        if cleaned in self.aliases:
            return self.aliases[cleaned]

        # Check prefix / substring matches
        for alias, target in self.aliases.items():
            if cleaned == alias or cleaned.endswith(" " + alias):
                return target

        return text
