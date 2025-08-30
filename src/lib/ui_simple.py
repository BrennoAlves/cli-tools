"""
Interface simples estilo Gemini CLI.
"""

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

console = Console()

def show_header():
    """Mostra cabeçalho do sistema."""
    header = Text("CLI TOOLS v2.0", style="bold blue")
    console.print(Panel(header, style="blue"))
    console.print()

def show_menu():
    """Mostra menu principal."""
    menu_text = """Escolha uma opção:

  [bold cyan]1.[/] 🔍 Buscar imagens
  [bold cyan]2.[/] 🎨 Extrair Figma  
  [bold cyan]3.[/] 📦 Baixar repositório
  [bold cyan]4.[/] 📊 Status do sistema
  [bold cyan]5.[/] ⚙️  Configurações
  [bold cyan]6.[/] ❌ Sair"""
    
    rprint(menu_text)
    console.print()

def get_menu_choice():
    """Obtém escolha do menu."""
    while True:
        try:
            choice = IntPrompt.ask("", choices=["1", "2", "3", "4", "5", "6"])
            return choice
        except KeyboardInterrupt:
            console.print("\n👋 Até logo!")
            return 6

def search_flow():
    """Fluxo conversacional para busca de imagens."""
    console.print("[bold green]🔍 BUSCAR IMAGENS[/]")
    console.print()
    
    # Consulta
    query = Prompt.ask("Consulta")
    if not query.strip():
        console.print("[red]❌ Consulta não pode estar vazia[/]")
        return
    
    # Quantidade
    count = IntPrompt.ask("Quantidade", default=1)
    if count < 1 or count > 80:
        console.print("[red]❌ Quantidade deve ser entre 1 e 80[/]")
        return
    
    # Orientação
    orientation = Prompt.ask(
        "Orientação", 
        choices=["landscape", "portrait", "square"], 
        default="landscape"
    )
    
    # Pasta
    output = Prompt.ask("Pasta", default="padrão")
    if output == "padrão":
        output = None
    
    # Confirmação
    console.print()
    console.print(f"[yellow]Buscar {count} imagem(ns) de '{query}' ({orientation})[/]")
    if not Confirm.ask("Confirmar busca?", default=False):
        console.print("[yellow]❌ Busca cancelada[/]")
        return
    
    # Executar
    console.print()
    with console.status(f"[green]Buscando {count} imagens de '{query}'..."):
        try:
            from ..lib.apis import pexels_download_files
            files = pexels_download_files(query, count=count, orientation=orientation, output=output)
            
            if files:
                console.print(f"[green]✅ {len(files)} imagem(ns) baixada(s):[/]")
                for f in files[:3]:  # Mostrar só as 3 primeiras
                    console.print(f"  📁 {f['nome']} ({f['tamanho']})")
                if len(files) > 3:
                    console.print(f"  ... e mais {len(files) - 3} arquivo(s)")
            else:
                console.print("[yellow]⚠️ Nenhuma imagem encontrada[/]")
                
        except Exception as e:
            console.print(f"[red]❌ Erro: {e}[/]")

def figma_flow():
    """Fluxo conversacional para Figma."""
    console.print("[bold green]🎨 EXTRAIR FIGMA[/]")
    console.print()
    
    # File Key
    file_key = Prompt.ask("File Key do Figma")
    if not file_key.strip() or len(file_key.strip()) < 10:
        console.print("[red]❌ File Key inválido[/]")
        return
    
    # Formato
    format = Prompt.ask("Formato", choices=["png", "jpg", "svg"], default="png")
    
    # Máximo
    max_images = IntPrompt.ask("Máximo de imagens", default=10)
    
    # Confirmação
    console.print()
    console.print(f"[yellow]Extrair designs de {file_key} ({format}, max {max_images})[/]")
    if not Confirm.ask("Confirmar extração?", default=False):
        console.print("[yellow]❌ Extração cancelada[/]")
        return
    
    # Executar
    console.print()
    with console.status("[green]Extraindo designs do Figma..."):
        try:
            from ..lib.apis import figma_download_files
            files = figma_download_files(file_key, fmt=format, max_images=max_images)
            
            if files:
                console.print(f"[green]✅ {len(files)} arquivo(s) extraído(s):[/]")
                for f in files[:3]:
                    console.print(f"  📁 {f['nome']} ({f['tamanho']})")
                if len(files) > 3:
                    console.print(f"  ... e mais {len(files) - 3} arquivo(s)")
            else:
                console.print("[yellow]⚠️ Nenhum arquivo gerado[/]")
                
        except Exception as e:
            console.print(f"[red]❌ Erro: {e}[/]")

