"""
Navegação CLI - Sistema de navegação simples
"""

import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

console = Console()

class NavegadorCLI:
    """Sistema de navegação simples"""
    
    def __init__(self):
        self.console = Console()
        self.comandos = {
            '1': {'nome': 'status', 'desc': 'Ver status do sistema'},
            '2': {'nome': 'search', 'desc': 'Buscar e baixar imagens'},
            '3': {'nome': 'figma', 'desc': 'Extrair designs do Figma'},
            '4': {'nome': 'repo', 'desc': 'Baixar repositório com IA'},
            '5': {'nome': 'config', 'desc': 'Gerenciar configurações'},
            '6': {'nome': 'costs', 'desc': 'Monitorar custos das APIs'},
            '7': {'nome': 'help', 'desc': 'Ajuda e exemplos'},
            'q': {'nome': 'quit', 'desc': 'Sair'}
        }
    
    def mostrar_menu(self):
        """Mostrar menu simples"""
        self.console.clear()
        
        header = Panel.fit(
            "[bold blue]🛠️ CLI Tools[/bold blue]\n"
            "[dim]Escolha uma opção:[/dim]",
            border_style="blue"
        )
        self.console.print(header)
        self.console.print()
        
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Opção", style="cyan", width=8)
        table.add_column("Comando", style="green")
        table.add_column("Descrição", style="white")
        
        for key, cmd in self.comandos.items():
            table.add_row(key, cmd['nome'], cmd['desc'])
        
        self.console.print(table)
        self.console.print()
    
    def navegar(self):
        """Navegação simples"""
        try:
            while True:
                self.mostrar_menu()
                
                escolha = Prompt.ask(
                    "[cyan]Digite sua escolha[/cyan]",
                    choices=list(self.comandos.keys()),
                    default="q"
                )
                
                if escolha == 'q':
                    self.console.print("\n[yellow]Saindo...[/yellow]")
                    break
                
                cmd = self.comandos[escolha]['nome']
                self.console.print(f"\n[green]Executando: {cmd}[/green]")
                
                if cmd == 'search':
                    self._executar_search()
                elif cmd == 'figma':
                    self._executar_figma()
                elif cmd == 'repo':
                    self._executar_repo()
                else:
                    self._executar_comando(cmd)
                
                if not Confirm.ask("\n[dim]Voltar ao menu?[/dim]", default=True):
                    break
                    
        except KeyboardInterrupt:
            self.console.print("\n\n[yellow]Saindo...[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]Erro: {e}[/red]")
    
    def _executar_comando(self, comando):
        """Executar comando simples"""
        import subprocess
        import sys
        
        try:
            result = subprocess.run([
                sys.executable, 'cli_tools/main.py', comando
            ], capture_output=True, text=True, cwd='/home/desk/cli-tools')
            
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Erro ao executar {comando}: {e}[/red]")
    
    def _executar_search(self):
        """Busca de imagens"""
        query = Prompt.ask("[cyan]Termo de busca[/cyan]")
        count = Prompt.ask("[cyan]Quantas imagens?[/cyan]", default="3")
        
        import subprocess
        import sys
        
        try:
            result = subprocess.run([
                sys.executable, 'cli_tools/main.py', 'search', query, '--count', count
            ], capture_output=True, text=True, cwd='/home/desk/cli-tools')
            
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Erro: {e}[/red]")
    
    def _executar_figma(self):
        """Extração do Figma"""
        file_key = Prompt.ask("[cyan]Chave do arquivo Figma[/cyan]")
        
        import subprocess
        import sys
        
        try:
            result = subprocess.run([
                sys.executable, 'cli_tools/main.py', 'figma', file_key
            ], capture_output=True, text=True, cwd='/home/desk/cli-tools')
            
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Erro: {e}[/red]")
    
    def _executar_repo(self):
        """Download de repositório"""
        repo = Prompt.ask("[cyan]Repositório (user/repo)[/cyan]")
        query = Prompt.ask("[cyan]Query para IA[/cyan]", default="arquivos principais")
        
        import subprocess
        import sys
        
        try:
            result = subprocess.run([
                sys.executable, 'cli_tools/main.py', 'repo', repo, query
            ], capture_output=True, text=True, cwd='/home/desk/cli-tools')
            
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Erro: {e}[/red]")

# Instância global
navegador_cli = NavegadorCLI()
