import os
import httpx


def parse_github_url(url: str) -> dict:
    """
    Parses a GitHub blob URL: https://github.com/{owner}/{repo}/blob/{ref}/{path}
    Returns a dict with owner, repo, ref, path, and filename.
    """
    prefix = "https://github.com/"
    if not url.startswith(prefix):
        raise ValueError(
            f"Invalid GitHub URL: {url!r}. Must start with https://github.com/"
        )

    remainder = url[len(prefix):]
    parts = remainder.split("/")

    # Expected parts: [owner, repo, "blob", ref, path...]
    if len(parts) < 5 or parts[2] != "blob":
        raise ValueError(
            f"Invalid GitHub blob URL format: {url!r}. "
            "Expected format: https://github.com/{owner}/{repo}/blob/{ref}/{path}"
        )

    owner = parts[0]
    repo = parts[1]
    ref = parts[3]
    path = "/".join(parts[4:])
    filename = os.path.basename(path)

    return {
        "owner": owner,
        "repo": repo,
        "ref": ref,
        "path": path,
        "filename": filename,
    }


def fetch_raw_content(parsed: dict) -> str:
    """
    Fetches raw content from GitHub using the parsed URL components.
    Raises RuntimeError if the HTTP response status is not 2xx.
    """
    raw_url = (
        f"https://raw.githubusercontent.com"
        f"/{parsed['owner']}/{parsed['repo']}/{parsed['ref']}/{parsed['path']}"
    )

    response = httpx.get(raw_url, follow_redirects=True, timeout=30.0)

    if not (200 <= response.status_code < 300):
        raise RuntimeError(
            f"Failed to fetch content (HTTP {response.status_code}): {raw_url}"
        )

    return response.text
