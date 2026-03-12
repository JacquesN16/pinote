def get_all_notes() -> list[dict]: ... # fetch all notes from Apple notes
def get_note_by_id(id: str) -> dict: ... # fetch one notes
def create_note(title: str, body: str) -> dict #create new notes
def update_note(id: str, title: str, body: str) -> None: ... #update existing note
