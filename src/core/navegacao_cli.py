"""
Sistema de navegação principal, utilizando o menu interativo moderno.
"""

import subprocess
import sys
from pathlib import Path

from .visuals import console, print_header, print_info, print_error
from src.menu_app.interactive_menu import show_interactive_menu
from .rich_dashboards import modern_dashboard

class NavegadorCLI:
    """Coordena a navegação principal através do menu interativo."""

    def __init__(self):
        self.base_command = [sys.executable, str(Path(__file__).parent.parent / "main.py")]

    def _run_command(self, command_args):
        try:
            subprocess.run(self.base_command + command_args, check=True)
        except subprocess.CalledProcessError as e:
            print_error(f"Erro ao executar o comando: {e}")
        except FileNotFoundError:
            print_error("Comando principal 'main.py' não encontrado.")

    def navegar(self):
        """Inicia o loop do menu principal."""
        while True:
            menu_options = [
                {"id": "search", "icon": "🔍", "title": "Buscar Imagens", "description": "Encontre e baixe imagens da web.", "action": "iniciar busca"},
                {"id": "figma", "icon": "🎨", "title": "Extrair do Figma", "description": "Extraia componentes e estilos de seus designs no Figma.", "action": "iniciar extração"},
                {"id": "repo", "icon": "📦", "title": "Analisar Repositório", "description": "Use IA para analisar e baixar arquivos de repositórios GitHub.", "action": "analisar repositório"},
                {"id": "status", "icon": "📊", "title": "Dashboard de Status", "description": "Visualize o status completo do sistema, APIs e workspace.", "action": "ver dashboard"},
                {"id": "config", "icon": "⚙️", "title": "Configurações", "description": "Gerencie chaves de API, diretórios e comportamento da IA.", "action": "abrir configurações"},
                {"id": "exit", "icon": "👋", "title": "Sair", "description": "Encerrar a aplicação.", "action": "sair"},
            ]

            selected_id = show_interactive_menu(menu_options)

            if selected_id == "search":
                self._run_command(["search", "--help"]) # Placeholder
            elif selected_id == "figma":
                self._run_command(["figma", "--help"]) # Placeholder
            elif selected_id == "repo":
                self._run_command(["repo", "--help"]) # Placeholder
            elif selected_id == "status":
                modern_dashboard.display()
            elif selected_id == "config":
                self._run_command(["config", "--show-dirs"]) # Placeholder
            elif selected_id == "exit":
                console.print("\n[primary]Até logo![/primary]")
                break
            else:
                # O menu textual já não permite isso, mas é uma boa prática.
                print_error("Opção inválida selecionada.")
                break

navegador_cli = NavegadorCLI()