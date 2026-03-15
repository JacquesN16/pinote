from pinote.notes import Note


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
