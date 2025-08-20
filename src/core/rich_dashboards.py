"""
Dashboard principal da CLI, focado em clareza e design moderno.
"""

from datetime import datetime
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
import time

from .config import validar_chaves_api
from .controle_uso import controlador_uso
from .config_diretorios import ConfigDiretorios
from .visuals import console, styled_panel, DRACULA_THEME

class ModernDashboard:
    """Gera um dashboard moderno e informativo para a CLI."""

    def __init__(self):
        self.config_dirs = ConfigDiretorios()

    def _get_api_status(self):
        problemas = validar_chaves_api()
        apis = ['pexels', 'figma', 'gemini']
        status = {}
        for api in apis:
            is_ok = api not in problemas
            usage = controlador_uso.get_uso_hoje(api)
            limit = controlador_uso.get_limite(api)
            status[api] = {
                "ok": is_ok,
                "icon": "✅" if is_ok else "❌",
                "label": f"{api.title()} API",
                "usage": f"{usage}/{limit} reqs",
                "description": "Operacional" if is_ok else problemas[api]
            }
        return status

    def _build_api_status_panel(self):
        status = self._get_api_status()
        
        grid = Table.grid(expand=True, padding=(0, 1))
        grid.add_column(style=f"{DRACULA_THEME['green']}")
        grid.add_column(style=f"{DRACULA_THEME['foreground']}")
        grid.add_column(style=f"italic {DRACULA_THEME['comment']}", justify="right")

        for api_info in status.values():
            grid.add_row(api_info["icon"], api_info["label"], api_info["description"])

        return styled_panel(grid, "🔌 Status das APIs", "Verificação de conectividade e uso")

    def _build_workspace_panel(self):
        stats = self.config_dirs.obter_estatisticas_workspace()

        grid = Table.grid(expand=True, padding=(0, 1))
        grid.add_column(style=f"{DRACULA_THEME['cyan']}") # Icon
        grid.add_column(style=f"{DRACULA_THEME['foreground']}") # Directory
        grid.add_column(style=f"{DRACULA_THEME['foreground']}", justify="right") # Files
        grid.add_column(style=f"{DRACULA_THEME['yellow']}", justify="right") # Size

        for dir_name, dir_stats in stats["directories"].items():
            grid.add_row(
                "📁",
                f"{dir_name.title()}",
                f"{dir_stats['files']} arquivos",
                f"{dir_stats['size_mb']:.2f} MB"
            )
        
        return styled_panel(grid, "🏠 Workspace", f"Total: {stats['total_files']} arquivos, {stats['total_size_mb']:.2f} MB")

    def _build_header(self):
        title = Text("GEMINI CLI", style="primary", justify="center")
        subtitle = Text(datetime.now().strftime("%d de %B, %Y - %H:%M:%S"), style="secondary", justify="center")
        return Panel(Text.assemble(title, "\n", subtitle), border_style="primary")

    def _generate_layout(self):
        layout = Layout()
        layout.split(
            Layout(self._build_header(), name="header", size=3),
            Layout(ratio=1, name="main"),
        )
        layout["main"].split_row(
            Layout(self._build_api_status_panel(), name="left"),
            Layout(self._build_workspace_panel(), name="right"),
        )
        return layout

    def display(self):
        """Exibe o dashboard estático."""
        console.print(self._generate_layout())

    def display_live(self):
        """Exibe o dashboard com atualizações em tempo real."""
        try:
            with Live(self._generate_layout(), screen=True, redirect_stderr=False, refresh_per_second=1) as live:
                while True:
                    time.sleep(1)
                    live.update(self._generate_layout())
        except KeyboardInterrupt:
            console.print("\n[success]👋 Dashboard finalizado.[/success]")

# Instância para fácil acesso
modern_dashboard = ModernDashboard()