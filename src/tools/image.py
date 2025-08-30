"""Image - Ferramenta de busca de imagens no Pexels."""

import os
from pathlib import Path
import requests
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel

# Carregar variáveis do .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

console = Console()

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')
PEXELS_BASE_URL = 'https://api.pexels.com/v1'


def run_image_cli():
    """Interface CLI para busca de imagens com tema Dracula."""
    
    # Header com tema Dracula
    console.print()
    console.print("🖼️  IMAGE", style="bold #bd93f9")
    console.print("═" * 50, style="#6272a4")
    console.print("Buscar e baixar imagens do Pexels", style="#f8f8f2")
    console.print()
    
    # Verificar API key primeiro
    if not PEXELS_API_KEY:
        console.print(Panel.fit(
            "[#ff5555]❌ API não configurada[/]\n\n"
            "[#f8f8f2]Para usar esta ferramenta, configure sua chave do Pexels:[/]\n\n"
            "[#8be9fd]1.[/] [#f8f8f2]Acesse: https://www.pexels.com/api/[/]\n"
            "[#8be9fd]2.[/] [#f8f8f2]Crie uma conta gratuita[/]\n"
            "[#8be9fd]3.[/] [#f8f8f2]Copie sua API key[/]\n"
            "[#8be9fd]4.[/] [#f8f8f2]Execute: [/][#50fa7b]nano .env[/]\n"
            "[#8be9fd]5.[/] [#f8f8f2]Cole a chave em PEXELS_API_KEY[/]\n\n"
            "[#6272a4]💡 Free tier: 200 requests/hora[/]",
            title="[#ff79c6]Configuração Necessária[/]",
            border_style="#ff5555"
        ))
        return
    
    # Interface de input
    console.print("📝 [#f1fa8c]Configure sua busca:[/]", style="#f8f8f2")
    console.print()
    
    query = console.input("🔍 [#8be9fd]Consulta[/] [#6272a4](ex: office desk):[/] ").strip()
    if not query:
        console.print("❌ [#ff5555]Consulta não pode estar vazia[/]")
        return
    
    count_input = console.input("📊 [#8be9fd]Quantidade[/] [#6272a4](padrão 5):[/] ").strip()
    try:
        count = int(count_input) if count_input else 5
        count = max(1, min(count, 80))  # Entre 1 e 80
    except ValueError:
        count = 5
    
    orientation = console.input("📐 [#8be9fd]Orientação[/] [#6272a4](landscape/portrait/square, Enter para qualquer):[/] ").strip() or None
    size = console.input("📏 [#8be9fd]Tamanho[/] [#6272a4](large/medium/small, Enter para qualquer):[/] ").strip() or None
    color = console.input("🎨 [#8be9fd]Cor[/] [#6272a4](ex: red, blue, Enter para qualquer):[/] ").strip() or None
    
    console.print()
    console.print(f"🚀 [#50fa7b]Buscando {count} imagens para '{query}'...[/]")
    
    try:
        results = search_images(query, count, orientation, size, color)
        console.print()
        console.print(Panel.fit(
            f"[#50fa7b]✅ Sucesso![/]\n\n"
            f"[#f8f8f2]📁 {len(results)} imagens baixadas[/]\n"
            f"[#f8f8f2]📂 Pasta: [/][#8be9fd]./imagens/[/]\n\n"
            f"[#6272a4]💡 Total de requests usados: {len(results)}/200 (hora)[/]",
            title="[#50fa7b]Download Concluído[/]",
            border_style="#50fa7b"
        ))
    except Exception as e:
        console.print()
        console.print(Panel.fit(
            f"[#ff5555]❌ Erro durante o download[/]\n\n"
            f"[#f8f8f2]Detalhes: {str(e)}[/]\n\n"
            f"[#6272a4]💡 Verifique sua conexão e tente novamente[/]",
            title="[#ff5555]Erro[/]",
            border_style="#ff5555"
        ))


def search_images(query, count=1, orientation=None, size=None, color=None):
    """Busca e baixa imagens do Pexels."""
    if not PEXELS_API_KEY:
        raise Exception("PEXELS_API_KEY não configurada")
    
    headers = {'Authorization': PEXELS_API_KEY}
    
    params = {
        'query': query,
        'per_page': min(count, 80),
        'page': 1
    }
    
    if orientation:
        params['orientation'] = orientation
    if size:
        params['size'] = size
    if color:
        params['color'] = color
    
    response = requests.get(f'{PEXELS_BASE_URL}/search', headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    photos = data.get('photos', [])
    
    if not photos:
        raise Exception("Nenhuma imagem encontrada para esta consulta")
    
    # Criar diretório
    output_dir = Path('imagens')
    output_dir.mkdir(exist_ok=True)
    
    downloaded = []
    
    with Progress() as progress:
        task = progress.add_task("[#bd93f9]Baixando imagens...", total=len(photos[:count]))
        
        for i, photo in enumerate(photos[:count]):
            # Usar URL de alta qualidade
            image_url = photo['src']['large2x']
            filename = f"{query.replace(' ', '_')}_{i+1}.jpg"
            filepath = output_dir / filename
            
            # Download
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            downloaded.append({
                'nome': filename,
                'tamanho': f"{len(img_response.content) // 1024}KB",
                'url': photo['url']
            })
            
            console.print(f"  📁 [#50fa7b]{filename}[/] [#6272a4]({len(img_response.content) // 1024}KB)[/]")
            progress.advance(task)
    
    return downloaded


def get_collections():
    """Lista coleções populares do Pexels."""
    if not PEXELS_API_KEY:
        raise Exception("PEXELS_API_KEY não configurada")
    
    headers = {'Authorization': PEXELS_API_KEY}
    response = requests.get(f'{PEXELS_BASE_URL}/collections/featured', headers=headers)
    response.raise_for_status()
    return response.json()


# Manter compatibilidade
def run_pexels_cli():
    """Alias para compatibilidade."""
    run_image_cli()

def run_pexels_ui():
    """Alias para compatibilidade."""
    run_image_cli()
