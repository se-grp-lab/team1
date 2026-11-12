"""Trie-based Prefix Index for Fast Command Lookups."""
from typing import Dict, Any, Optional

class CommandTrie:
    def __init__(self):
        self.root: Dict[str, Any] = {}

    def insert(self, phrase: str, action: str):
        node = self.root
        for word in phrase.lower().split():
            node = node.setdefault(word, {})
        node["__action__"] = action

    def search(self, phrase: str) -> Optional[str]:
        node = self.root
        for word in phrase.lower().split():
            if word not in node:
                return None
            node = node[word]
        return node.get("__action__")
