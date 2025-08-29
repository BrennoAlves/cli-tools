import click
from src.lib.utils import show_dashboard


@click.command(name='status')
@click.option('--simple', is_flag=True, help='Modo simplificado')
@click.option('--live', is_flag=True, help='Atualização em tempo real (ignorado)')
def status(simple: bool, live: bool):
    """Exibe o dashboard de status do sistema."""
    show_dashboard(simple=True, live=False)
