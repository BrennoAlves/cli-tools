import click
from typing import Optional
from ..lib.apis import figma_download_files


@click.command(name='figma')
@click.argument('file_key')
@click.option('--max', '--number', '-n', 'max_images', default=3, help='Máximo de imagens')
@click.option('--format', '-f', 'fmt', default='png', help='Formato: png/webp/jpg/svg/pdf')
@click.option('--mode', type=click.Choice(['all', 'components', 'css']), default='all', help='Modo de extração')
@click.option('--output', '-o', help='Diretório de saída')
def figma(file_key: str, max_images: int, fmt: str, mode: str, output: Optional[str]):
    """Extrair designs do Figma."""
    try:
        files = figma_download_files(file_key, fmt=fmt, scale=1.0, output=output, nodes=None, max_images=max_images, mode=mode)
        if not files:
            click.echo("⚠️ Nenhum arquivo gerado.")
        for f in files:
            click.echo(f"📁 {f['nome']} ({f['tamanho']})")
    except Exception as e:
        click.echo(f"❌ Erro no Figma: {e}")
        raise SystemExit(1)
