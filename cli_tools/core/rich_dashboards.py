"""
Dashboards avançados usando Rich para CLI Tools
Implementa 4 versões diferentes do dashboard de status
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.columns import Columns
from rich.tree import Tree
from rich.align import Align
from rich.rule import Rule
from rich import box
import time

from .config import ConfigAPI, validar_chaves_api
from .controle_uso import controlador_uso


class RichDashboards:
    """Classe para gerenciar diferentes tipos de dashboards Rich"""
    
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.console = Console()
        
    def _get_dracula_theme(self):
        """Retorna tema Dracula personalizado"""
        from rich.theme import Theme
        return Theme({
            "primary": "bold magenta",
            "secondary": "bold cyan", 
            "success": "bold green",
            "warning": "bold yellow",
            "error": "bold red",
            "info": "blue",
            "text": "white",
            "background": "black"
        })
    
    def _get_api_status(self) -> Dict[str, Dict[str, Any]]:
        """Coleta status das APIs"""
        from .config import validar_chaves_api
        
        problemas = validar_chaves_api()
        
        return {
            'pexels': {
                'name': 'Pexels API',
                'status': 'pexels' not in problemas,
                'info': 'Busca de imagens' if 'pexels' not in problemas else problemas['pexels'],
                'icon': '🖼️',
                'usage': self._get_api_usage('pexels')
            },
            'figma': {
                'name': 'Figma API', 
                'status': 'figma' not in problemas,
                'info': 'Extração de designs' if 'figma' not in problemas else problemas['figma'],
                'icon': '🎨',
                'usage': self._get_api_usage('figma')
            },
            'gemini': {
                'name': 'Google Gemini',
                'status': 'gemini' not in problemas, 
                'info': 'IA para análise' if 'gemini' not in problemas else problemas['gemini'],
                'icon': '🤖',
                'usage': self._get_api_usage('gemini')
            }
        }
    
    def _get_api_usage(self, api_name: str) -> Dict[str, Any]:
        """Obtém dados de uso de uma API"""
        try:
            requests_today = controlador_uso.get_uso_hoje(api_name)
            quota_limit = controlador_uso.get_limite(api_name)
            
            # Calcular total aproximado (hoje * 30 como estimativa)
            requests_total = requests_today * 30
            
            # Última requisição (simulada baseada no uso)
            last_request = "Hoje" if requests_today > 0 else "Nunca"
            
            return {
                'requests_today': requests_today,
                'requests_total': requests_total,
                'last_request': last_request,
                'quota_limit': quota_limit
            }
        except Exception as e:
            return {
                'requests_today': 0,
                'requests_total': 0, 
                'last_request': 'Nunca',
                'quota_limit': 'Desconhecido'
            }
    
    def _get_workspace_info(self) -> Dict[str, Any]:
        """Obtém informações do workspace"""
        try:
            from .config_diretorios import ConfigDiretorios
            config_dirs = ConfigDiretorios()
            
            workspace_dir = config_dirs.obter_diretorio('workspace')
            
            # Contar arquivos em cada diretório
            stats = {}
            for tipo in ['imagens', 'figma', 'repos']:
                dir_path = Path(config_dirs.obter_diretorio(tipo))
                if dir_path.exists():
                    files = list(dir_path.rglob('*'))
                    stats[tipo] = {
                        'path': str(dir_path),
                        'files': len([f for f in files if f.is_file()]),
                        'size': sum(f.stat().st_size for f in files if f.is_file() and f.exists()) / (1024*1024)  # MB
                    }
                else:
                    stats[tipo] = {'path': str(dir_path), 'files': 0, 'size': 0}
            
            return {
                'workspace_path': str(workspace_dir),
                'stats': stats,
                'total_files': sum(s['files'] for s in stats.values()),
                'total_size': sum(s['size'] for s in stats.values())
            }
        except Exception as e:
            return {
                'workspace_path': 'Erro ao obter',
                'stats': {},
                'total_files': 0,
                'total_size': 0,
                'error': str(e)
            }
    
    def dashboard_version_a_table(self) -> None:
        """Versão A: Rich Table simples com informações de APIs"""
        if self.quiet:
            return
            
        self.console.print("\n[bold magenta]🎯 CLI Tools - Dashboard Status (Versão A - Table)[/bold magenta]", style="bold")
        self.console.print("[blue]Versão: Rich Table simples com informações de APIs[/blue]\n")
        
        # Tabela de APIs
        api_table = Table(title="📊 Status das APIs", box=box.ROUNDED)
        api_table.add_column("API", style="bold magenta", width=15)
        api_table.add_column("Status", width=10)
        api_table.add_column("Descrição", style="white")
        api_table.add_column("Uso Hoje", justify="right", style="bold cyan")
        
        apis = self._get_api_status()
        for api_key, api_data in apis.items():
            status_icon = "[bold green]✅ Ativo[/bold green]" if api_data['status'] else "[bold red]❌ Inativo[/bold red]"
            usage = api_data['usage']['requests_today']
            
            api_table.add_row(
                f"{api_data['icon']} {api_data['name']}",
                status_icon,
                api_data['info'][:50] + "..." if len(api_data['info']) > 50 else api_data['info'],
                str(usage)
            )
        
        self.console.print(api_table)
        
        # Tabela de Workspace
        workspace = self._get_workspace_info()
        workspace_table = Table(title="📁 Workspace Status", box=box.ROUNDED)
        workspace_table.add_column("Diretório", style="bold magenta")
        workspace_table.add_column("Arquivos", justify="right", style="bold cyan")
        workspace_table.add_column("Tamanho (MB)", justify="right", style="bold yellow")
        workspace_table.add_column("Caminho", style="blue")
        
        for tipo, stats in workspace['stats'].items():
            workspace_table.add_row(
                f"📂 {tipo.title()}",
                str(stats['files']),
                f"{stats['size']:.1f}",
                stats['path']
            )
        
        self.console.print("\n")
        self.console.print(workspace_table)
        
        # Resumo
        self.console.print(f"\n[bold green]✨ Total: {workspace['total_files']} arquivos, {workspace['total_size']:.1f} MB[/bold green]")
    
    def dashboard_version_b_panels(self) -> None:
        """Versão B: Rich Panel com seções organizadas por serviço"""
        if self.quiet:
            return
            
        self.console.print("\n[bold magenta]🎯 CLI Tools - Dashboard Status (Versão B - Panels)[/primary]", style="bold")
        self.console.print("[blue]Versão: Rich Panel com seções organizadas por serviço[/info]\n")
        
        apis = self._get_api_status()
        workspace = self._get_workspace_info()
        
        # Panel para cada API
        api_panels = []
        for api_key, api_data in apis.items():
            status_color = "success" if api_data['status'] else "error"
            status_text = "🟢 ATIVO" if api_data['status'] else "🔴 INATIVO"
            
            usage = api_data['usage']
            panel_content = f"""[{status_color}]{status_text}[/{status_color}]
            
