import pytest
import httpx
from github_to_pdf.fetcher import parse_github_url, fetch_raw_content


# ---------------------------------------------------------------------------
# parse_github_url
# ---------------------------------------------------------------------------

def test_parse_github_url_simple_path():
    url = "https://github.com/psf/requests/blob/main/setup.py"
    parsed = parse_github_url(url)

    assert parsed["owner"] == "psf"
    assert parsed["repo"] == "requests"
    assert parsed["ref"] == "main"
    assert parsed["path"] == "setup.py"
    assert parsed["filename"] == "setup.py"


def test_parse_github_url_nested_path():
    url = "https://github.com/encode/httpx/blob/master/httpx/__init__.py"
    parsed = parse_github_url(url)

    assert parsed["owner"] == "encode"
    assert parsed["repo"] == "httpx"
    assert parsed["ref"] == "master"
    assert parsed["path"] == "httpx/__init__.py"
    assert parsed["filename"] == "__init__.py"


def test_parse_github_url_wrong_domain():
    with pytest.raises(ValueError, match="Invalid GitHub URL"):
        parse_github_url("https://google.com/user/repo/blob/main/file.py")


def test_parse_github_url_missing_blob_segment():
    with pytest.raises(ValueError, match="Invalid GitHub blob URL format"):
        parse_github_url("https://github.com/user/repo/tree/main/file.py")


def test_parse_github_url_too_short():
    with pytest.raises(ValueError, match="Invalid GitHub blob URL format"):
        parse_github_url("https://github.com/user/repo")


# ---------------------------------------------------------------------------
# fetch_raw_content
# ---------------------------------------------------------------------------

def test_fetch_raw_content_success(httpx_mock):
    parsed = {
        "owner": "user",
        "repo": "repo",
        "ref": "main",
        "path": "test.txt",
    }
    target_url = "https://raw.githubusercontent.com/user/repo/main/test.txt"
    httpx_mock.add_response(url=target_url, text="hello world", status_code=200)

    content = fetch_raw_content(parsed)

    assert content == "hello world"


def test_fetch_raw_content_not_found_raises_runtime_error(httpx_mock):
    parsed = {
        "owner": "user",
        "repo": "repo",
        "ref": "main",
        "path": "missing.txt",
    }
    target_url = "https://raw.githubusercontent.com/user/repo/main/missing.txt"
    httpx_mock.add_response(url=target_url, status_code=404)

    with pytest.raises(RuntimeError, match="HTTP 404"):
        fetch_raw_content(parsed)


def test_fetch_raw_content_server_error_raises_runtime_error(httpx_mock):
    parsed = {
        "owner": "user",
        "repo": "repo",
        "ref": "main",
        "path": "file.py",
    }
    target_url = "https://raw.githubusercontent.com/user/repo/main/file.py"
    httpx_mock.add_response(url=target_url, status_code=500)

    with pytest.raises(RuntimeError, match="HTTP 500"):
        fetch_raw_content(parsed)
