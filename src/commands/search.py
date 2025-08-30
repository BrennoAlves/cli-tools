import click
from ..lib.apis import pexels_download_files


@click.command(name='search')
@click.argument('consulta')
@click.option('--count', '-c', default=1, help='Número de imagens (padrão: 1)')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--orientation', type=click.Choice(['landscape', 'portrait', 'square']), help='Orientação')
@click.option('--json', 'output_json', is_flag=True, help='Saída em formato JSON')
def search(consulta, count, output, orientation, output_json):
    """Buscar e baixar imagens do Pexels."""
    # Execução direta (sem subprocess). Para saída JSON, apenas ecoa caminhos.
    try:
        files = pexels_download_files(consulta, count=count, orientation=orientation, output=output)
        if output_json:
            import json
            print(json.dumps(files, ensure_ascii=False, indent=2))
        else:
            for f in files:
                click.echo(f"📁 {f['nome']} ({f['tamanho']})")
    except Exception as e:
        click.echo(f"❌ Erro na busca/baixar imagens: {e}")
        raise SystemExit(1)
