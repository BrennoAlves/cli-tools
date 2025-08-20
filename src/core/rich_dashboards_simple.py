"""
Dashboard simplificado, ideal para logs e ambientes sem suporte a Rich.
"""

from .config import validar_chaves_api
from .controle_uso import controlador_uso
from .config_diretorios import ConfigDiretorios
from .visuals import print_header, print_info, print_success, print_error

class SimpleDashboard:
    """Gera um output de status simples, em texto puro."""

    def __init__(self):
        self.config_dirs = ConfigDiretorios()

    def display(self):
        """Exibe o status formatado como texto."""
        print_header("Status do Sistema (Modo Simplificado)")

        # Status das APIs
        print_info("\n--- Status das APIs ---")
        problemas = validar_chaves_api()
        apis = ['pexels', 'figma', 'gemini']
        for api in apis:
            if api not in problemas:
                print_success(f"{api.title()}: Operacional")
            else:
                print_error(f"{api.title()}: Falha - {problemas[api]}")

        # Status do Workspace
        print_info("\n--- Status do Workspace ---")
        stats = self.config_dirs.obter_estatisticas_workspace()
        for dir_name, dir_stats in stats["directories"].items():
            print_info(f"{dir_name.title()}: {dir_stats['files']} arquivos, {dir_stats['size_mb']:.2f} MB")
        
        print_success(f"Total: {stats['total_files']} arquivos, {stats['total_size_mb']:.2f} MB")

# Instância para fácil acesso
simple_dashboard = SimpleDashboard()