def repo_flow():
    """Fluxo conversacional para repositório."""
    console.print("[bold green]📦 BAIXAR REPOSITÓRIO[/]")
    console.print()
    
    # Repositório
    repo = Prompt.ask("Repositório (user/repo)")
    if not repo.strip() or "/" not in repo:
        console.print("[red]❌ Formato inválido. Use: usuario/repositorio[/]")
        return
    
    # Query IA
    query = Prompt.ask("Query para IA (opcional)", default="")
    if query == "":
        query = None
    
    # Opções
    no_ai = Confirm.ask("Baixar sem IA?", default=False)
    all_files = Confirm.ask("Baixar todos os arquivos?", default=False)
    
    # Confirmação
    console.print()
    console.print(f"[yellow]Baixar {repo}" + (f" com query '{query}'" if query else "")[/])
    if not Confirm.ask("Confirmar download?", default=False):
        console.print("[yellow]❌ Download cancelado[/]")
        return
    
    # Executar
    console.print()
    with console.status(f"[green]Baixando repositório {repo}..."):
        try:
            from ..lib.apis import repo_download_auto
            path = repo_download_auto(repo, query=query, no_ai=no_ai, all_clone=all_files)
            console.print(f"[green]✅ Repositório baixado em: {path}[/]")
        except Exception as e:
            console.print(f"[red]❌ Erro: {e}[/]")

def status_flow():
    """Mostra status do sistema."""
    console.print("[bold green]📊 STATUS DO SISTEMA[/]")
    console.print()
    
    try:
        from ..lib.utils import get_system_status
        status = get_system_status()
        
        # Workspace
        console.print(f"[cyan]Workspace:[/] {status.get('workspace', 'N/A')}")
        console.print(f"[cyan]Tema:[/] {status.get('theme', 'N/A')}")
        console.print()
        
        # APIs
        console.print("[cyan]APIs:[/]")
        apis = status.get('apis', {})
        for api, configured in apis.items():
            icon = "✅" if configured else "❌"
            console.print(f"  {icon} {api}")
            
    except Exception as e:
        console.print(f"[red]❌ Erro ao carregar status: {e}[/]")
    
    console.print()
    Prompt.ask("Pressione Enter para continuar", default="")

def config_flow():
    """Fluxo de configuração."""
    console.print("[bold green]⚙️ CONFIGURAÇÕES[/]")
    console.print()
    
    console.print("[yellow]Funcionalidade em desenvolvimento...[/]")
    console.print()
    Prompt.ask("Pressione Enter para continuar", default="")

def run():
    """Executa a interface principal."""
    try:
        while True:
            console.clear()
            show_header()
            show_menu()
            
            choice = get_menu_choice()
            
            console.print()
            
            if choice == 1:
                search_flow()
            elif choice == 2:
                figma_flow()
            elif choice == 3:
                repo_flow()
            elif choice == 4:
                status_flow()
            elif choice == 5:
                config_flow()
            elif choice == 6:
                console.print("[green]👋 Até logo![/]")
                break
            
            if choice != 6:
                console.print()
                Prompt.ask("Pressione Enter para continuar", default="")
                
    except KeyboardInterrupt:
        console.print("\n[green]👋 Até logo![/]")
    except Exception as e:
        console.print(f"\n[red]❌ Erro inesperado: {e}[/]")