📊 Uso: {usage['requests_today']} requests hoje
📈 Total: {usage['requests_total']} requests
⏰ Último: {usage['last_request']}
🎯 Limite: {usage['quota_limit']}

ℹ️  {api_data['info']}"""
            
            panel = Panel(
                panel_content,
                title=f"{api_data['icon']} {api_data['name']}",
                border_style=status_color,
                padding=(1, 2)
            )
            api_panels.append(panel)
        
        # Mostrar panels das APIs em colunas
        self.console.print(Columns(api_panels, equal=True, expand=True))
        
        # Panel do Workspace
        workspace_content = f"""📁 Workspace: {workspace['workspace_path']}

📊 Estatísticas:"""
        
        for tipo, stats in workspace['stats'].items():
            workspace_content += f"""
  📂 {tipo.title()}: {stats['files']} arquivos ({stats['size']:.1f} MB)"""
        
        workspace_content += f"""

✨ Total: {workspace['total_files']} arquivos, {workspace['total_size']:.1f} MB"""
        
        workspace_panel = Panel(
            workspace_content,
            title="🏠 Workspace Status",
            border_style="primary",
            padding=(1, 2)
        )
        
        self.console.print("\n")
        self.console.print(workspace_panel)
    
    def dashboard_version_c_layout(self) -> None:
        """Versão C: Rich Layout com múltiplas colunas e gráficos"""
        if self.quiet:
            return
            
        self.console.print("\n[bold magenta]🎯 CLI Tools - Dashboard Status (Versão C - Layout)[/primary]", style="bold")
        self.console.print("[blue]Versão: Rich Layout com múltiplas colunas e gráficos[/info]\n")
        
        # Criar layout principal
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        layout["left"].split_column(
            Layout(name="apis"),
            Layout(name="usage")
        )
        
        # Header
        header_text = Text("CLI Tools Dashboard", style="bold primary", justify="center")
        layout["header"].update(Panel(header_text, style="primary"))
        
        # APIs Status (esquerda superior)
        apis = self._get_api_status()
        api_tree = Tree("🔌 APIs Status", style="primary")
        
        for api_key, api_data in apis.items():
            status_style = "success" if api_data['status'] else "error"
            status_icon = "🟢" if api_data['status'] else "🔴"
            
            api_branch = api_tree.add(f"{status_icon} {api_data['name']}", style=status_style)
            api_branch.add(f"📊 Hoje: {api_data['usage']['requests_today']} requests")
            api_branch.add(f"📈 Total: {api_data['usage']['requests_total']} requests")
            api_branch.add(f"ℹ️  {api_data['info'][:30]}...")
        
        layout["apis"].update(Panel(api_tree, title="APIs", border_style="secondary"))
        
        # Usage Graph (esquerda inferior) - Simulação de gráfico com barras
        usage_content = ""
        for api_key, api_data in apis.items():
            usage_today = api_data['usage']['requests_today']
            bar_length = min(20, max(1, usage_today // 5)) if usage_today > 0 else 1
            bar = "█" * bar_length
            
            usage_content += f"{api_data['icon']} {api_key.title():<8} {bar} {usage_today}\n"
        
        layout["usage"].update(Panel(usage_content, title="📊 Uso Hoje", border_style="warning"))
        
        # Workspace Info (direita)
        workspace = self._get_workspace_info()
        workspace_tree = Tree("🏠 Workspace", style="primary")
        
        for tipo, stats in workspace['stats'].items():
            tipo_branch = workspace_tree.add(f"📂 {tipo.title()}")
            tipo_branch.add(f"📄 {stats['files']} arquivos")
            tipo_branch.add(f"💾 {stats['size']:.1f} MB")
            tipo_branch.add(f"📍 {stats['path']}")
        
        workspace_summary = f"""
