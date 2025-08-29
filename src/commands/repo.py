import click
from typing import Optional
from src.lib.apis import repo_download_auto


@click.command(name='repo')
@click.argument('repositorio')
@click.argument('query', required=False)
@click.option('--query', '-q', 'query_flag', help='Query para IA')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--explain', type=click.Choice(['silencioso', 'basico', 'detalhado', 'debug']))
@click.option('--dry-run', is_flag=True)
@click.option('--interactive', '-i', is_flag=True)
@click.option('--no-ai', is_flag=True)
@click.option('--all', 'all_clone', is_flag=True)
@click.option('--json', 'output_json', is_flag=True)
def repo(repositorio: str, query: Optional[str], query_flag: Optional[str], output: Optional[str], explain: Optional[str], dry_run: bool, interactive: bool, no_ai: bool, all_clone: bool, output_json: bool):
    """Baixar repositório com ou sem IA."""
    if not query and query_flag:
        query = query_flag
    try:
        path = repo_download_auto(
            repositorio,
            query=query,
            output=output,
            no_ai=no_ai,
            all_clone=all_clone,
            explain=explain,
            dry_run=dry_run,
            interactive=interactive,
        )
        click.echo(f"📦 Repositório salvo em: {path}")
    except Exception as e:
        click.echo(f"❌ Erro no download do repositório: {e}")
        raise SystemExit(1)
