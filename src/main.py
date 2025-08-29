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
        # Interface navegável por setas como Gemini CLI
        try:
            from src.lib.ui_gemini import interactive_menu
            interactive_menu()
        except ImportError as e:
            click.echo(f"❌ Erro ao carregar interface: {e}")
            click.echo("💡 Instale as dependências: pip install -r requirements.txt")
            ctx.get_help()


@cli.command()
def ui():
    """Interface interativa navegável por setas."""
    try:
        from src.lib.ui_gemini import interactive_menu
        interactive_menu()
    except ImportError as e:
        click.echo(f"❌ Erro ao carregar interface: {e}")
        click.echo("💡 Instale as dependências: pip install -r requirements.txt")


# Registrar comandos isolados
cli.add_command(search)
cli.add_command(figma)
cli.add_command(repo)
cli.add_command(status)


if __name__ == "__main__":
    cli()
