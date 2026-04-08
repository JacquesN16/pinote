from unittest.mock import patch

from typer.testing import CliRunner

from pinote.applescript import AppleScriptError
from pinote.cli import app

runner = CliRunner()

FULL_RAW = {
    "id": "some-id",
    "title": "Test",
    "body": "<p/>",
    "plaintext": "",
    "created_at": "",
    "updated_at": "",
    "folder": "Notes",
}


def test_app_has_list_command():
    with patch("pinote.applescript.get_all_notes", return_value=[]):
        result = runner.invoke(app, ["list"])
    assert result.exit_code == 0


def test_app_has_read_command():
    with patch("pinote.applescript.get_note_by_id", return_value=FULL_RAW):
        result = runner.invoke(app, ["read", "some-id"])
    assert result.exit_code == 0


def test_app_has_create_command():
    with patch("pinote.applescript.create_note", return_value=FULL_RAW):
        result = runner.invoke(app, ["create", "My Note"])
    assert result.exit_code == 0


def test_app_has_update_command():
    with patch("pinote.applescript.update_note", return_value=None):
        result = runner.invoke(app, ["update", "some-id", "--title", "New Title", "--body", "New Body"])
    assert result.exit_code == 0


# --- error exit codes ---

def test_list_exits_1_on_applescript_error():
    with patch("pinote.applescript.get_all_notes", side_effect=AppleScriptError("Notes not running")):
        result = runner.invoke(app, ["list"])
    assert result.exit_code == 1


def test_read_exits_1_on_applescript_error():
    with patch("pinote.applescript.get_note_by_id", side_effect=AppleScriptError("not found")):
        result = runner.invoke(app, ["read", "bad-id"])
    assert result.exit_code == 1


def test_create_exits_1_on_applescript_error():
    with patch("pinote.applescript.create_note", side_effect=AppleScriptError("fail")):
        result = runner.invoke(app, ["create", "Title"])
    assert result.exit_code == 1


def test_update_exits_1_on_applescript_error():
    with patch("pinote.applescript.update_note", side_effect=AppleScriptError("fail")):
        result = runner.invoke(app, ["update", "some-id", "--title", "T"])
    assert result.exit_code == 1


# --- partial update ---

def test_update_with_only_title():
    with patch("pinote.applescript.update_note") as mock_upd:
        result = runner.invoke(app, ["update", "some-id", "--title", "New Title"])
    assert result.exit_code == 0
    mock_upd.assert_called_once_with("some-id", "New Title", None)


def test_update_with_only_body():
    with patch("pinote.applescript.update_note") as mock_upd:
        result = runner.invoke(app, ["update", "some-id", "--body", "New Body"])
    assert result.exit_code == 0
    mock_upd.assert_called_once_with("some-id", None, "New Body")
