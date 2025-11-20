from pathlib import Path
from datetime import datetime

import typer

from .mover import build_target_path, safe_move
from .summary import Summary
import sss.dedupe as dedupe_module


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
    out_dir: Path = typer.Option(
        None, "--out-dir", help="Zielbasis (default: <path>/_by_date)"
    ),
    dry_run: bool = typer.Option(
        True, "--dry-run/--no-dry-run", help="Nur simulieren, nichts verschieben"
    ),
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

    sorted_screenshots = sorted(
        screenshots, key=lambda p: p.stat().st_mtime, reverse=True
    )

    summary = Summary(out_root=out_root)

    typer.echo("Gefundene Screenshots:")
    for file_path in sorted_screenshots:
        dest_dir = build_target_path(file_path, out_root)
        mtime = file_path.stat().st_mtime
        change_time = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M:%S")
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        typer.echo(
            f"PLAN: {file_path.name} -> {dest_dir}  ({file_size_mb:.2f} MB, {change_time})"
        )

        if not dry_run:
            dest_dir = build_target_path(file_path, out_root)
            safe_move(file_path, dest_dir)
            summary.inc_moved()
            typer.echo(f"✓ Verschoben: {file_path.name} -> {dest_dir}")
        else:
            summary.inc_simulated()
            typer.echo(f"✈ Simulation: {file_path.name} -> {dest_dir}")

    typer.echo("\n" + summary.render())


if __name__ == "__main__":
    import sys

    sys.exit(app())


@app.command()
def dedupe(
    directory: Path,
    execute: bool = typer.Option(
        False,
        "--execute",
        help="Aktionen wirklich ausführen statt nur Dry-Run.",
    ),
) -> None:
    """Findet Duplikate und zeigt einen Dry-Run oder führt die Aktionen aus."""

    actions = dedupe_module.plan_moves(directory)

    if not actions:
        typer.echo("Keine doppelten Dateien gefunden.")
        raise typer.Exit(code=0)

    if not execute:
        # wie bisher: nur anzeigen
        typer.echo(f"Dry-Run: {len(actions)} geplante Aktionen")
        for act in actions:
            # act ist DedupAction
            typer.echo(f"{act.action.upper()} {act.src} -> {act.dst}")
        raise typer.Exit(code=0)

    # == execute == True ==
    summary = Summary(out_root=directory)
    dedupe_module.execute_actions(actions, summary)

    # einfache Erfolgsmeldung – Detailformat kannst du später hübscher machen
    typer.echo("Ausführung abgeschlossen.")
    typer.echo(str(summary))
