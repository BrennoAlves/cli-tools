#!/usr/bin/env python3
"""CLI Tools v0.1 - Kit de ferramentas para desenvolvedores."""

import click
import sys
import os

def show_menu():
    """Menu navegável por setas com tema Dracula."""
    from rich.console import Console
    
    console = Console()
    
    # ASCII Art
    ascii_art = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""
    
    options = [
        "🖼️  Image - Buscar imagens no Pexels",
        "🎨  FigClone - Download de designs do Figma", 
        "📦  Repo - Clonar repositórios do GitHub",
        "📊  Status - Verificar APIs e sistema",
        "🚪  Sair"
    ]
    
    selected = 0
    
    def print_menu():
        # Limpar sem piscar
        print('\033[2J\033[H', end='')
        
        # ASCII Art em roxo Dracula
        console.print(ascii_art, style="bold #bd93f9")
        
        # Subtítulo centralizado em relação ao ASCII (70 chars)
        subtitle = "v0.1 - Kit de ferramentas para desenvolvedores"
        padding = (70 - len(subtitle)) // 2
        console.print(" " * padding + subtitle, style="#6272a4")
        console.print()
        
        for i, option in enumerate(options):
            if i == selected:
                # Selecionado: verde Dracula com fundo
                console.print(f"  ▶ {option}", style="bold #50fa7b on #44475a")
            else:
                # Normal: texto claro Dracula
                console.print(f"    {option}", style="#f8f8f2")
        
        console.print()
        console.print("  ↑↓ Navegar  Enter Selecionar  q Sair", style="#6272a4")
    
    print_menu()
    
    while True:
        try:
            # Ler tecla sem Enter
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
            if key == '\x1b':  # ESC sequence
                key += sys.stdin.read(2)
                if key == '\x1b[A':  # Up arrow
                    selected = (selected - 1) % len(options)
                    print_menu()
                elif key == '\x1b[B':  # Down arrow
                    selected = (selected + 1) % len(options)
                    print_menu()
            elif key == '\r' or key == '\n':  # Enter
                print('\033[2J\033[H', end='')
                if selected == 0:
                    from .tools.image import run_image_cli
                    run_image_cli()
                    console.print("\n  💡 Pressione Enter para voltar ao menu...", style="#6272a4")
                    input()
                    print_menu()
                elif selected == 1:
                    from .tools.figclone import run_figclone_cli
                    run_figclone_cli()
                    console.print("\n  💡 Pressione Enter para voltar ao menu...", style="#6272a4")
                    input()
                    print_menu()
                elif selected == 2:
                    from .tools.repo import run_repo_cli
                    run_repo_cli()
                    console.print("\n  💡 Pressione Enter para voltar ao menu...", style="#6272a4")
                    input()
                    print_menu()
                elif selected == 3:
                    from .tools.status import show_status_cli
                    show_status_cli()
                    console.print("\n  💡 Pressione Enter para voltar ao menu...", style="#6272a4")
                    input()
                    print_menu()
                elif selected == 4:
                    console.print("  👋 Até logo!", style="#50fa7b")
                    break
            elif key == 'q' or key == '\x03':  # q ou Ctrl+C
                console.print("  👋 Até logo!", style="#50fa7b")
                break
                
        except (ImportError, OSError):
            # Fallback para sistemas sem termios
            console.print("  💡 Use as opções numéricas:", style="#f1fa8c")
            choice = input("  Escolha (1-4, 0 para sair): ")
            
            if choice == '1':
                from .tools.image import run_image_cli
                run_image_cli()
                console.print("\n  💡 Pressione Enter para voltar ao menu...", style="#6272a4")
                input()
                print_menu()
            elif choice == '2':
                from .tools.figclone import run_figclone_cli
                run_figclone_cli()
                console.print("\n  💡 Pressione Enter para voltar ao menu...", style="#6272a4")
                input()
                print_menu()
            elif choice == '3':
                from .tools.repo import run_repo_cli
                run_repo_cli()
                console.print("\n  💡 Pressione Enter para voltar ao menu...", style="#6272a4")
                input()
                print_menu()
            elif choice == '4':
                from .tools.status import show_status_cli
                show_status_cli()
                console.print("\n  💡 Pressione Enter para voltar ao menu...", style="#6272a4")
                input()
                print_menu()
            elif choice == '0':
                console.print("  👋 Até logo!", style="#50fa7b")
                break
            else:
                console.print("  ❌ Opção inválida", style="#ff5555")
                console.print("  💡 Pressione Enter para continuar...", style="#6272a4")
                input()
                print_menu()


@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0", prog_name="CLI Tools")
@click.pass_context
def cli(ctx):
    """CLI Tools v0.1 - Kit de ferramentas para desenvolvedores."""
    if ctx.invoked_subcommand is None:
        show_menu()


@cli.command()
@click.argument('query')
@click.option('--count', '-c', default=1, help='Número de imagens')
@click.option('--orientation', type=click.Choice(['landscape', 'portrait', 'square']))
@click.option('--size', type=click.Choice(['large', 'medium', 'small']))
@click.option('--color', help='Cor predominante')
def image(query, count, orientation, size, color):
    """Buscar imagens no Pexels."""
    from .tools.image import search_images
    search_images(query, count, orientation, size, color)


@cli.command()
@click.argument('file_key')
@click.option('--format', '-f', default='png', help='Formato: png/jpg/svg/pdf')
@click.option('--scale', default=1.0, help='Escala de export')
@click.option('--nodes', help='IDs dos nodes específicos')
def figclone(file_key, format, scale, nodes):
    """Download de designs do Figma."""
    from .tools.figclone import export_figma
    export_figma(file_key, format, scale, nodes)


@cli.command()
@click.argument('repo')
@click.option('--query', '-q', help='Buscar nos arquivos')
@click.option('--depth', type=int, help='Profundidade do clone')
def repo(repo, query, depth):
    """Clonar repositório do GitHub."""
    from .tools.repo import clone_repository
    clone_repository(repo, query, depth)


@cli.command()
def status():
    """Status das APIs e sistema."""
    from .tools.status import show_status_cli
    show_status_cli()


if __name__ == "__main__":
    cli()


@cli.command()
@click.argument('query')
@click.option('--count', '-c', default=1, help='Número de imagens')
@click.option('--orientation', type=click.Choice(['landscape', 'portrait', 'square']))
@click.option('--size', type=click.Choice(['large', 'medium', 'small']))
@click.option('--color', help='Cor predominante')
def search(query, count, orientation, size, color):
    """Buscar imagens no Pexels."""
    from .tools.pexels import search_images
    search_images(query, count, orientation, size, color)


@cli.command()
@click.argument('file_key')
@click.option('--format', '-f', default='png', help='Formato: png/jpg/svg/pdf')
@click.option('--scale', default=1.0, help='Escala de export')
@click.option('--nodes', help='IDs dos nodes específicos')
def figma(file_key, format, scale, nodes):
    """Download de designs do Figma."""
    from .tools.figma import export_figma
    export_figma(file_key, format, scale, nodes)


@cli.command()
@click.argument('repo')
@click.option('--query', '-q', help='Buscar nos arquivos')
@click.option('--depth', type=int, help='Profundidade do clone')
def repo(repo, query, depth):
    """Clonar repositório do GitHub."""
    from .tools.repo import clone_repository
    clone_repository(repo, query, depth)


@cli.command()
def status():
    """Status do sistema."""
    from .tools.system import show_status
    show_status()


if __name__ == "__main__":
    cli()
