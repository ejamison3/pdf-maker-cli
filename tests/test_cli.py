from click.testing import CliRunner
from github_to_pdf.cli import main

def test_cli_smoke():
    runner = CliRunner()
    result = runner.invoke(main, ["https://github.com/user/repo"])
    assert result.exit_code == 0
    assert "URL: https://github.com/user/repo" in result.output
