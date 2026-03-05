import pytest
from github_to_pdf.renderer import render_pdf


def test_render_pdf_creates_valid_file(tmp_path):
    output_file = tmp_path / "out.pdf"
    code = "x = 1\ny = 2\n"
    filename = "test.py"

    render_pdf(code, filename, str(output_file))

    assert output_file.exists()
    assert output_file.stat().st_size > 0

    with open(output_file, "rb") as f:
        header = f.read(4)
    assert header == b"%PDF"


def test_render_pdf_unknown_extension(tmp_path):
    output_file = tmp_path / "out.pdf"
    code = "some random text\nline 2"
    filename = "README.unknownext"

    render_pdf(code, filename, str(output_file))

    assert output_file.exists()
    with open(output_file, "rb") as f:
        assert f.read(4) == b"%PDF"


def test_render_pdf_empty_code(tmp_path):
    output_file = tmp_path / "out.pdf"

    render_pdf("", "empty.py", str(output_file))

    assert output_file.exists()
    with open(output_file, "rb") as f:
        assert f.read(4) == b"%PDF"
