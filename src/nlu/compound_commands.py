"""Parser for Multi-Clause Compound Media Commands."""
import re
from typing import List

class CompoundCommandSplitter:
    CLAUSE_DELIMITERS = re.compile(r"\s+(?:and\s+then|and|then)\s+", re.IGNORECASE)

    @classmethod
    def split(cls, text: str) -> List[str]:
        raw = text.strip()
        parts = cls.CLAUSE_DELIMITERS.split(raw)
        return [p.strip() for p in parts if p.strip()]
