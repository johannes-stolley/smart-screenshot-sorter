from pathlib import Path

from typer.testing import CliRunner
from sss.cli import app
import sss.dedupe as dedupe_module

runner = CliRunner()


def test_dedupe_execute_moves_file(tmp_path, monkeypatch):
    src = tmp_path / "a.jpg"
    dst = tmp_path / "b.jpg"
    src.write_bytes(b"123")

    # plan_moves so faken, dass genau eine Move-Action zurückkommt
    def fake_plan_moves(_dir: Path):
        return [
            dedupe_module.DedupAction(
                action="move",
                src=src,
                dst=dst,
                reason="test-execute",
            )
        ]

    monkeypatch.setattr(dedupe_module, "plan_moves", fake_plan_moves)

    result = runner.invoke(app, ["dedupe", "--execute", str(tmp_path)])

    # CLI darf nicht crashen
    assert result.exit_code == 0

    # Datei muss wirklich verschoben sein
    assert not src.exists()
    assert dst.exists()


def test_dedupe_dry_run_does_not_move_file(tmp_path, monkeypatch):
    src = tmp_path / "a.jpg"
    dst = tmp_path / "b.jpg"
    src.write_bytes(b"123")

    def fake_plan_moves(_dir: Path):
        return [
            dedupe_module.DedupAction(
                action="move",
                src=src,
                dst=dst,
                reason="test",
            )
        ]

    monkeypatch.setattr(dedupe_module, "plan_moves", fake_plan_moves)

    result = runner.invoke(app, ["dedupe", str(tmp_path)])  # kein --execute!

    # CLI darf nicht crashen
    assert result.exit_code == 0

    # Datei darf NICHT verschoben worden sein
    assert src.exists()
    assert not dst.exists()

    # Ausgabe soll erkennbar Dry-Run sein
    assert "Dry-Run" in result.stdout


def test_dedupe_no_duplicates_found(tmp_path, monkeypatch):
    # plan_moves soll eine LEERE Liste zurückgeben
    def fake_plan_moves(_dir):
        return []

    monkeypatch.setattr(dedupe_module, "plan_moves", fake_plan_moves)

    result = runner.invoke(app, ["dedupe", str(tmp_path)])

    # Soll nicht crashen
    assert result.exit_code == 0

    # CLI soll klar sagen, dass es keine Duplikate gibt
    assert "Keine doppelten Dateien gefunden" in result.stdout
