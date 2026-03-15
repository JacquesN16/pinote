import typer

from pinote.notes import list_notes

app = typer.Typer()


@app.command()
def list():
    notes = list_notes()
    for note in notes:
        typer.echo(f"{note.id} - {note.title}")
if __name__ == "__main__":
    app()

@app.command()
def read(id: str): ...


@app.command()
def create(): ...


@app.command()
def update(id: str): ...
