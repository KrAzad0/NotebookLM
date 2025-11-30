"""Command line interface for NotebookLM."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

from .llm import summarize
from .storage import JsonStorage


def _format_note(note) -> str:
    tags = f" [tags: {', '.join(note.tags)}]" if note.tags else ""
    return f"- {note.title}{tags}\n  {note.content}"


def handle_add(args: argparse.Namespace) -> None:
    storage = JsonStorage(Path(args.storage) if args.storage else None)
    note = storage.add_note(args.title, args.content, args.tags)
    print(f"Added note '{note.title}'")


def handle_list(args: argparse.Namespace) -> None:
    storage = JsonStorage(Path(args.storage) if args.storage else None)
    for note in storage.all_notes():
        print(_format_note(note))


def handle_search(args: argparse.Namespace) -> None:
    storage = JsonStorage(Path(args.storage) if args.storage else None)
    results = storage.search(args.query)
    if not results:
        print("No matching notes")
        return
    for note in results:
        print(_format_note(note))


def handle_summarize(args: argparse.Namespace) -> None:
    storage = JsonStorage(Path(args.storage) if args.storage else None)
    notes = storage.search(args.query) if args.query else storage.all_notes()
    text = "\n\n".join(note.content for note in notes)
    sentences = summarize(text, max_sentences=args.sentences)
    if not sentences:
        print("No content available to summarize")
        return
    print("Summary:")
    for sentence in sentences:
        print(f"- {sentence}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=dedent(
            """
            NotebookLM: lightweight note taking and summarization.

            Notes are stored locally in JSON (default: ~/.notebooklm/notes.json).
            """
        ).strip()
    )
    parser.add_argument(
        "--storage",
        help="Path to storage file (default: ~/.notebooklm/notes.json)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("title", help="Title of the note")
    add_parser.add_argument("content", help="Content of the note")
    add_parser.add_argument("--tags", nargs="*", default=[], help="Optional tags")
    add_parser.set_defaults(func=handle_add)

    list_parser = subparsers.add_parser("list", help="List all notes")
    list_parser.set_defaults(func=handle_list)

    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("query", help="Search query")
    search_parser.set_defaults(func=handle_search)

    summarize_parser = subparsers.add_parser("summarize", help="Summarize notes")
    summarize_parser.add_argument(
        "--query",
        help="Only summarize notes matching this query",
    )
    summarize_parser.add_argument(
        "--sentences", type=int, default=3, help="Maximum sentences in summary"
    )
    summarize_parser.set_defaults(func=handle_summarize)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
