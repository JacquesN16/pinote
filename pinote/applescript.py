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


def get_note_by_id(note_id: str) -> dict:
    # fetch one notes
    script = f"""
tell application "Notes"
    set n to note id "{note_id}"
    set noteId to the id of n 
    set noteTitle to name of n
    set noteBody to body of n
    set notePlaintext to plaintext of n
    set noteCreated to creation date of n
    set noteModified to modification date of n
    return noteId & "||" & noteTitle & "||" & noteBody & "||" & notePlaintext & "||" & (noteCreated as string) & "||" & (noteModified as string)
end tell
"""
    result = subprocess.run(
        ["osascript", "-e", script], capture_output=True, text=True
    )
    parts = result.stdout.strip().split("||")
    return {
        "id" : parts[0],
        "title": parts[1],
        "body": parts[2],
        "plaintext": parts[3],
        "created_at": parts[4],
        "updated_at": parts[5],
    }



def create_note(title: str, body: str) -> dict: ...  # create new notes
def update_note(id: str, title: str, body: str) -> None: ...  # update existing note
