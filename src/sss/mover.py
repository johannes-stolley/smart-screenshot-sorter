from pathlib import Path
from datetime import datetime
import shutil
from .renamer import unique_path
from .dedupe import DedupAction


def build_target_path(file_path: Path, out_root: Path) -> Path:
    ts = file_path.stat().st_mtime
    dt = datetime.fromtimestamp(ts)
    year = f"{dt:%Y}"
    month = f"{dt:%m}"
    return out_root / year / month


def safe_move(src: Path, dest_dir: Path) -> Path:
    dest_path = unique_path(dest_dir, src.name)
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), dest_path)
    return dest_path


def execute_actions(actions: list[DedupAction]) -> None:
    """
    Führt die übergebenen DedupActions aus.
    Aktuell unterstützen wir nur: action == 'move'.
    """
    for act in actions:
        src = act.src if isinstance(act.src, Path) else Path(act.src)
        dst = act.dst if isinstance(act.dst, Path) else Path(act.dst)

        # Zielordner anlegen, falls nötig
        dst.parent.mkdir(parents=True, exist_ok=True)

        if act.action == "move":
            # Datei verschieben/umbenennen
            src.replace(dst)
        else:
            raise ValueError(f"Unsupported action: {act.action!r}")
