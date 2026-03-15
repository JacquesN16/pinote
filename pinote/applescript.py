import json
import subprocess

GET_ALL_NOTES_SCRIPT = """
tell application "Notes"
    set output to "["
    set allNotes to every note 
    repeat with i from 1 to count of allNotes
        set n to item i of allNotes
        set noteId to id of n
        set noteTitle to name of n
        set output to output & "{\\"id\\":\\"" & noteId & "\\",\\"title\\":\\"" & noteTitle & "\\"}"
        if i < count of allNotes then set output to output & ","
    end repeat
    set output to output & "]"
    return output
end tell
"""


def get_all_notes() -> list[dict]:
    # fetch all notes from Apple notes
    result = subprocess.run(
        ["osascript", "-e", GET_ALL_NOTES_SCRIPT], capture_output=True, text=True
    )
    print(result.stdout)
    return json.loads(result.stdout)


def get_note_by_id(id: str) -> dict: ...  # fetch one notes
def create_note(title: str, body: str) -> dict: ...  # create new notes
def update_note(id: str, title: str, body: str) -> None: ...  # update existing note
