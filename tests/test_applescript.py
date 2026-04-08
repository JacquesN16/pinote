import json
from unittest.mock import MagicMock, patch

import pytest

from pinote.applescript import (
    AppleScriptError,
    _escape,
    create_note,
    get_all_notes,
    get_note_by_id,
    update_note,
)


def make_run_result(stdout: str = "", returncode: int = 0, stderr: str = "") -> MagicMock:
    result = MagicMock()
    result.stdout = stdout
    result.returncode = returncode
    result.stderr = stderr
    return result


FULL_NOTE_STDOUT = "id1||title||<p/>||plain||2024-01-01||2024-01-01||Notes"


# --- existing get_all_notes tests ---

def test_get_all_notes_returns_list():
    data = [{"id": "x1", "title": "Note A"}, {"id": "x2", "title": "Note B"}]
    with patch("subprocess.run", return_value=make_run_result(json.dumps(data))):
        notes = get_all_notes()
    assert notes == data


def test_get_all_notes_empty():
    with patch("subprocess.run", return_value=make_run_result(json.dumps([]))):
        notes = get_all_notes()
    assert notes == []


def test_get_all_notes_single():
    data = [{"id": "abc", "title": "Hello"}]
    with patch("subprocess.run", return_value=make_run_result(json.dumps(data))):
        notes = get_all_notes()
    assert len(notes) == 1
    assert notes[0]["title"] == "Hello"


def test_get_all_notes_calls_osascript():
    with patch("subprocess.run", return_value=make_run_result(json.dumps([]))) as mock_run:
        get_all_notes()
    args = mock_run.call_args[0][0]
    assert args[0] == "osascript"


# --- _escape tests ---

def test_escape_double_quotes():
    assert _escape('say "hello"') == 'say \\"hello\\"'


def test_escape_backslash():
    assert _escape("path\\to") == "path\\\\to"


def test_escape_both():
    assert _escape('\\"') == '\\\\\\"'


def test_escape_plain_string_unchanged():
    assert _escape("hello world") == "hello world"


# --- AppleScriptError on non-zero returncode ---

def test_get_all_notes_raises_on_error():
    with patch("subprocess.run", return_value=make_run_result(returncode=1, stderr="error")):
        with pytest.raises(AppleScriptError):
            get_all_notes()


def test_get_note_by_id_raises_on_error():
    with patch("subprocess.run", return_value=make_run_result(returncode=1, stderr="not found")):
        with pytest.raises(AppleScriptError):
            get_note_by_id("bad-id")


def test_create_note_raises_on_error():
    with patch("subprocess.run", return_value=make_run_result(returncode=1, stderr="fail")):
        with pytest.raises(AppleScriptError):
            create_note("title", "body")


def test_update_note_raises_on_error():
    with patch("subprocess.run", return_value=make_run_result(returncode=1, stderr="fail")):
        with pytest.raises(AppleScriptError):
            update_note("bad-id", "title", "body")


# --- injection safety ---

def test_get_note_by_id_escapes_id():
    with patch("subprocess.run", return_value=make_run_result(FULL_NOTE_STDOUT)) as mock_run:
        get_note_by_id('x"1')
    script = mock_run.call_args[0][0][2]
    assert '"x"' not in script
    assert '\\"' in script


def test_create_note_escapes_title_and_body():
    with patch("subprocess.run", side_effect=[
        make_run_result("new-id"),
        make_run_result(FULL_NOTE_STDOUT),
    ]) as mock_run:
        create_note('My "Note"', 'body "here"')
    first_script = mock_run.call_args_list[0][0][0][2]
    assert '\\"' in first_script


def test_update_note_escapes_inputs():
    with patch("subprocess.run", return_value=make_run_result("")) as mock_run:
        update_note('id"1', 'ti"tle', 'bo"dy')
    script = mock_run.call_args[0][0][2]
    assert '\\"' in script


# --- optional update fields ---

def test_update_note_skips_title_when_none():
    with patch("subprocess.run", return_value=make_run_result("")) as mock_run:
        update_note("some-id", None, "new body")
    script = mock_run.call_args[0][0][2]
    assert "set name" not in script
    assert "set body" in script


def test_update_note_skips_body_when_none():
    with patch("subprocess.run", return_value=make_run_result("")) as mock_run:
        update_note("some-id", "new title", None)
    script = mock_run.call_args[0][0][2]
    assert "set body" not in script
    assert "set name" in script


# --- folder field ---

def test_get_note_by_id_returns_folder():
    raw = "id1||title||<html/>||plain||2024-01-01||2024-01-01||Work"
    with patch("subprocess.run", return_value=make_run_result(raw)):
        note = get_note_by_id("id1")
    assert note["folder"] == "Work"
