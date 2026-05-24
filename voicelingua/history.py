"""Translation history manager.

Stores, retrieves, and manages translation history with
persistence support.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class HistoryEntry:
    """A single translation history entry."""

    def __init__(
        self,
        source_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        timestamp: Optional[str] = None,
    ):
        self.source_text = source_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "timestamp": self.timestamp,
        }


class HistoryManager:
    """Manages translation history with optional persistence."""

    def __init__(self, max_entries: int = 100, persist: bool = False):
        self.max_entries = max_entries
        self.persist = persist
        self._entries: list[HistoryEntry] = []
        if persist:
            self._load()

    def add(self, result) -> HistoryEntry:
        """Add a translation result to history."""
        entry = HistoryEntry(
            source_text=result.source_text,
            translated_text=result.translated_text,
            source_lang=result.source_lang,
            target_lang=result.target_lang,
        )
        self._entries.insert(0, entry)
        if len(self._entries) > self.max_entries:
            self._entries.pop()
        if self.persist:
            self._save()
        return entry

    def get_all(self) -> list[dict]:
        """Get all history entries."""
        return [e.to_dict() for e in self._entries]

    def get_recent(self, count: int = 10) -> list[dict]:
        """Get recent history entries."""
        return [e.to_dict() for e in self._entries[:count]]

    def search(self, query: str) -> list[dict]:
        """Search history by text content."""
        query = query.lower()
        matches = [
            e for e in self._entries
            if query in e.source_text.lower() or query in e.translated_text.lower()
        ]
        return [e.to_dict() for e in matches]

    def clear(self):
        """Clear all history."""
        self._entries.clear()
        if self.persist:
            self._save()

    @property
    def count(self) -> int:
        """Number of history entries."""
        return len(self._entries)

    def _save(self):
        """Persist history to file."""
        path = Path.home() / ".voicelingua" / "history.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.get_all(), f, indent=2)

    def _load(self):
        """Load history from file."""
        path = Path.home() / ".voicelingua" / "history.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                self._entries = [
                    HistoryEntry(**entry) for entry in data
                ]
