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

Update the title and/or body of an existing note. Both flags are optional — omit either to leave it unchanged.

```bash
pinote update <note-id> [--title <title>] [--body <body>]
```

Examples:
```bash
pinote update "x-coredata://abc123/..." --title "New Title"
pinote update "x-coredata://abc123/..." --body "New content."
pinote update "x-coredata://abc123/..." --title "New Title" --body "New content."
```

### show

Browse all notes interactively. Use ↑/↓ to navigate, Enter to open a note in your `$EDITOR`, and `q` or Ctrl+C to quit.

```bash
pinote show
```

When a note opens in the editor, the first line is the title and the rest is the body. Save and quit the editor to write the changes back to Notes. If nothing changed, no update is made.

### delete

Delete a note by ID or by exact title.

```bash
pinote delete --id <note-id>
pinote delete --name <title>
```

Examples:
```bash
pinote delete --id "x-coredata://abc123/..."
pinote delete --name "Shopping list"
```

If multiple notes share the same title, the command will list their IDs and ask you to use `--id` to disambiguate.

## Development

Install dev dependencies and run tests:

```bash
pip install -e ".[dev]"
pytest
```
