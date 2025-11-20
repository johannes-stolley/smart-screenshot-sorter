from typer.testing import CliRunner
from sss.cli import app
import sss.dedupe as dedupe_module

runner = CliRunner()

def test_dedupe_dry_run(tmp_path, monkeypatch):
    f1 = tmp_path / "a.jpg"
    f2 = tmp_path / "b.jpg"
    f1.write_bytes(b"123")
    f2.write_bytes(b"123")

    def fake_plan_moves(_dir):
        return [
            dedupe_module.DedupAction(
                action="move",
                src=f1,
                dst=f2,
                reason="test-dry-run",
            )
        ]

    monkeypatch.setattr(dedupe_module, "plan_moves", fake_plan_moves)

    result = runner.invoke(app, ["dedupe", str(tmp_path)])

    assert result.exit_code == 0
    assert "Dry-Run" in result.stdout
    assert "a.jpg" in result.stdout
    assert "b.jpg" in result.stdout
