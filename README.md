# NotebookLM

A lightweight, local-first note-taking utility with simple summarization.

## Features
- Add, list, and search notes stored in a JSON file (default: `~/.notebooklm/notes.json`).
- Summarize notes using a deterministic TF-IDF-style sentence extractor; no external APIs.
- Customizable storage location via `--storage` flag or `NOTEBOOKLM_HOME` environment variable.

## Getting Started
No third-party dependencies are required. Use any recent Python 3 interpreter.

```bash
python -m notebooklm.cli --help
```

### Examples
Add a note:
```bash
python -m notebooklm.cli add "Project kickoff" "Discussed milestones and owners" --tags work planning
```

List notes:
```bash
python -m notebooklm.cli list
```

Search for a keyword:
```bash
python -m notebooklm.cli search milestones
```

Summarize all notes (or only those matching a query):
```bash
python -m notebooklm.cli summarize --sentences 2
python -m notebooklm.cli summarize --query planning
```

## Tests
Run the unit test suite:
```bash
python -m unittest discover -s tests -p 'test_*.py'
```
