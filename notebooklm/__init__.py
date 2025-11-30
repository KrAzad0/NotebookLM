"""NotebookLM: simple local note taking and summarization utility."""

from .notes import Note, Notebook
from .storage import JsonStorage
from .llm import summarize

__all__ = ["Note", "Notebook", "JsonStorage", "summarize"]
