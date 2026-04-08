import json
import subprocess


class AppleScriptError(Exception):
    pass


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _run_script(script: str) -> str:
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        raise AppleScriptError(result.stderr.strip())
    return result.stdout


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
    return json.loads(_run_script(GET_ALL_NOTES_SCRIPT))


def get_note_by_id(note_id: str) -> dict:
    script = f"""
tell application "Notes"
    set n to note id "{_escape(note_id)}"
    set noteId to the id of n
    set noteTitle to name of n
    set noteBody to body of n
    set notePlaintext to plaintext of n
    set noteCreated to creation date of n
    set noteModified to modification date of n
    set noteFolder to name of container of n
    return noteId & "||" & noteTitle & "||" & noteBody & "||" & notePlaintext & "||" & (noteCreated as string) & "||" & (noteModified as string) & "||" & noteFolder
end tell
"""
    output = _run_script(script)
    parts = output.strip().split("||")
    return {
        "id": parts[0],
        "title": parts[1],
        "body": parts[2],
        "plaintext": parts[3],
        "created_at": parts[4],
        "updated_at": parts[5],
        "folder": parts[6],
    }


def create_note(title: str, body: str, folder: str | None = None) -> dict:
    folder_clause = f', default folder folder "{_escape(folder)}"' if folder else ""
    script = f"""
tell application "Notes"
    set n to make new note with properties {{name:"{_escape(title)}", body:"{_escape(body)}"}}{folder_clause}
    return id of n
end tell
"""
    note_id = _run_script(script).strip()
    return get_note_by_id(note_id)


def update_note(note_id: str, title: str | None, body: str | None) -> None:
    lines = [f'set n to note id "{_escape(note_id)}"']
    if title is not None:
        lines.append(f'set name of n to "{_escape(title)}"')
    if body is not None:
        lines.append(f'set body of n to "{_escape(body)}"')
    script = "tell application \"Notes\"\n" + "\n".join(f"    {l}" for l in lines) + "\nend tell"
    _run_script(script)
