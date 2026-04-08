# pinote

A command-line interface for Apple Notes on macOS, powered by AppleScript.

## Requirements

- macOS
- Python 3.10+
- Apple Notes app

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/JacquesNguyen/pinote.git
cd pinote
pip install -e .
```

This installs the `pinote` command globally in your environment.

## Commands

### list

List all notes with their IDs and titles.

```bash
pinote list
```

Example output:
```
x-coredata://... - Shopping list
x-coredata://... - Meeting notes
```

### read

Display the title and plaintext content of a note.

```bash
pinote read <note-id>
```

Example:
```bash
pinote read "x-coredata://abc123/..."
```

### create

Create a new note with a title and optional body.

```bash
pinote create <title> [body]
```

Example:
```bash
pinote create "My Note" "This is the content."
```

### update

Update the title and body of an existing note.

```bash
pinote update <note-id> <title> <body>
```

Example:
```bash
pinote update "x-coredata://abc123/..." "Updated Title" "Updated content."
```

## Development

Install dev dependencies and run tests:

```bash
pip install -e ".[dev]"
pytest
```
