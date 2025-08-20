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
            # Ferramentas em ordem alfabética
            '1': {'nome': 'figma', 'desc': 'Extrair designs do Figma'},
            '2': {'nome': 'repo', 'desc': 'Baixar repositório com IA'},
            '3': {'nome': 'search', 'desc': 'Buscar e baixar imagens'},
            # Informações e monitoramento
            '4': {'nome': 'info', 'desc': 'Status e custos das APIs'},
            # Configurações
            '5': {'nome': 'config', 'desc': 'Configurações do sistema'},
            '6': {'nome': 'help', 'desc': 'Ajuda e exemplos'},
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
                elif cmd == 'info':
                    self._submenu_info()
                elif cmd == 'config':
                    self._submenu_config()
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
        import os
        
        try:
            # Para comandos interativos como status, não capturar output
            if comando in ['status', 'config']:
                result = subprocess.run([
                    sys.executable, '-m', 'src.main', comando
                ])
            else:
                # Usar mesmo ambiente que o comando cli-tools
                env = os.environ.copy()
                env['PYTHONPATH'] = f"{os.path.expanduser('~/.local/share/cli-tools')}:{env.get('PYTHONPATH', '')}"
                
                result = subprocess.run([
                    sys.executable, '-m', 'src.main', comando
                ], capture_output=True, text=True, env=env)
                
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
        import os
        
        try:
            # Usar mesmo ambiente que o comando cli-tools
            env = os.environ.copy()
            env['PYTHONPATH'] = f"{os.path.expanduser('~/.local/share/cli-tools')}:{env.get('PYTHONPATH', '')}"
            
            result = subprocess.run([
                sys.executable, '-m', 'src.main', 'search', query, '--count', count
            ], capture_output=True, text=True, env=env)
            
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")
                
        except Exception as e:
            self.console.print(f"\n[red]Erro: {e}[/red]")
            self.console.print(f"[red]Erro: {e}[/red]")
    
    def _executar_figma(self):
        """Extração do Figma"""
        file_key = Prompt.ask("[cyan]Chave do arquivo Figma[/cyan]")
        
        import subprocess
        import sys
        import os
        
        try:
            # Usar mesmo ambiente que o comando cli-tools
            env = os.environ.copy()
            env['PYTHONPATH'] = f"{os.path.expanduser('~/.local/share/cli-tools')}:{env.get('PYTHONPATH', '')}"
            
            result = subprocess.run([
                sys.executable, '-m', 'src.main', 'figma', file_key
            ], capture_output=True, text=True, env=env)
            
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Erro: {e}[/red]")
    
    def _executar_repo(self):
        """Download de repositório"""
        from rich.prompt import Confirm
        import os
        
        repo = Prompt.ask("[cyan]Repositório (user/repo)[/cyan]")
        
        # Verificar se tem API do Gemini configurada
        tem_gemini = os.getenv('GEMINI_API_KEY') is not None
        
        if not tem_gemini:
            self.console.print("[yellow]⚠️  API do Gemini não configurada[/yellow]")
            self.console.print("[yellow]📦 Baixando repositório completo...[/yellow]")
            
            if Confirm.ask("Continuar com download completo?", default=True):
                self._executar_repo_completo(repo)
            return
        
        # Com API configurada, perguntar sobre query
        usar_ia = Confirm.ask("[cyan]Usar IA para seleção inteligente?[/cyan]", default=True)
        
        if usar_ia:
            query = Prompt.ask("[cyan]Query para IA[/cyan]", default="arquivos principais")
            self._executar_repo_com_ia(repo, query)
        else:
            self._executar_repo_completo(repo)
    
    def _executar_repo_completo(self, repo):
        """Baixar repositório completo"""
        import subprocess
        import sys
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'src.main', 'repo', repo, '--all'
            ], capture_output=True, text=True)
            
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Erro: {e}[/red]")
    
    def _executar_repo_com_ia(self, repo, query):
        """Baixar repositório com IA"""
        import subprocess
        import sys
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'src.main', 'repo', repo, query
            ], capture_output=True, text=True)
            
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[red]{result.stderr}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Erro: {e}[/red]")
    
    def _submenu_info(self):
        """Submenu de informações e monitoramento"""
        from rich.prompt import Confirm
        
        while True:
            self.console.print("\n[bold cyan]📊 Informações e Monitoramento[/bold cyan]")
            
            opcoes_info = {
                '1': {'nome': 'status', 'desc': 'Ver status do sistema'},
                '2': {'nome': 'costs', 'desc': 'Monitorar custos das APIs'},
                'b': {'nome': 'back', 'desc': 'Voltar ao menu principal'}
            }
            
            # Mostrar opções
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Opção", style="cyan", width=8)
            table.add_column("Comando", style="green", width=10)
            table.add_column("Descrição", style="white")
            
            for opcao, info in opcoes_info.items():
                table.add_row(opcao, info['nome'], info['desc'])
            
            self.console.print(table)
            
            escolha = Prompt.ask(
                "[cyan]Digite sua escolha[/cyan]",
                choices=list(opcoes_info.keys()),
                default="b"
            )
            
            if escolha == 'b':
                break
            
            cmd = opcoes_info[escolha]['nome']
            self.console.print(f"\n[green]Executando: {cmd}[/green]")
            self._executar_comando(cmd)
            
            if not Confirm.ask("\nVoltar ao submenu?", default=True):
                break
    
    def _submenu_config(self):
        """Submenu de configurações"""
        from rich.prompt import Confirm
        
        while True:
            self.console.print("\n[bold cyan]⚙️ Configurações do Sistema[/bold cyan]")
            
            opcoes_config = {
                '1': {'nome': 'setup', 'desc': 'Configurar sistema inicial (chaves APIs)'},
                '2': {'nome': 'ai-config', 'desc': 'Configurar comportamento da IA'},
                '3': {'nome': 'config', 'desc': 'Gerenciar configurações gerais'},
                'b': {'nome': 'back', 'desc': 'Voltar ao menu principal'}
            }
            
            # Mostrar opções
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Opção", style="cyan", width=8)
            table.add_column("Comando", style="green", width=12)
            table.add_column("Descrição", style="white")
            
            for opcao, info in opcoes_config.items():
                table.add_row(opcao, info['nome'], info['desc'])
            
            self.console.print(table)
            
            escolha = Prompt.ask(
                "[cyan]Digite sua escolha[/cyan]",
                choices=list(opcoes_config.keys()),
                default="b"
            )
            
            if escolha == 'b':
                break
            
            cmd = opcoes_config[escolha]['nome']
            self.console.print(f"\n[green]Executando: {cmd}[/green]")
            
            if cmd == 'setup':
                self._executar_setup()
            elif cmd == 'ai-config':
                self._executar_ai_config()
            else:
                self._executar_comando(cmd)
            
            if not Confirm.ask("\nVoltar ao submenu?", default=True):
                break
    
    def _executar_setup(self):
        """Configuração inicial do sistema"""
        self.console.print("\n[bold green]🔧 Configuração Inicial do Sistema[/bold green]")
        self.console.print("Vamos configurar suas chaves de API uma por uma.\n")
        
        # Configurar cada API
        self._configurar_api_pexels()
        self._configurar_api_figma()
        self._configurar_api_gemini()
        
        self.console.print("\n[bold green]✅ Configuração inicial concluída![/bold green]")
        self.console.print("🎉 Sistema pronto para uso!")
    
    def _configurar_api_pexels(self):
        """Configurar API do Pexels"""
        from rich.prompt import Confirm
        import os
        from pathlib import Path
        
        if not Confirm.ask("\n🖼️ Configurar API do Pexels (busca de imagens)?", default=True):
            return
        
        self.console.print("\n[cyan]📝 Para obter sua chave do Pexels:[/cyan]")
        self.console.print("1. Acesse: https://www.pexels.com/api/")
        self.console.print("2. Crie uma conta gratuita")
        self.console.print("3. Copie sua API Key")
        
        while True:
            chave = Prompt.ask("\n[yellow]Cole sua chave do Pexels (ou 'pular' para pular)[/yellow]")
            
            if chave.lower() == 'pular':
                self.console.print("[yellow]⏭️ Pexels pulado[/yellow]")
                break
            
            # Validar chave (teste simples)
            if len(chave) > 10 and not ' ' in chave:
                self._salvar_chave_env('PEXELS_API_KEY', chave)
                self.console.print("[green]✅ Chave do Pexels salva![/green]")
                break
            else:
                self.console.print("[red]❌ Chave inválida. Tente novamente.[/red]")
    
    def _configurar_api_figma(self):
        """Configurar API do Figma"""
        from rich.prompt import Confirm
        
        if not Confirm.ask("\n🎨 Configurar API do Figma (extração de designs)?", default=True):
            return
        
        self.console.print("\n[cyan]📝 Para obter seu token do Figma:[/cyan]")
        self.console.print("1. Acesse: https://www.figma.com/developers/api")
        self.console.print("2. Faça login na sua conta")
        self.console.print("3. Gere um Personal Access Token")
        
        while True:
            token = Prompt.ask("\n[yellow]Cole seu token do Figma (ou 'pular' para pular)[/yellow]")
            
            if token.lower() == 'pular':
                self.console.print("[yellow]⏭️ Figma pulado[/yellow]")
                break
            
            # Validar token (teste simples)
            if len(token) > 20 and token.startswith('figd_'):
                self._salvar_chave_env('FIGMA_API_TOKEN', token)
                self.console.print("[green]✅ Token do Figma salvo![/green]")
                break
            else:
                self.console.print("[red]❌ Token inválido. Deve começar com 'figd_'.[/red]")
    
    def _configurar_api_gemini(self):
        """Configurar API do Gemini"""
        from rich.prompt import Confirm
        
        if not Confirm.ask("\n🤖 Configurar API do Google Gemini (IA para análise)?", default=True):
            return
        
        self.console.print("\n[cyan]📝 Para obter sua chave do Gemini:[/cyan]")
        self.console.print("1. Acesse: https://makersuite.google.com/app/apikey")
        self.console.print("2. Faça login com sua conta Google")
        self.console.print("3. Crie uma nova API Key")
        
        while True:
            chave = Prompt.ask("\n[yellow]Cole sua chave do Gemini (ou 'pular' para pular)[/yellow]")
            
            if chave.lower() == 'pular':
                self.console.print("[yellow]⏭️ Gemini pulado[/yellow]")
                break
            
            # Validar chave (teste simples)
            if len(chave) > 30 and chave.startswith('AIza'):
                self._salvar_chave_env('GEMINI_API_KEY', chave)
                self.console.print("[green]✅ Chave do Gemini salva![/green]")
                break
            else:
                self.console.print("[red]❌ Chave inválida. Deve começar com 'AIza'.[/red]")
    
    def _salvar_chave_env(self, nome_var, valor):
        """Salva chave no arquivo .env"""
        from pathlib import Path
        import os
        
        # Determinar arquivo .env (projeto atual ou global)
        env_paths = [
            Path.cwd() / '.env',
            Path.home() / '.local/share/cli-tools/.env'
        ]
        
        env_file = None
        for path in env_paths:
            if path.exists():
                env_file = path
                break
        
        if not env_file:
            env_file = env_paths[0]  # Criar no diretório atual
        
        # Ler arquivo existente
        lines = []
        if env_file.exists():
            with open(env_file, 'r') as f:
                lines = f.readlines()
        
        # Atualizar ou adicionar variável
        found = False
        for i, line in enumerate(lines):
            if line.startswith(f'{nome_var}='):
                lines[i] = f'{nome_var}={valor}\n'
                found = True
                break
        
        if not found:
            lines.append(f'{nome_var}={valor}\n')
        
        # Salvar arquivo
        env_file.parent.mkdir(parents=True, exist_ok=True)
        with open(env_file, 'w') as f:
            f.writelines(lines)
    
    def _executar_ai_config(self):
        """Configurar comportamento da IA"""
        from rich.prompt import Confirm
        
        self.console.print("\n[bold green]🤖 Configuração do Comportamento da IA[/bold green]")
        self.console.print("Configure como a IA deve se comportar nas ferramentas:\n")
        
        opcoes = {
            'silencioso': 'Execução silenciosa - apenas resultados',
            'equilibrado': 'Equilibrado - informações essenciais',
            'declarativo': 'Declarativo - passo a passo detalhado'
        }
        
        self.console.print("[cyan]Opções disponíveis:[/cyan]")
        for key, desc in opcoes.items():
            self.console.print(f"  • [yellow]{key}[/yellow]: {desc}")
        
        escolha = Prompt.ask(
            "\n[yellow]Como a IA deve se comportar?[/yellow]",
            choices=list(opcoes.keys()),
            default="equilibrado"
        )
        
        self._salvar_chave_env('AI_BEHAVIOR', escolha)
        self.console.print(f"\n[green]✅ Comportamento da IA configurado para: {escolha}[/green]")
        self.console.print(f"[dim]{opcoes[escolha]}[/dim]")

# Instância global
navegador_cli = NavegadorCLI()
