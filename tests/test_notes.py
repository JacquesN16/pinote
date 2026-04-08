from unittest.mock import patch

import pytest

from pinote.applescript import AppleScriptError
from pinote.notes import Note, create_note, get_note, update_note

FULL_RAW = {
    "id": "n1",
    "title": "T",
    "body": "<p/>",
    "plaintext": "T",
    "created_at": "2024-01-01",
    "updated_at": "2024-01-01",
    "folder": "Notes",
}


# --- Note dataclass ---

def test_note_dataclass_required_fields():
    note = Note(id="1", title="Test")
    assert note.id == "1"
    assert note.title == "Test"


def test_note_dataclass_optional_fields_default_none():
    note = Note(id="1", title="Test")
    assert note.body is None
    assert note.plaintext is None
    assert note.created_at is None
    assert note.updated_at is None
    assert note.folder is None


def test_note_dataclass_with_all_fields():
    from datetime import datetime

    dt = datetime(2024, 1, 15)
    note = Note(
        id="abc",
        title="My Note",
        body="<p>Hello</p>",
        plaintext="Hello",
        created_at=dt,
        updated_at=dt,
        folder="Work",
    )
    assert note.body == "<p>Hello</p>"
    assert note.folder == "Work"
    assert note.created_at == dt


# --- create_note ---

def test_create_note_returns_full_note():
    with patch("pinote.applescript.create_note", return_value=FULL_RAW):
        note = create_note("T", "<p/>")
    assert note.body == "<p/>"
    assert note.folder == "Notes"
    assert note.plaintext == "T"
    assert note.created_at == "2024-01-01"


def test_create_note_propagates_applescript_error():
    with patch("pinote.applescript.create_note", side_effect=AppleScriptError("fail")):
        with pytest.raises(AppleScriptError):
            create_note("T", "B")


# --- get_note ---

def test_get_note_returns_folder():
    with patch("pinote.applescript.get_note_by_id", return_value=FULL_RAW):
        note = get_note("n1")
    assert note.folder == "Notes"


# --- update_note ---

def test_update_note_passes_none_title():
    with patch("pinote.applescript.update_note") as mock_upd:
        update_note("n1", None, "new body")
    mock_upd.assert_called_once_with("n1", None, "new body")


def test_update_note_passes_none_body():
    with patch("pinote.applescript.update_note") as mock_upd:
        update_note("n1", "new title", None)
    mock_upd.assert_called_once_with("n1", "new title", None)
