#!/usr/bin/env python3
"""CLI Tools v2.0 — Entry point minimalista."""

import click

from src.commands.search import search
from src.commands.figma import figma
from src.commands.repo import repo
from src.commands.status import status


@click.group(invoke_without_command=True)
@click.version_option(version="2.0.0", prog_name="CLI Tools")
@click.pass_context
def cli(ctx):
    """CLI Tools v2.0 - Kit de ferramentas para desenvolvedores."""
    if ctx.invoked_subcommand is None:
        # Import tardio para evitar exigir Textual fora do modo UI
        from src.lib.ui import interactive_menu
        interactive_menu()


@cli.command()
def ui():
    """Interface interativa."""
    from src.lib.ui import interactive_menu
    interactive_menu()


# Registrar comandos isolados
cli.add_command(search)
cli.add_command(figma)
cli.add_command(repo)
cli.add_command(status)


if __name__ == "__main__":
    cli()
