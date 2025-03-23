"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Glicko."""


if __name__ == "__main__":
    main(prog_name="glicko")  # pragma: no cover
