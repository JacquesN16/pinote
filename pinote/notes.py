from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    id: str
    title: str  # maps to AppleScript "name"
    body: str | None = None  # HTML
    plaintext: str | None = None
    created_at: datetime | None = None  # maps to "creation date"
    updated_at: datetime | None = None  # maps to "modification date"
    folder: str | None = None  # maps to "container"


def list_notes() -> list[Note]: ...
