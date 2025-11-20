from typer.testing import CliRunner
from sss.cli import app

runner = CliRunner()

def test_dedupe_dry_run(tmp_path, monkeypatch):
    # 1) Fake-Dateien erstellen
    f1 = tmp_path / "a.jpg"
    f2 = tmp_path / "b.jpg"
    f1.write_bytes(b"123")
    f2.write_bytes(b"123")  # absichtlich identisch -> Duplikat

    # 2) Pipeline mocken, damit wir keine echten Moves planen müssen
    def fake_plan_moves(_):
        return [("MOVE", str(f1), str(f2))]

    import sss.dedupe
    monkeypatch.setattr(sss.dedupe, "plan_moves", fake_plan_moves)

    # 3) CLI aufrufen
    result = runner.invoke(app, ["dedupe", str(tmp_path)])

    # 4) Erwartung: Exit-Code 0 + Dry-Run-Ausgabe
    assert result.exit_code == 0
    assert "Dry-Run" in result.stdout
    assert "MOVE" in result.stdout
    assert "a.jpg" in result.stdout
    assert "b.jpg" in result.stdout
