from unittest.mock import patch

from typer.testing import CliRunner

from pinote.cli import app

runner = CliRunner()


def test_app_has_list_command():
    with patch("pinote.notes.get_all_notes", return_value=[]):
        result = runner.invoke(app, ["list"])
    assert result.exit_code == 0


def test_app_has_read_command():
    fake_note = {
        "id": "some-id",
        "title": "Test",
        "body": "",
        "plaintext": "",
        "created_at": "",
        "updated_at": "",
    }
    with patch("pinote.notes.get_note_by_id", return_value=fake_note):
        result = runner.invoke(app, ["read", "some-id"])
    assert result.exit_code == 0


def test_app_has_create_command():
    fake_note = {"id": "new-id", "title": "My Note"}
    with patch("pinote.notes.applescript_create", return_value=fake_note):
        result = runner.invoke(app, ["create", "My Note"])
    assert result.exit_code == 0


def test_app_has_update_command():
    with patch("pinote.notes.applescript_update", return_value=None):
        result = runner.invoke(app, ["update", "some-id", "New Title", "New Body"])
    assert result.exit_code == 0
