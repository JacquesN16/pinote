import typer

from pinote.notes import list_notes, get_note

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
def create(): ...


@app.command()
def update(id: str): ...
