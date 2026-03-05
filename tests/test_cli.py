from unittest.mock import patch
from click.testing import CliRunner
from github_to_pdf.cli import main

def test_cli_success():
    runner = CliRunner()
    url = "https://github.com/user/repo/blob/main/file.py"
    
    with patch("github_to_pdf.fetcher.fetch_raw_content", return_value="print('hello')") as mock_fetch:
        with patch("github_to_pdf.renderer.render_pdf") as mock_render:
            result = runner.invoke(main, [url])
            
            assert result.exit_code == 0
            assert "PDF saved to: file.py.pdf" in result.output
            mock_fetch.assert_called_once()
            mock_render.assert_called_once_with("print('hello')", "file.py", "file.py.pdf", no_color=False)

def test_cli_invalid_url():
    runner = CliRunner()
    result = runner.invoke(main, ["https://not-github.com/bad/url"])
    
    assert result.exit_code == 1
    assert "Error: Invalid GitHub URL" in result.output

def test_cli_output_option():
    runner = CliRunner()
    url = "https://github.com/user/repo/blob/main/file.py"
    custom_output = "custom.pdf"
    
    with patch("github_to_pdf.fetcher.fetch_raw_content", return_value="code"):
        with patch("github_to_pdf.renderer.render_pdf") as mock_render:
            result = runner.invoke(main, [url, "--output", custom_output])
            
            assert result.exit_code == 0
            assert f"PDF saved to: {custom_output}" in result.output
            mock_render.assert_called_once_with("code", "file.py", custom_output, no_color=False)

def test_cli_no_color_option():
    runner = CliRunner()
    url = "https://github.com/user/repo/blob/main/file.py"
    
    with patch("github_to_pdf.fetcher.fetch_raw_content", return_value="code"):
        with patch("github_to_pdf.renderer.render_pdf") as mock_render:
            result = runner.invoke(main, [url, "--no-color"])
            
            assert result.exit_code == 0
            mock_render.assert_called_once_with("code", "file.py", "file.py.pdf", no_color=True)
