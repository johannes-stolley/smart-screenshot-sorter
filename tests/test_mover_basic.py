import pytest
from pathlib import Path
from sss.dedupe import DedupAction
from sss.mover import execute_actions


def test_execute_actions_moves_file(tmp_path: Path):
    # Ordnerstruktur für den Test
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    # Quelldatei anlegen
    src_file = src_dir / "a.txt"
    content = b"HELLO\n"
    src_file.write_bytes(content)

    # Zielpfad definieren
    dst_file = dst_dir / "a.txt"

    # Eine DedupAction vorbereiten
    action = DedupAction(
        src=src_file,
        action="move",
        dst=dst_file,
        reason="test move",
    )

    # Aktion ausführen
    execute_actions([action])

    # Quelle soll weg sein, Ziel soll existieren
    assert not src_file.exists()
    assert dst_file.exists()
    assert dst_file.read_bytes() == content


def test_execute_actions_moves_multiple_files(tmp_path: Path):
    # src/ und dst/ Ordner
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    # Zwei Quelldateien
    src_file1 = src_dir / "a.txt"
    src_file2 = src_dir / "b.txt"
    content1 = b"FILE A\n"
    content2 = b"FILE B\n"
    src_file1.write_bytes(content1)
    src_file2.write_bytes(content2)

    # Zielpfade
    dst_file1 = dst_dir / "a.txt"
    dst_file2 = dst_dir / "b.txt"

    # Zwei Aktionen vorbereiten
    actions = [
        DedupAction(
            src=src_file1,
            action="move",
            dst=dst_file1,
            reason="move a",
        ),
        DedupAction(
            src=src_file2,
            action="move",
            dst=dst_file2,
            reason="move b",
        ),
    ]

    # Alle Aktionen auf einmal ausführen
    execute_actions(actions)

    # Beide Quellen weg
    assert not src_file1.exists()
    assert not src_file2.exists()

    # Beide Ziele da, mit korrektem Inhalt
    assert dst_file1.exists()
    assert dst_file1.read_bytes() == content1

    assert dst_file2.exists()
    assert dst_file2.read_bytes() == content2


def test_execute_actions_raises_on_unsupported_action(tmp_path: Path):
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    src_file = src_dir / "a.txt"
    src_file.write_text("TEST")

    dst_file = dst_dir / "a.txt"

    # absichtlich falsche Action
    action = DedupAction(
        src=src_file,
        action="delete",  # <- wird NICHT unterstützt
        dst=dst_file,
        reason="invalid",
    )

    with pytest.raises(ValueError) as excinfo:
        execute_actions([action])

    # Optionale Zusatzprüfung: Fehlermeldung enthält das Wort "Unsupported"
    assert "Unsupported action" in str(excinfo.value)
