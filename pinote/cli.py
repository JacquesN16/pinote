import typer

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


if __name__ == "__main__":
    app()
