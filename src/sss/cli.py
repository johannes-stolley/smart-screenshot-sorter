import typer 
import os
from datetime import datetime


app = typer.Typer(no_args_is_help=True)

@app.callback()
def main():
    pass


@app.command()
def hello(name: str = "Freund"):
    """Begrüßt den Benutzer mit seinem Namen."""
    typer.echo(f"Hallo, {name}!")

@app.command()
def scan(path: str):
    typer.echo(f"Scanne Ordner: {path}")

    if not os.path.exists(path):
        typer.echo("Der Pfad wurde nicht gefunden")
        raise typer.Exit(code=1)

    files = os.listdir(path)
    image_extensions = (".png", ".jpg", ".jpeg")

    screenshots = [f for f in files if f.lower().endswith(image_extensions)]

    if not screenshots:
        typer.echo("Keine Screenshots gefunden.")
        raise typer.Exit(code=0)


    sorted_screenshots = sorted(screenshots, key = lambda f: os.path.getmtime(os.path.join(path, f))
, reverse=True)



    typer.echo("Gefundene Screenshots:")
    for f in sorted_screenshots:
        file_path = os.path.join(path, f)
        mtime = os.path.getmtime(file_path)
        change_time = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M:%S")
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)   
        typer.echo(f" - {f} - {file_size_mb:.2f} MB - {change_time}")


if __name__ == "__main__":
    app() 



   # python -m src.sss.cli scan C:\Users\stoll\Downloads
