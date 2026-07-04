# github-to-pdf

A CLI tool that fetches a GitHub file by URL and renders it as a PDF with line numbers without any syntax highlighting.
This was largely vibe coded and then tweaked by a human to make it as desired. It's an activate work in progress so apologies for the ugly README. 

## Installation

### Probably unnecessary?
I don't think you need to do this? But now i can't remember so keeping it here
```bash
pip install -e ".[dev]"
```

### venv
You need to create and activate a virtual environment (venv) for it to run properly.

To create do the following inside the `pdf-maker` folder. This creates the virtual environment. You only need to do this once

```bash
python -m venv venv
```

This activates the virtual environment. You have to do this every time you want to activate the venv
```bash
source venv/bin/activate
```


Once you are done, to deactivate the venv do: 
```bash
deactivate
```

### activate toml
The cli command is defined in pyproject.toml To use it, you first have to install it in the venv as follows:
```bash
pip install -e .
```
If this errors, make sure you are using the pip in the venv, not the system pip (i.e., do `which pip`) A lot of problems can be solved by just uninstalling and reinstalling venv. 

## Running the CLI

**Basic usage:**

```bash
github-to-pdf https://github.com/owner/repo/blob/main/path/to/file.py
```

This saves `file.py.pdf` in the current directory.

**Options:**

| Option | Description |
|---|---|
| `--output` / `-o PATH` | Custom output PDF path (default: `<filename>.pdf`) |
| `--no-color` | Disable syntax highlighting; render plain monospace |

**Examples:**

```bash
# Custom output path
github-to-pdf https://github.com/psf/requests/blob/main/setup.py -o requests_setup.pdf

# Plain monospace (no syntax highlighting)
github-to-pdf https://github.com/encode/httpx/blob/master/httpx/__init__.py --no-color
```

## Making edits
Font, font size and border size can be editted in the `github_to_pdf/renderer.py` file. 

## Key files
#### AI generated stuff below

| File | Purpose |
|---|---|
| `github_to_pdf/cli.py` | Click CLI entry point — parses options, orchestrates fetch → render |
| `github_to_pdf/fetcher.py` | `parse_github_url` (URL → metadata dict) and `fetch_raw_content` (httpx GET to `raw.githubusercontent.com`) |
| `github_to_pdf/renderer.py` | `render_pdf` — Pygments tokenisation + ReportLab PDF generation with line numbers and Monokai theme |
| `pyproject.toml` | Build metadata, runtime dependencies (`click`, `httpx`, `pygments`, `reportlab`), dev dependencies (`pytest`, `pytest-httpx`, `Pillow`) |

## Running tests

```bash
pytest tests/
```

| Test file | What it covers |
|---|---|
| `tests/test_cli.py` | CLI integration: valid URL → exit 0 + success message; invalid URL → exit 1 + error message; `--output` flag; `--no-color` flag |
| `tests/test_fetcher.py` | `parse_github_url` for simple and nested paths, wrong domain, missing blob segment, too-short URLs; `fetch_raw_content` success (200), 404, and 500 using `pytest-httpx` mocks |
| `tests/test_renderer.py` | `render_pdf` produces a valid `%PDF` file; handles unknown file extensions; handles empty code string |

## Dependencies (brief)

- **click** — CLI framework
- **httpx** — async-capable HTTP client for fetching raw GitHub content
- **pygments** — syntax tokenisation and colour lookup
- **reportlab** — PDF document generation
