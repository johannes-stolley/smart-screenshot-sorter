import os
import time
from pathlib import Path
from sss.dedupe import (
    compute_sha256,
    find_duplicate_groups,
    DuplicateGroup,
    choose_keeper,
    plan_moves,
    DedupAction,
)
from sss.mover import execute_actions


def test_compute_sha256_stable_and_chunked(tmp_path: Path):
    # zwei kleine, inhaltsgleiche Dateien
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    content = b"hello world\n"
    f1.write_bytes(content)
    f2.write_bytes(content)

    d1 = compute_sha256(f1)
    d2 = compute_sha256(f2)

    assert d1 == d2
    assert len(d1) == 64
    assert all(c in "0123456789abcdef" for c in d1)

    # eine größere Datei und Chunk-Unabhängigkeit prüfen
    big = tmp_path / "big.bin"
    big.write_bytes(b"xyz" * (1024 * 1024))  # ~3 MB

    d_default = compute_sha256(big)  # Standard-Chunk
    d_tiny = compute_sha256(big, chunk_size=8)  # winzige Chunks

    assert d_default == d_tiny


def test_find_duplicate_groups_basic(tmp_path: Path):
    # Arrange: 3 Dateien, davon 2 identisch
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    c = tmp_path / "c.txt"

    content_dup = b"hello world\n"
    a.write_bytes(content_dup)
    b.write_bytes(content_dup)
    c.write_bytes(b"something else\n")  # anderer Inhalt

    groups = find_duplicate_groups([a, b, c])

    # Es soll genau eine Gruppe geben
    assert isinstance(groups, list)
    assert len(groups) == 1

    g = groups[0]
    assert isinstance(g, DuplicateGroup)

    # Größe prüfen
    assert g.size == len(content_dup)

    # Digest prüfen (64 hex)
    assert isinstance(g.digest, str) and len(g.digest) == 64
    assert all(ch in "0123456789abcdef" for ch in g.digest)

    # Enthaltene Dateien prüfen (Reihenfolge egal)
    assert set(map(Path, g.files)) == {a, b}


def test_choose_keeper_newest(tmp_path: Path):
    # Zwei identische Dateien anlegen
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    content = b"HELLO\n"
    a.write_bytes(content)
    b.write_bytes(content)

    # Unterschiedliche mtime setzen (a älter, b neuer)
    now = time.time()
    os.utime(a, (now - 200, now - 200))  # atime, mtime
    os.utime(b, (now - 100, now - 100))  # b ist neuer

    # DuplicateGroup aufbauen (size + digest identisch)
    digest = compute_sha256(a)
    group = DuplicateGroup(size=len(content), digest=digest, files=[a, b])

    # Prüfen: Policy "newest" wählt b
    keep = choose_keeper(group, policy="newest")
    assert keep == b

    # Optional: Default-Policy ist ebenfalls "newest"
    keep_default = choose_keeper(group)
    assert keep_default == b


def test_plan_moves_layout(tmp_path: Path):
    # Arrange: zwei identische Dateien
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    content = b"DATA\n"
    a.write_bytes(content)
    b.write_bytes(content)

    digest = compute_sha256(a)
    group = DuplicateGroup(size=len(content), digest=digest, files=[a, b])

    # Keeper bestimmen (b soll neuer sein)
    b.write_bytes(content + b"!")  # kurz ändern, um mtime anzuheben
    b.write_bytes(content)  # Inhalt zurücksetzen, Hash bleibt gleich
    keeper = choose_keeper(group, policy="newest")
    assert keeper in {a, b}  # sanity check

    target_dir = tmp_path / "duplicates"
    actions = plan_moves(group, keeper, target_dir=target_dir)

    # Es gibt genau eine Aktion (die Nicht-Keeper-Datei)
    assert isinstance(actions, list)
    assert len(actions) == 1

    act = actions[0]
    assert isinstance(act, DedupAction)
    assert act.action == "move"
    assert act.src in {a, b} and act.src != keeper

    # Zielpfad liegt unter target_dir/<digest[:8]>/<original_name>
    sub = digest[:8]
    assert act.dst.is_relative_to(target_dir)  # Python 3.9+: Path.is_relative_to
    assert act.dst.parent.name == sub
    assert act.dst.name == act.src.name

    # Reason enthält Digest-Kürzel
    assert sub in act.reason


def test_execute_actions_moves_file(tmp_path: Path):
    # Ordnerstruktur: src/ und dst/
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


def test_integration_dedupe_pipeline(tmp_path: Path):
    # Drei Dateien: zwei identische, eine andere
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    c = tmp_path / "c.txt"

    content_dup = b"HELLO\n"
    content_other = b"WORLD\n"

    a.write_bytes(content_dup)
    b.write_bytes(content_dup)
    c.write_bytes(content_other)

    # 1) Duplikatsgruppen finden
    paths = [a, b, c]
    groups = find_duplicate_groups(paths)

    # Es soll genau eine Gruppe mit a und b geben
    assert len(groups) == 1
    group = groups[0]
    assert set(group.files) == {a, b}

    # 2) Keeper bestimmen
    keeper = choose_keeper(group, policy="newest")
    assert keeper in {a, b}

    # 3) Moves planen
    target_dir = tmp_path / "dupes"
    actions = plan_moves(group, keeper, target_dir=target_dir)
    assert len(actions) == 1  # eine Datei wird verschoben

    # 4) Aktionen ausführen
    execute_actions(actions)

    # 5) Zustand prüfen

    # Keeper existiert noch am Originalort
    assert keeper.exists()

    # Die nicht-duplizierte Datei c bleibt unberührt
    assert c.exists()

    # Es gibt genau eine verschobene Datei im Zielordner
    moved_files = list(target_dir.rglob("*.txt"))
    assert len(moved_files) == 1
    moved = moved_files[0]

    # Inhalt ist gleich wie bei den Duplikaten
    assert moved.read_bytes() == content_dup

    # Dateiname gehört zu {a, b}, aber ist nicht der Keeper
    assert moved.name in {"a.txt", "b.txt"}
    assert moved.name != keeper.name
