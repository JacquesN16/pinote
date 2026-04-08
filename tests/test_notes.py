from unittest.mock import patch

import pytest

from pinote.applescript import AppleScriptError
from pinote.notes import Note, create_note, delete_note, find_notes_by_title, get_note, update_note

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


# --- delete_note ---

def test_delete_note_delegates_to_applescript():
    with patch("pinote.applescript.delete_note") as mock_del:
        delete_note("n1")
    mock_del.assert_called_once_with("n1")


def test_delete_note_propagates_applescript_error():
    with patch("pinote.applescript.delete_note", side_effect=AppleScriptError("gone")):
        with pytest.raises(AppleScriptError):
            delete_note("n1")


# --- find_notes_by_title ---

def test_find_notes_by_title_returns_empty_when_no_match():
    raw = [{"id": "1", "title": "Alpha"}, {"id": "2", "title": "Beta"}]
    with patch("pinote.applescript.get_all_notes", return_value=raw):
        result = find_notes_by_title("Gamma")
    assert result == []


def test_find_notes_by_title_returns_single_match():
    raw = [{"id": "1", "title": "Alpha"}, {"id": "2", "title": "Beta"}]
    with patch("pinote.applescript.get_all_notes", return_value=raw):
        result = find_notes_by_title("Alpha")
    assert len(result) == 1
    assert result[0].id == "1"


def test_find_notes_by_title_returns_multiple_matches():
    raw = [
        {"id": "1", "title": "Same"},
        {"id": "2", "title": "Same"},
        {"id": "3", "title": "Other"},
    ]
    with patch("pinote.applescript.get_all_notes", return_value=raw):
        result = find_notes_by_title("Same")
    assert len(result) == 2
    assert {n.id for n in result} == {"1", "2"}


def test_find_notes_by_title_is_case_sensitive():
    raw = [{"id": "1", "title": "hello"}, {"id": "2", "title": "Hello"}]
    with patch("pinote.applescript.get_all_notes", return_value=raw):
        result = find_notes_by_title("hello")
    assert len(result) == 1
    assert result[0].id == "1"


def test_find_notes_by_title_propagates_applescript_error():
    with patch("pinote.applescript.get_all_notes", side_effect=AppleScriptError("fail")):
        with pytest.raises(AppleScriptError):
            find_notes_by_title("anything")
