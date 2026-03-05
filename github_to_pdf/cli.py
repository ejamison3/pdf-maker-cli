import click
import sys
from github_to_pdf import fetcher, renderer

@click.command()
@click.argument("url")
@click.option(
    "--output", "-o", 
    type=click.Path(), 
    help="Output PDF path (defaults to <filename>.pdf in current directory)."
)
@click.option(
    "--no-color", 
    is_flag=True, 
    help="Disable syntax highlighting (render plain monospace)."
)
def main(url: str, output: str | None, no_color: bool):
    """Convert a GitHub repository or file to PDF."""
    try:
        parsed = fetcher.parse_github_url(url)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    try:
        code = fetcher.fetch_raw_content(parsed)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    output_path = output or f"{parsed['filename']}.pdf"

    renderer.render_pdf(code, parsed['filename'], output_path, no_color=no_color)
    click.echo(f"PDF saved to: {output_path}")

if __name__ == "__main__":
    main()
