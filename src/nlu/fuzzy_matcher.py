"""Fuzzy Keyword Token Matcher for Slurred or Whispered Voice Inputs."""
import difflib
from typing import Optional, List

class FuzzyKeywordMatcher:
    def __init__(self, canonical_keywords: List[str], similarity_threshold: float = 0.78):
        self.keywords = [k.lower() for k in canonical_keywords]
        self.threshold = similarity_threshold

    def match(self, token: str) -> Optional[str]:
        cleaned = token.lower().strip()
        if cleaned in self.keywords:
            return cleaned
        matches = difflib.get_close_matches(cleaned, self.keywords, n=1, cutoff=self.threshold)
        return matches[0] if matches else None
