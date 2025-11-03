from pathlib import Path
import re

def sanitize_filename(name: str) -> str:
    """
    Entfernt ungültige Zeichen aus einem Dateinamen (Windows-kompatibel).
    Beispiel: 'bild:neu?.png' -> 'bild_neu_.png'
    """
    name = re.sub(r'[<>:"/\\|?*]+', "_", name)  
    name = name.strip().rstrip(".")             
    return name or "_"                          

def unique_path(dest_dir: Path, filename: str) -> Path:
    """
    Gibt einen eindeutigen Pfad in dest_dir zurück.
    Beispiel: 'bild.png' -> 'bild (1).png' falls vorhanden.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    p = Path(filename)
    stem = sanitize_filename(p.stem)
    suffix = p.suffix
    candidate = dest_dir / f"{stem}{suffix}"
    counter = 1
    while candidate.exists():
        candidate = dest_dir / f"{stem} ({counter}){suffix}"
        counter += 1
    return candidate
