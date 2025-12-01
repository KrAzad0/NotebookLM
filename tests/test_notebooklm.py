import tempfile
import unittest
from pathlib import Path

from notebooklm.cli import build_parser
from notebooklm.llm import summarize
from notebooklm.storage import JsonStorage


class NotebookLMTestCase(unittest.TestCase):
    def test_storage_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir) / "notes.json")
            storage.add_note("Title", "Content body", tags=["tag1"])
            storage.add_note("Another", "More content here", tags=["tag2"])

            notes = storage.all_notes()
            self.assertEqual(len(notes), 2)
            self.assertEqual(notes[0].title, "Title")
            self.assertIn("tag1", notes[0].tags)

            results = storage.search("content")
            self.assertEqual(len(results), 2)

    def test_summarize_returns_sentences(self):
        text = (
            "Python is a programming language. It is popular for scripting. "
            "It also powers many data tools."
        )
        sentences = summarize(text, max_sentences=2)
        self.assertEqual(len(sentences), 2)
        self.assertTrue(any("programming language" in s for s in sentences))

    def test_cli_parses_commands(self):
        parser = build_parser()
        args = parser.parse_args(["add", "Title", "Content", "--tags", "one", "two"])
        self.assertEqual(args.command, "add")
        self.assertEqual(args.tags, ["one", "two"])

        args = parser.parse_args(["summarize", "--sentences", "1"])
        self.assertEqual(args.command, "summarize")
        self.assertEqual(args.sentences, 1)
