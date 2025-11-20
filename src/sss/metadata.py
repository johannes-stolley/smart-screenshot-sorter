"""Utility module for extracting file metadata:
- file extension, size, sha256 hash, MIME type
- optional image width/height via Pillow
"""



from pathlib import Path
import hashlib
import mimetypes
from PIL import Image, UnidentifiedImageError

def get_file_ext(path: Path | str) -> str:
    """Return file extension in lowercase without dot ('' if none)."""
    p = Path(path)
    return p.suffix.lstrip(".").lower()


def get_file_size(path: Path | str) -> int:
    """Return file size in bytes."""
    p = Path(path)
    return p.stat().st_size



def get_sha256(path: Path | str) -> str:
    """Return SHA-256 hex digest of file content."""
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()



def get_mime_type(path: Path | str) -> str:
    """Return MIME type guessed from filename (fallback: application/octet-stream)."""
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".png":
        return "image/png"
    return mimetypes.guess_type(p.name)[0] or "application/octet-stream"


def get_image_size(path: Path | str) -> tuple[int, int]:
    """Return (width, height) for image files."""
    p = Path(path)
    with Image.open(p) as img:
        return img.size  # (width, height)




def extract_metadata(path: Path | str) -> dict:
    """Collect basic metadata (ext, size, sha256, mime, optional width/height)."""
    p = Path(path)
    md = {
        "ext": get_file_ext(p),
        "size": get_file_size(p),
        "sha256": get_sha256(p),
        "mime": get_mime_type(p),
    }
    if md["mime"].startswith("image/"):
        try:
            w, h = get_image_size(p)
            md["width"] = w
            md["height"] = h
        except UnidentifiedImageError:
            pass
    return md

