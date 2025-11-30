"""Models representing notebook content."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Note:
    """A single note entry."""

    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        return cls(
            title=data["title"],
            content=data["content"],
            tags=list(data.get("tags", [])),
            created_at=datetime.fromisoformat(data["created_at"]),
        )


class Notebook:
    """A collection of notes."""

    def __init__(self, notes: Optional[List[Note]] = None):
        self.notes: List[Note] = notes or []

    def add(self, note: Note) -> None:
        self.notes.append(note)

    def search(self, query: str) -> List[Note]:
        lower_q = query.lower()
        return [
            note
            for note in self.notes
            if lower_q in note.title.lower()
            or lower_q in note.content.lower()
            or any(lower_q in tag.lower() for tag in note.tags)
        ]

    def to_dict(self) -> dict:
        return {"notes": [note.to_dict() for note in self.notes]}

    @classmethod
    def from_dict(cls, data: dict) -> "Notebook":
        notes = [Note.from_dict(raw) for raw in data.get("notes", [])]
        return cls(notes)
