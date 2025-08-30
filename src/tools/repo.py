"""Repo - Ferramenta de clonagem e busca em repositórios."""

import os
import subprocess
import requests
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

# Carregar variáveis do .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

console = Console()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')


def run_repo_cli():
    """Interface CLI para clone de repositórios com tema Dracula."""
    
    # Header com tema Dracula
    console.print()
    console.print("📦 REPO", style="bold #bd93f9")
    console.print("═" * 50, style="#6272a4")
    console.print("Clonar e buscar em repositórios do GitHub", style="#f8f8f2")
    console.print()
    
    # Interface de input
    console.print("📝 [#f1fa8c]Configure seu clone:[/]", style="#f8f8f2")
    console.print()
    
    repo = console.input("📦 [#8be9fd]Repositório[/] [#6272a4](ex: microsoft/vscode):[/] ").strip()
    if not repo:
        console.print("❌ [#ff5555]Repositório não pode estar vazio[/]")
        return
    
    if "/" not in repo:
        console.print("❌ [#ff5555]Formato deve ser: usuario/repositorio[/]")
        return
    
    parts = repo.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        console.print("❌ [#ff5555]Formato deve ser: usuario/repositorio[/]")
        return
    
    query = console.input("🔍 [#8be9fd]Buscar nos arquivos[/] [#6272a4](opcional):[/] ").strip() or None
    
    depth_input = console.input("📏 [#8be9fd]Profundidade[/] [#6272a4](opcional, padrão completo):[/] ").strip()
    depth = None
    if depth_input:
        try:
            depth = int(depth_input)
            if depth < 1:
                console.print("❌ [#ff5555]Profundidade deve ser maior que 0[/]")
                return
        except ValueError:
            console.print("❌ [#ff5555]Profundidade deve ser um número[/]")
            return
    
    console.print()
    console.print(f"🚀 [#50fa7b]Clonando repositório {repo}...[/]")
    
    try:
        result = clone_repository(repo, query, depth)
        console.print()
        
        # Informações do resultado
        repo_name = repo.split('/')[-1]
        repo_path = Path(repo_name)
        
        if repo_path.exists():
            file_count = sum(1 for _ in repo_path.rglob('*') if _.is_file())
            folder_size = sum(f.stat().st_size for f in repo_path.rglob('*') if f.is_file()) // (1024 * 1024)  # MB
        else:
            file_count = 0
            folder_size = 0
        
        success_msg = f"[#50fa7b]✅ Repositório clonado com sucesso![/]\n\n"
        success_msg += f"[#f8f8f2]📁 Nome: [/][#8be9fd]{repo_name}[/]\n"
        success_msg += f"[#f8f8f2]📂 Pasta: [/][#8be9fd]./{repo_name}/[/]\n"
        success_msg += f"[#f8f8f2]📄 Arquivos: [/][#bd93f9]{file_count}[/]\n"
        success_msg += f"[#f8f8f2]💾 Tamanho: [/][#bd93f9]{folder_size}MB[/]\n"
        
        if query:
            success_msg += f"\n[#6272a4]🔍 Busca por '{query}' executada[/]"
        
        if GITHUB_TOKEN:
            success_msg += f"\n[#6272a4]💡 Requests usados: ~1/5000 (hora)[/]"
        else:
            success_msg += f"\n[#6272a4]💡 Sem token GitHub: 60 requests/hora[/]"
        
        console.print(Panel.fit(
            success_msg,
            title="[#50fa7b]Clone Concluído[/]",
            border_style="#50fa7b"
        ))
        
    except Exception as e:
        console.print()
        console.print(Panel.fit(
            f"[#ff5555]❌ Erro durante o clone[/]\n\n"
            f"[#f8f8f2]Detalhes: {str(e)}[/]\n\n"
            f"[#6272a4]💡 Verifique se o repositório existe e sua conexão[/]",
            title="[#ff5555]Erro[/]",
            border_style="#ff5555"
        ))


def search_github(query, language=None, sort="stars", limit=10):
    """Busca repositórios no GitHub."""
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    params = {
        'q': query,
        'sort': sort,
        'order': 'desc',
        'per_page': limit
    }
    
    if language:
        params['q'] += f' language:{language}'
    
    response = requests.get('https://api.github.com/search/repositories', 
                          headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()


def clone_repository(repo, query=None, depth=None):
    """Clona repositório do GitHub."""
    if '/' not in repo:
        raise ValueError("Formato deve ser: usuario/repositorio")
    
    # URL do repositório
    repo_url = f"https://github.com/{repo}.git"
    repo_name = repo.split('/')[-1]
    
    # Verificar se já existe
    if Path(repo_name).exists():
        raise Exception(f"Diretório '{repo_name}' já existe")
    
    # Comando git clone
    cmd = ['git', 'clone']
    
    if depth:
        cmd.extend(['--depth', str(depth)])
    
    cmd.extend([repo_url, repo_name])
    
    console.print("  📥 [#6272a4]Executando git clone...[/]")
    
    # Executar clone
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        if "not found" in result.stderr.lower():
            raise Exception(f"Repositório '{repo}' não encontrado")
        elif "permission denied" in result.stderr.lower():
            raise Exception("Repositório privado ou sem permissão")
        else:
            raise Exception(f"Erro no git: {result.stderr.strip()}")
    
    console.print(f"  📁 [#50fa7b]Repositório clonado: {repo_name}[/]")
    
    # Buscar nos arquivos se especificado
    if query:
        console.print("  🔍 [#6272a4]Buscando nos arquivos...[/]")
        search_results = search_in_files(repo_name, query)
        
        if search_results:
            console.print(f"  📋 [#50fa7b]Encontrados {len(search_results)} resultados para '{query}'[/]")
            
            # Mostrar apenas os primeiros 10 resultados
            for result in search_results[:10]:
                file_path = result['file'].replace(f"{repo_name}/", "")
                console.print(f"    📄 [#8be9fd]{file_path}[/][#6272a4]:{result['line_number']}[/] {result['line'][:60]}...")
            
            if len(search_results) > 10:
                console.print(f"    [#6272a4]... e mais {len(search_results) - 10} resultados[/]")
        else:
            console.print(f"  ⚠️  [#f1fa8c]Nenhum resultado encontrado para '{query}'[/]")
    
    return f"Repositório {repo} clonado com sucesso"


def search_in_files(directory, pattern, file_types=None):
    """Busca padrão nos arquivos do diretório."""
    results = []
    
    # Usar grep para busca eficiente
    cmd = ['grep', '-r', '-n', '-i', pattern, directory]  # -i para case insensitive
    
    if file_types:
        for ext in file_types:
            cmd.extend(['--include', f'*.{ext}'])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        for line in result.stdout.split('\n'):
            if ':' in line and line.strip():
                parts = line.split(':', 2)
                if len(parts) >= 3:
                    results.append({
                        'file': parts[0],
                        'line_number': parts[1],
                        'line': parts[2].strip()
                    })
    except Exception:
        pass
    
    return results


def get_repo_info(repo):
    """Obtém informações do repositório."""
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers)
    response.raise_for_status()
    
    return response.json()


# Manter compatibilidade
def run_repo_ui():
    """Alias para compatibilidade."""
    run_repo_cli()
