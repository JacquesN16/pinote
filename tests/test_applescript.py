import json
from unittest.mock import MagicMock, patch

from pinote.applescript import get_all_notes


def make_run_result(data: list) -> MagicMock:
    result = MagicMock()
    result.stdout = json.dumps(data)
    return result


def test_get_all_notes_returns_list():
    data = [{"id": "x1", "title": "Note A"}, {"id": "x2", "title": "Note B"}]
    with patch("subprocess.run", return_value=make_run_result(data)):
        notes = get_all_notes()
    assert notes == data


def test_get_all_notes_empty():
    with patch("subprocess.run", return_value=make_run_result([])):
        notes = get_all_notes()
    assert notes == []


def test_get_all_notes_single():
    data = [{"id": "abc", "title": "Hello"}]
    with patch("subprocess.run", return_value=make_run_result(data)):
        notes = get_all_notes()
    assert len(notes) == 1
    assert notes[0]["title"] == "Hello"


def test_get_all_notes_calls_osascript():
    with patch("subprocess.run", return_value=make_run_result([])) as mock_run:
        get_all_notes()
    args = mock_run.call_args[0][0]
    assert args[0] == "osascript"
