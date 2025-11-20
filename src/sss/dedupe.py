from pathlib import Path
import hashlib
from dataclasses import dataclass
from collections import defaultdict
from typing import Literal


def compute_sha256(path: Path, *, chunk_size: int = 1 << 20) -> str:
    """
    Berechnet den SHA-256-Hash einer Datei und gibt ihn als 64-stelligen Hex-String zurück.
    - chunk_size: in Bytes (Default ~1 MB) -> ermöglicht hashing großer Dateien ohne viel RAM.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    h = hashlib.sha256()
    with path.open("rb") as f:
        # Datei stückweise lesen, bis read() b"" liefert (EOF).
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)

    return h.hexdigest()  # lowercase 64-hex


@dataclass
class DuplicateGroup:
    """Repräsentiert eine Gruppe von Dateien mit identischem Inhalt."""

    size: int  # Dateigröße in Bytes
    digest: str  # SHA-256 Hash
    files: list[Path]  # Liste der Pfade (mind. 2)


def find_duplicate_groups(paths: list[Path]) -> list[DuplicateGroup]:
    """
    Findet Duplikate auf Byte-Ebene:
    - Vorfilter: nach Dateigröße gruppieren
    - Für Größen-Buckets mit >=2 Dateien: SHA-256-Hash berechnen
    - Dateien mit identischem (size, digest) zu DuplicateGroup bündeln
    """
    # 1) Leereingabe
    if not paths:
        return []

    # 2) Nach Größe gruppieren
    size_buckets: dict[int, list[Path]] = defaultdict(list)
    for p in paths:
        # nur reguläre Dateien berücksichtigen
        if not isinstance(p, Path):

            p = Path(p)
        if p.is_file():
            size_buckets[p.stat().st_size].append(p)

    groups: list[DuplicateGroup] = []

    # 3) Nur Buckets mit mindestens 2 Dateien weiterverarbeiten
    hash_buckets: dict[tuple[int, str], list[Path]] = defaultdict(list)
    for size, files in size_buckets.items():
        if len(files) < 2:
            continue
        # 4) Hash pro Datei berechnen und nach (size, digest) gruppieren
        for fp in files:
            digest = compute_sha256(fp)
            hash_buckets[(size, digest)].append(fp)

    # 5) DuplicateGroup-Objekte erzeugen (nur, wenn >=2 Dateien)
    for (size, digest), same_files in hash_buckets.items():
        if len(same_files) >= 2:
            groups.append(DuplicateGroup(size=size, digest=digest, files=same_files))

    # 6) Rückgabe
    return groups


def choose_keeper(group: DuplicateGroup, *, policy: str = "newest") -> Path:
    """
    Wählt eine Datei aus der Duplikatgruppe als 'Keeper'.
    Standard-Policy: 'newest' -> Datei mit größtem mtime.
    """
    if not group.files:
        raise ValueError("DuplicateGroup.files ist leer")

    files = [p if isinstance(p, Path) else Path(p) for p in group.files]

    if policy == "newest":
        return max(files, key=lambda p: p.stat().st_mtime)
    elif policy == "oldest":
        return min(files, key=lambda p: p.stat().st_mtime)
    elif policy == "shortest_path":
        return min(files, key=lambda p: (len(str(p)), str(p)))
    else:
        raise ValueError(f"Unbekannte Policy: {policy!r}")


@dataclass
class DedupAction:
    src: Path
    action: Literal["move"]
    dst: Path
    reason: str


def plan_moves(
    group: DuplicateGroup, keeper: Path, *, target_dir: Path
) -> list[DedupAction]:
    """
    Erzeuge einen Dry-Run-Plan: Alle Nicht-Keeper einer Gruppe
    werden 'virtuell' nach target_dir/<digest[:8]>/<original_name> verschoben.
    """
    # Normalisiere Typen
    keeper = keeper if isinstance(keeper, Path) else Path(keeper)
    files = [p if isinstance(p, Path) else Path(p) for p in group.files]

    digest_prefix = group.digest[:8]
    base = target_dir / digest_prefix

    actions: list[DedupAction] = []
    for src in files:
        if src == keeper:
            continue
        dst = base / src.name
        reason = f"duplicate of {keeper.name} ({digest_prefix})"
        actions.append(DedupAction(src=src, action="move", dst=dst, reason=reason))

    return actions


def execute_actions(actions, summary) -> None:
    """
    Führt die geplanten Aktionen aus.
    Aktuell: nur 'move' wird unterstützt, minimal für den CLI-Test.

    actions: Iterable von DedupAction
    summary: Summary-Objekt (wird vorerst nicht benutzt)
    """
    for act in actions:
        if act.action == "move":
            src = Path(act.src)
            dst = Path(act.dst)

            dst.parent.mkdir(parents=True, exist_ok=True)
            src.replace(dst)  # Datei wirklich verschieben

            # TODO: Hier könntest du später summary.update(...) o.ä. aufrufen
