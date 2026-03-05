import click

@click.command()
@click.argument("url")
def main(url: str):
    """Convert a GitHub repository or file to PDF."""
    click.echo(f"URL: {url}")

if __name__ == "__main__":
    main()
