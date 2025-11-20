from pathlib import Path
from sss.metadata import get_file_ext
from sss.metadata import get_sha256
import hashlib
from sss.metadata import get_mime_type
from sss.metadata import extract_metadata
from sss.metadata import get_image_size
from PIL import Image
from sss.metadata import get_file_size


def test_get_file_ext_basic_uppercase_to_lower(tmp_path: Path):
    f = tmp_path / "bild.JPG"
    f.write_bytes(b"x")
    assert get_file_ext(f) == "jpg"


def test_get_file_ext_multiple_dots(tmp_path):
    f = tmp_path / "foto.backup.JPG"
    f.write_text("x")
    assert get_file_ext(f) == "jpg"


def test_get_file_ext_hidden_file(tmp_path):
    f = tmp_path / ".gitignore"
    f.write_text("x")
    assert get_file_ext(f) == ""


def test_get_file_ext_double_extension(tmp_path):
    f = tmp_path / "archive.tar.gz"
    f.write_text("x")
    assert get_file_ext(f) == "gz"


def test_get_file_ext_no_extension(tmp_path):
    f = tmp_path / "bild"
    f.write_text("x")
    assert get_file_ext(f) == ""



def test_get_file_size_bytes(tmp_path):
    f = tmp_path / "a.bin"
    f.write_bytes(b"abc") 
    assert get_file_size(f) == 3


def test_get_file_size_accepts_str_path(tmp_path):
    f = tmp_path / "b.txt"
    f.write_text("Hallo")
    assert get_file_size(str(f)) == 5




def test_get_sha256_basic(tmp_path):
    f = tmp_path / "data.txt"
    f.write_bytes(b"abc")

   
    expected = hashlib.sha256(b"abc").hexdigest()

    assert get_sha256(f) == expected



def test_get_mime_type_png(tmp_path):
    f = tmp_path / "image.PNG"
    f.write_bytes(b"x")
    assert get_mime_type(f) == "image/png"

def test_get_mime_type_jpeg(tmp_path):
    f = tmp_path / "foto.jpeg"
    f.write_bytes(b"x")
    assert get_mime_type(f) in ("image/jpeg", "image/jpg")


def test_get_mime_type_unknown_extension(tmp_path):
    f = tmp_path / "file.unknown"
    f.write_bytes(b"x")
    assert get_mime_type(f) == "application/octet-stream"



def test_extract_metadata_basic(tmp_path):
    f = tmp_path / "image.PNG"
    f.write_bytes(b"abc") 

    expected_sha = hashlib.sha256(b"abc").hexdigest()

    md = extract_metadata(f)

    assert md["ext"] == "png"
    assert md["size"] == 3
    assert md["mime"] == "image/png"
    assert md["sha256"] == expected_sha



def test_get_image_size_png(tmp_path):
    f = tmp_path / "img.png"
    Image.new("RGB", (40, 30)).save(f, format="PNG")
    w, h = get_image_size(f)
    assert (w, h) == (40, 30)


def test_extract_metadata_includes_image_size(tmp_path):
    from sss.metadata import extract_metadata
    from PIL import Image

    f = tmp_path / "bild.png"
    Image.new("RGB", (100, 50)).save(f, format="PNG")

    md = extract_metadata(f)

    assert md["mime"] == "image/png"
    assert md["width"] == 100
    assert md["height"] == 50
