import typer

from pinote.notes import create_note, get_note, list_notes, update_note

app = typer.Typer()


@app.command()
def list():
    notes = list_notes()
    for note in notes:
        typer.echo(f"{note.id} - {note.title}")


if __name__ == "__main__":
    app()


@app.command()
def read(note_id: str):
    note = get_note(note_id)
    typer.echo(f"Title: {note.title}")
    typer.echo(f"Body: {note.plaintext}")


@app.command()
def create(title: str, body: str = ""):
    note = create_note(title, body)
    typer.echo(f"{note.id} - {note.title}")


@app.command()
def update(note_id: str, title: str, body: str):
    update_note(note_id, title, body)
    typer.echo("Updated.")
