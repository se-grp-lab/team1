"""Fuzzy Keyword Token Matcher for Slurred or Whispered Voice Inputs."""
import difflib
from typing import Optional, List

class FuzzyKeywordMatcher:
    PHONETIC_VARIANTS = {
        "paws": "pause",
        "pawsing": "pause",
        "playin": "play",
    }

    def __init__(self, canonical_keywords: List[str], similarity_threshold: float = 0.70):
        self.keywords = [k.lower() for k in canonical_keywords]
        self.threshold = similarity_threshold

    def match(self, token: str) -> Optional[str]:
        cleaned = token.lower().strip()
        if cleaned in self.keywords:
            return cleaned
        if cleaned in self.PHONETIC_VARIANTS and self.PHONETIC_VARIANTS[cleaned] in self.keywords:
            return self.PHONETIC_VARIANTS[cleaned]
        matches = difflib.get_close_matches(cleaned, self.keywords, n=1, cutoff=self.threshold)
        return matches[0] if matches else None
