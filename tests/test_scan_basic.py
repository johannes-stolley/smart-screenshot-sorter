# tests/test_scan_basic.py
import os
from pathlib import Path
from datetime import datetime
import sys

# Repo-Root/src auf den Modulpfad legen (damit "from sss..." funktioniert)
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from typer.testing import CliRunner  # type: ignore
from sss.cli import app              # jetzt importierbar

runner = CliRunner()


def _make_fake_png(path: Path, ts: datetime) -> None:
    # Minimaler PNG-Header reicht als Dummy-Datei
    path.write_bytes(b"\x89PNG\r\n\x1a\n")
    epoch = ts.timestamp()
    os.utime(path, (epoch, epoch))  # atime, mtime setzen


def test_scan_creates_year_month_dirs(tmp_path: Path):
    src = tmp_path / "in"
    out = tmp_path / "out"
    src.mkdir()

    ts = datetime(2024, 7, 5, 12, 34, 56)
    f = src / "shot.png"
    _make_fake_png(f, ts)

    # CLI ausführen: realer Move, mit out-dir
    result = runner.invoke(
        app,
        ["scan", str(src), "--no-dry-run", "--out-dir", str(out)],
    )

    assert result.exit_code == 0, result.output

    # Erwarteter Zielordner: YYYY/MM
    target_dir = out / "2024" / "07"
    assert (target_dir / "shot.png").exists()



def test_scan_handles_duplicates(tmp_path: Path):
    src = tmp_path / "in"
    out = tmp_path / "out"
    src.mkdir()

    ts = datetime(2024, 7, 5, 12, 34, 56)
    f = src / "shot.png"

    # 1. Erste Datei erstellen und verschieben
    _make_fake_png(f, ts)
    result = runner.invoke(app, ["scan", str(src), "--no-dry-run", "--out-dir", str(out)])
    assert result.exit_code == 0, result.output

    # 2. Zweite Datei mit gleichem Namen erstellen und nochmal verschieben
    _make_fake_png(f, ts)
    result = runner.invoke(app, ["scan", str(src), "--no-dry-run", "--out-dir", str(out)])
    assert result.exit_code == 0, result.output

    # 3. Ergebnis prüfen
    target_dir = out / "2024" / "07"
    files = sorted(p.name for p in target_dir.iterdir())
    print("Dateien im Ziel:", files)

    # Erwartung: shot.png und shot (1).png existieren beide
    assert "shot.png" in files
    assert "shot (1).png" in files
