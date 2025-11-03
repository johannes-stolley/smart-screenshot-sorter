from pathlib import Path
import typer 
import os
from datetime import datetime
import shutil
from .mover import build_target_path, safe_move
from sss.summary import Summary





app = typer.Typer(no_args_is_help=True)

@app.callback()
def main():
    pass


@app.command()
def hello(name: str = "Freund"):
    """Begrüßt den Benutzer mit seinem Namen."""
    typer.echo(f"Hallo, {name}!")


@app.command()
def scan(
    path: Path,
    out_dir: Path = typer.Option(None, "--out-dir", help="Zielbasis (default: <path>/_by_date)"),
    dry_run: bool = typer.Option(True, "--dry-run/--no-dry-run", help="Nur simulieren, nichts verschieben"),
):
    in_root = Path(path)

    if not in_root.exists():
        typer.echo("Der Pfad wurde nicht gefunden")
        raise typer.Exit(code=1)

    out_root = out_dir or (in_root / "_by_date")
    typer.echo(f"📁 Zielbasis: {out_root}")

    files = [f for f in in_root.iterdir() if f.is_file()]
    image_extensions = (".png", ".jpg", ".jpeg")

    screenshots = [f for f in files if f.suffix.lower() in image_extensions]

    if not screenshots:
        typer.echo("Keine Screenshots gefunden.")
        raise typer.Exit(code=0)


    sorted_screenshots = sorted(screenshots, key = lambda p: p.stat().st_mtime, reverse=True)
    moved = 0
    simulated = 0
    total = len(sorted_screenshots)


    typer.echo("Gefundene Screenshots:")
    for file_path in sorted_screenshots:
        dest_dir = build_target_path(file_path, out_root)
        mtime = file_path.stat().st_mtime
        change_time = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M:%S")
        file_size = file_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)   
        typer.echo(f"PLAN: {file_path}  ->  {dest_dir}")

        if dry_run:
            typer.echo(f"🟡 Simulation: {file_path.name} → {dest_dir}")
            simulated += 1
        else:
            final_path = safe_move(file_path, dest_dir)
            typer.echo(f"🟢 Verschoben: {file_path.name} → {final_path}")
            moved += 1

    typer.echo(
        f"\n✅ Zusammenfassung: gesamt={total} | verschoben={moved} | simuliert={simulated} | zielbasis={out_root}"
    )



if __name__ == "__main__":
    app() 



   # python -m src.sss.cli scan C:\Users\stoll\Downloads
