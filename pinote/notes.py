from dataclasses import dataclass
from datetime import datetime

import pinote.applescript as applescript
from pinote.applescript import AppleScriptError  # noqa: F401 — re-exported for callers


@dataclass
class Note:
    id: str
    title: str  # maps to AppleScript "name"
    body: str | None = None  # HTML
    plaintext: str | None = None
    created_at: datetime | None = None  # maps to "creation date"
    updated_at: datetime | None = None  # maps to "modification date"
    folder: str | None = None  # maps to "container"


def list_notes() -> list[Note]:
    raw_notes = applescript.get_all_notes()
    return [Note(id=note["id"], title=note["title"]) for note in raw_notes]


def get_note(note_id: str) -> Note:
    raw = applescript.get_note_by_id(note_id)
    return Note(
        id=raw["id"],
        title=raw["title"],
        body=raw["body"],
        plaintext=raw["plaintext"],
        created_at=raw["created_at"],
        updated_at=raw["updated_at"],
        folder=raw["folder"],
    )


def create_note(title: str, body: str = "", folder: str | None = None) -> Note:
    raw = applescript.create_note(title, body, folder)
    return Note(
        id=raw["id"],
        title=raw["title"],
        body=raw["body"],
        plaintext=raw["plaintext"],
        created_at=raw["created_at"],
        updated_at=raw["updated_at"],
        folder=raw["folder"],
    )


def update_note(note_id: str, title: str | None = None, body: str | None = None) -> None:
    applescript.update_note(note_id, title, body)