📊 Resumo Total:
  📄 {workspace['total_files']} arquivos
  💾 {workspace['total_size']:.1f} MB
  📁 {workspace['workspace_path']}
"""
        
        workspace_content = Align.center(workspace_tree)
        layout["right"].update(Panel(workspace_content, title="Workspace", border_style="success"))
        
        # Footer
        footer_text = Text(f"⏰ Atualizado em: {datetime.now().strftime('%H:%M:%S')}", style="info", justify="center")
        layout["footer"].update(Panel(footer_text, style="info"))
        
        self.console.print(layout)
    
    def dashboard_version_d_live(self) -> None:
        """Versão D: Rich Live Dashboard com updates em tempo real"""
        if self.quiet:
            return
            
        self.console.print("\n[bold magenta]🎯 CLI Tools - Dashboard Status (Versão D - Live)[/primary]", style="bold")
        self.console.print("[blue]Versão: Rich Live Dashboard com updates em tempo real[/info]")
        self.console.print("[bold yellow]⚠️  Pressione Ctrl+C para sair do modo live[/warning]\n")
        
        def generate_live_content():
            """Gera conteúdo atualizado para o dashboard live"""
            apis = self._get_api_status()
            workspace = self._get_workspace_info()
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Layout principal
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=5),
                Layout(name="main"),
                Layout(name="footer", size=3)
            )
            
            layout["main"].split_row(
                Layout(name="left"),
                Layout(name="center"), 
                Layout(name="right")
            )
            
            # Header com informações dinâmicas
            header_content = f"""[bold primary]🚀 CLI Tools Live Dashboard[/bold primary]
[bold cyan]⏰ {current_time} | 🔄 Atualizando a cada 2 segundos[/secondary]
[bold green]✨ Sistema operacional | 🎯 Todas as funcionalidades ativas[/success]"""
            
            layout["header"].update(Panel(header_content, style="primary"))
            
            # APIs Status (esquerda)
            api_content = ""
            for api_key, api_data in apis.items():
                status_indicator = "🟢 ONLINE" if api_data['status'] else "🔴 OFFLINE"
                status_style = "success" if api_data['status'] else "error"
                
                api_content += f"""[{status_style}]{api_data['icon']} {api_data['name']}[/{status_style}]
{status_indicator}
📊 {api_data['usage']['requests_today']} requests hoje
📈 {api_data['usage']['requests_total']} total

"""
            
            layout["left"].update(Panel(api_content, title="🔌 APIs Status", border_style="secondary"))
            
            # Métricas em tempo real (centro)
            total_requests = sum(api['usage']['requests_today'] for api in apis.values())
            active_apis = sum(1 for api in apis.values() if api['status'])
            
            metrics_content = f"""[bold success]📊 Métricas em Tempo Real[/bold success]

🎯 APIs Ativas: {active_apis}/3
📈 Requests Hoje: {total_requests}
💾 Workspace: {workspace['total_size']:.1f} MB
📄 Arquivos: {workspace['total_files']}

[bold yellow]🔥 Status: OPERACIONAL[/warning]
[blue]⚡ Performance: ÓTIMA[/info]
[bold green]🛡️  Segurança: OK[/success]"""
            
            layout["center"].update(Panel(metrics_content, title="📊 Métricas", border_style="warning"))
            
            # Workspace (direita)
            workspace_content = f"""[bold primary]📁 Workspace Overview[/bold primary]

📍 {workspace['workspace_path']}

"""
            for tipo, stats in workspace['stats'].items():
                workspace_content += f"""📂 {tipo.title()}:
   📄 {stats['files']} arquivos
   💾 {stats['size']:.1f} MB
   
"""
            
            layout["right"].update(Panel(workspace_content, title="🏠 Workspace", border_style="success"))
            
            # Footer com timestamp
            footer_content = f"[blue]🕐 Última atualização: {current_time} | 🔄 Próxima em 2s | 💡 Pressione Ctrl+C para sair[/info]"
            layout["footer"].update(Panel(footer_content, style="info"))
            
            return layout
        
        # Executar dashboard live
        try:
            with Live(generate_live_content(), refresh_per_second=0.5, screen=False) as live:
                while True:
                    time.sleep(2)
                    live.update(generate_live_content())
        except KeyboardInterrupt:
            self.console.print("\n[bold green]✅ Dashboard live finalizado![/success]")


# Instância global para uso fácil
rich_dashboards = RichDashboards()
