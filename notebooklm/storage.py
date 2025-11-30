"""Persistence helpers for storing notebooks on disk."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from .notes import Notebook, Note

DEFAULT_STORAGE = Path(os.environ.get("NOTEBOOKLM_HOME", Path.home() / ".notebooklm"))
DEFAULT_STORAGE_FILE = DEFAULT_STORAGE / "notes.json"


class JsonStorage:
    """A simple JSON-backed storage engine."""

    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path else DEFAULT_STORAGE_FILE

    def load(self) -> Notebook:
        if not self.path.exists():
            return Notebook()
        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return Notebook.from_dict(data)

    def save(self, notebook: Notebook) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(notebook.to_dict(), f, indent=2)

    def add_note(
        self, title: str, content: str, tags: Optional[list[str]] = None
    ) -> Note:
        notebook = self.load()
        note = Note(title=title, content=content, tags=tags or [])
        notebook.add(note)
        self.save(notebook)
        return note

    def search(self, query: str) -> list[Note]:
        return self.load().search(query)

    def all_notes(self) -> list[Note]:
        return self.load().notes
