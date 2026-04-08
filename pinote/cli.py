import os
import subprocess
import tempfile

import typer
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl

import pinote.notes as notes
from pinote.applescript import AppleScriptError

app = typer.Typer()


@app.command()
def list():
    try:
        all_notes = notes.list_notes()
        for note in all_notes:
            typer.echo(f"{note.id} - {note.title}")
    except AppleScriptError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def read(note_id: str):
    try:
        note = notes.get_note(note_id)
        typer.echo(f"Title: {note.title}")
        typer.echo(f"Body: {note.plaintext}")
    except AppleScriptError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def create(
    title: str,
    body: str = "",
    folder: str = typer.Option(None, "--folder"),
):
    try:
        note = notes.create_note(title, body, folder)
        typer.echo(f"{note.id} - {note.title}")
    except AppleScriptError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def update(
    note_id: str,
    title: str = typer.Option(None, "--title"),
    body: str = typer.Option(None, "--body"),
):
    try:
        notes.update_note(note_id, title, body)
        typer.echo("Updated.")
    except AppleScriptError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def show():
    try:
        all_notes = notes.list_notes()
    except AppleScriptError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    if not all_notes:
        typer.echo("No notes found.")
        return

    selected_index = [0]

    while True:
        quit_app = [False]

        def get_text():
            lines = []
            for i, note in enumerate(all_notes):
                if i == selected_index[0]:
                    lines.append(("reverse", f"> {note.title}\n"))
                else:
                    lines.append(("", f"  {note.title}\n"))
            lines.append(("", "\n  ↑/↓ navigate  Enter: open  q: quit"))
            return lines

        kb = KeyBindings()

        @kb.add("up")
        def _up(event):
            selected_index[0] = max(0, selected_index[0] - 1)

        @kb.add("down")
        def _down(event):
            selected_index[0] = min(len(all_notes) - 1, selected_index[0] + 1)

        @kb.add("enter")
        def _enter(event):
            event.app.exit()

        @kb.add("q")
        @kb.add("c-c")
        def _quit(event):
            quit_app[0] = True
            event.app.exit()

        picker = Application(
            layout=Layout(Window(content=FormattedTextControl(get_text, focusable=True))),
            key_bindings=kb,
            full_screen=True,
        )
        picker.run()

        if quit_app[0]:
            break

        note = all_notes[selected_index[0]]

        try:
            full_note = notes.get_note(note.id)
        except AppleScriptError as e:
            typer.echo(f"Error fetching note: {e}", err=True)
            continue

        content = f"{full_note.title}\n\n{full_note.plaintext or ''}"

        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
        try:
            tmp.write(content)
            tmp.flush()
            tmp.close()
            editor = os.environ.get("EDITOR", "nano")
            subprocess.call([editor, tmp.name])
            with open(tmp.name, encoding="utf-8") as f:
                new_content = f.read()
        finally:
            os.unlink(tmp.name)

        if new_content == content:
            continue

        new_lines = new_content.splitlines()
        new_title = new_lines[0].strip() if new_lines else ""
        if not new_title:
            typer.echo("Title is empty — skipping save.", err=True)
            continue

        new_body = "\n".join(new_lines[2:]) if len(new_lines) > 2 else ""

        try:
            notes.update_note(full_note.id, new_title, new_body)
            all_notes[selected_index[0]] = notes.Note(id=full_note.id, title=new_title)
        except AppleScriptError as e:
            typer.echo(f"Error saving note: {e}", err=True)


@app.command()
def delete(
    note_id: str = typer.Option(None, "--id", help="Delete note by ID"),
    name: str = typer.Option(None, "--name", help="Delete note by exact title"),
):
    if (note_id is None) == (name is None):
        typer.echo("Error: provide exactly one of --id or --name.", err=True)
        raise typer.Exit(code=1)

    try:
        if note_id is not None:
            notes.delete_note(note_id)
            typer.echo("Deleted.")
        else:
            matches = notes.find_notes_by_title(name)
            if len(matches) == 0:
                typer.echo(f"Error: no note found with title '{name}'.", err=True)
                raise typer.Exit(code=1)
            elif len(matches) > 1:
                typer.echo(
                    f"Error: {len(matches)} notes found with title '{name}'. "
                    "Use --id to disambiguate:",
                    err=True,
                )
                for m in matches:
                    typer.echo(f"  {m.id} - {m.title}", err=True)
                raise typer.Exit(code=1)
            else:
                notes.delete_note(matches[0].id)
                typer.echo("Deleted.")
    except AppleScriptError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
