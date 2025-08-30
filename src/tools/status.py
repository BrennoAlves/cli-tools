"""Status - Verificação de APIs e sistema."""

import os
import shutil
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import requests

console = Console()


def show_status_cli():
    """Interface CLI para status com tema Dracula."""
    
    # Header com tema Dracula
    console.print()
    console.print("📊 STATUS", style="bold #bd93f9")
    console.print("═" * 50, style="#6272a4")
    console.print("Verificação de APIs e informações do sistema", style="#f8f8f2")
    console.print()
    
    # Status das APIs
    console.print("🔑 [#f1fa8c]STATUS DAS APIs[/]", style="#f8f8f2")
    console.print()
    
    api_table = Table(show_header=True, header_style="#bd93f9", border_style="#6272a4")
    api_table.add_column("API", style="#8be9fd", width=12)
    api_table.add_column("Status", width=15)
    api_table.add_column("Free Tier", style="#6272a4", width=20)
    
    # Pexels
    pexels_key = os.getenv('PEXELS_API_KEY', '')
    if pexels_key:
        try:
            headers = {'Authorization': pexels_key}
            response = requests.get('https://api.pexels.com/v1/search?query=test&per_page=1', 
                                  headers=headers, timeout=5)
            if response.status_code == 200:
                pexels_status = "[#50fa7b]✅ Funcionando[/]"
            else:
                pexels_status = "[#ff5555]❌ Chave inválida[/]"
        except:
            pexels_status = "[#f1fa8c]⚠️ Sem conexão[/]"
    else:
        pexels_status = "[#6272a4]⭕ Não configurado[/]"
    
    api_table.add_row("Pexels", pexels_status, "200 requests/hora")
    
    # Figma
    figma_token = os.getenv('FIGMA_TOKEN', '')
    if figma_token:
        try:
            headers = {'X-Figma-Token': figma_token}
            response = requests.get('https://api.figma.com/v1/me', 
                                  headers=headers, timeout=5)
            if response.status_code == 200:
                figma_status = "[#50fa7b]✅ Funcionando[/]"
            else:
                figma_status = "[#ff5555]❌ Token inválido[/]"
        except:
            figma_status = "[#f1fa8c]⚠️ Sem conexão[/]"
    else:
        figma_status = "[#6272a4]⭕ Não configurado[/]"
    
    api_table.add_row("Figma", figma_status, "30 requests/minuto")
    
    # GitHub
    github_token = os.getenv('GITHUB_TOKEN', '')
    if github_token:
        try:
            headers = {'Authorization': f'token {github_token}'}
            response = requests.get('https://api.github.com/user', 
                                  headers=headers, timeout=5)
            if response.status_code == 200:
                github_status = "[#50fa7b]✅ Funcionando[/]"
            else:
                github_status = "[#ff5555]❌ Token inválido[/]"
        except:
            github_status = "[#f1fa8c]⚠️ Sem conexão[/]"
    else:
        github_status = "[#6272a4]💡 Opcional[/]"
    
    api_table.add_row("GitHub", github_status, "5000 requests/hora")
    
    console.print(api_table)
    console.print()
    
    # Informações do sistema
    console.print("🖥️  [#f1fa8c]INFORMAÇÕES DO SISTEMA[/]", style="#f8f8f2")
    console.print()
    
    system_table = Table(show_header=True, header_style="#bd93f9", border_style="#6272a4")
    system_table.add_column("Item", style="#8be9fd", width=15)
    system_table.add_column("Valor", style="#f8f8f2")
    
    # Sistema operacional
    system_table.add_row("Sistema", f"{platform.system()} {platform.release()}")
    system_table.add_row("Arquitetura", platform.machine())
    system_table.add_row("Python", platform.python_version())
    
    # Git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        git_version = result.stdout.strip().split()[-1] if result.returncode == 0 else "❌ Não instalado"
    except:
        git_version = "❌ Não instalado"
    system_table.add_row("Git", git_version)
    
    # Espaço em disco
    try:
        disk_usage = shutil.disk_usage('.')
        total = disk_usage.total // (1024**3)  # GB
        free = disk_usage.free // (1024**3)    # GB
        used = total - free
        percent_used = (used / total) * 100
        
        if percent_used > 90:
            disk_status = f"[#ff5555]{used}GB/{total}GB ({percent_used:.1f}% usado)[/]"
        elif percent_used > 75:
            disk_status = f"[#f1fa8c]{used}GB/{total}GB ({percent_used:.1f}% usado)[/]"
        else:
            disk_status = f"[#50fa7b]{used}GB/{total}GB ({percent_used:.1f}% usado)[/]"
        
        system_table.add_row("Disco", disk_status)
    except:
        system_table.add_row("Disco", "❌ Não disponível")
    
    system_table.add_row("Diretório", str(Path.cwd()))
    
    console.print(system_table)
    console.print()
    
    # Pastas de saída
    console.print("📁 [#f1fa8c]PASTAS DE SAÍDA[/]", style="#f8f8f2")
    console.print()
    
    folders_table = Table(show_header=True, header_style="#bd93f9", border_style="#6272a4")
    folders_table.add_column("Pasta", style="#8be9fd", width=12)
    folders_table.add_column("Status", width=15)
    folders_table.add_column("Arquivos", style="#6272a4")
    
    folders = [
        ('imagens', 'Image'),
        ('figma', 'FigClone'), 
        ('repos', 'Repo')
    ]
    
    for folder, tool in folders:
        path = Path(folder)
        if path.exists():
            count = len(list(path.iterdir()))
            if count > 0:
                status = "[#50fa7b]📁 Existe[/]"
                files = f"{count} arquivos"
            else:
                status = "[#f1fa8c]📂 Vazia[/]"
                files = "0 arquivos"
        else:
            status = "[#6272a4]⭕ Não existe[/]"
            files = f"Criada pelo {tool}"
        
        folders_table.add_row(f"{folder}/", status, files)
    
    console.print(folders_table)
    console.print()
    
    # Dependências
    console.print("📦 [#f1fa8c]DEPENDÊNCIAS[/]", style="#f8f8f2")
    console.print()
    
    deps_info = []
    deps = ['textual', 'requests', 'click', 'rich', 'python-dotenv']
    
    for dep in deps:
        try:
            module = __import__(dep.replace('-', '_'))
            version = getattr(module, '__version__', 'desconhecida')
            deps_info.append(f"[#50fa7b]✅[/] {dep} v{version}")
        except ImportError:
            deps_info.append(f"[#ff5555]❌[/] {dep} não instalado")
    
    for dep_info in deps_info:
        console.print(f"  {dep_info}")
    
    console.print()
    
    # Resumo
    configured_apis = sum([
        1 if os.getenv('PEXELS_API_KEY') else 0,
        1 if os.getenv('FIGMA_TOKEN') else 0,
        1 if os.getenv('GITHUB_TOKEN') else 0
    ])
    
    if configured_apis == 3:
        summary_color = "#50fa7b"
        summary_icon = "🎉"
        summary_text = "Todas as APIs configuradas!"
    elif configured_apis >= 1:
        summary_color = "#f1fa8c"
        summary_icon = "⚠️"
        summary_text = f"{configured_apis}/3 APIs configuradas"
    else:
        summary_color = "#ff5555"
        summary_icon = "❌"
        summary_text = "Nenhuma API configurada"
    
    console.print(Panel.fit(
        f"[{summary_color}]{summary_icon} {summary_text}[/]\n\n"
        f"[#f8f8f2]Para configurar APIs: [/][#50fa7b]nano .env[/]\n"
        f"[#f8f8f2]Para reinstalar: [/][#50fa7b]./install.sh[/]",
        title="[#bd93f9]Resumo[/]",
        border_style=summary_color
    ))


def check_dependencies():
    """Verifica dependências instaladas."""
    deps = ['textual', 'requests', 'click', 'rich', 'python-dotenv']
    missing = []
    
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            missing.append(dep)
    
    return missing


# Manter compatibilidade
def show_status():
    """Alias para compatibilidade."""
    show_status_cli()

def run_system_ui():
    """Alias para compatibilidade."""
    show_status_cli()
