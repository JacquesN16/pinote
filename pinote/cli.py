import typer

app = typer.Typer()


@app.command()
def list(): ...


@app.command()
def read(id: str): ...


@app.command()
def create(): ...


@app.command()
def update(id: str): ...
