from typer.testing import CliRunner

from pinote.cli import app

runner = CliRunner()


def test_app_has_list_command():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0


def test_app_has_read_command():
    result = runner.invoke(app, ["read", "some-id"])
    assert result.exit_code == 0


def test_app_has_create_command():
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0


def test_app_has_update_command():
    result = runner.invoke(app, ["update", "some-id"])
    assert result.exit_code == 0
