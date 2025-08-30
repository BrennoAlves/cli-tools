"""FigClone - Ferramenta de download do Figma."""

import os
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

FIGMA_TOKEN = os.getenv('FIGMA_TOKEN', '')
FIGMA_BASE_URL = 'https://api.figma.com/v1'


def run_figclone_cli():
    """Interface CLI para download do Figma com tema Dracula."""
    
    # Header com tema Dracula
    console.print()
    console.print("🎨 FIGCLONE", style="bold #bd93f9")
    console.print("═" * 50, style="#6272a4")
    console.print("Download de designs e componentes do Figma", style="#f8f8f2")
    console.print()
    
    # Verificar API token primeiro
    if not FIGMA_TOKEN:
        console.print(Panel.fit(
            "[#ff5555]❌ Token não configurado[/]\n\n"
            "[#f8f8f2]Para usar esta ferramenta, configure seu token do Figma:[/]\n\n"
            "[#8be9fd]1.[/] [#f8f8f2]Acesse: https://www.figma.com/developers/api[/]\n"
            "[#8be9fd]2.[/] [#f8f8f2]Faça login na sua conta[/]\n"
            "[#8be9fd]3.[/] [#f8f8f2]Gere um Personal Access Token[/]\n"
            "[#8be9fd]4.[/] [#f8f8f2]Execute: [/][#50fa7b]nano .env[/]\n"
            "[#8be9fd]5.[/] [#f8f8f2]Cole o token em FIGMA_TOKEN[/]\n\n"
            "[#6272a4]💡 Free tier: 30 requests/minuto[/]",
            title="[#ff79c6]Configuração Necessária[/]",
            border_style="#ff5555"
        ))
        return
    
    # Interface de input
    console.print("📝 [#f1fa8c]Configure seu download:[/]", style="#f8f8f2")
    console.print()
    
    file_key = console.input("🔑 [#8be9fd]File Key[/] [#6272a4](da URL do Figma):[/] ").strip()
    if not file_key:
        console.print("❌ [#ff5555]File Key não pode estar vazio[/]")
        return
    
    if len(file_key) < 10:
        console.print("❌ [#ff5555]File Key muito curto[/]")
        return
    
    format_input = console.input("📄 [#8be9fd]Formato[/] [#6272a4](png/jpg/svg/pdf, padrão png):[/] ").strip().lower()
    format_type = format_input if format_input in ['png', 'jpg', 'svg', 'pdf'] else 'png'
    
    scale_input = console.input("📏 [#8be9fd]Escala[/] [#6272a4](1x/2x/3x/4x, padrão 2x):[/] ").strip()
    try:
        scale = float(scale_input.replace('x', '')) if scale_input else 2.0
        scale = max(1.0, min(scale, 4.0))  # Entre 1x e 4x
    except ValueError:
        scale = 2.0
    
    nodes = console.input("🎯 [#8be9fd]Node IDs[/] [#6272a4](específicos, Enter para todos os frames):[/] ").strip() or None
    
    console.print()
    console.print(f"🚀 [#50fa7b]Baixando designs do Figma...[/]")
    
    try:
        results = export_figma(file_key, format_type, scale, nodes)
        console.print()
        console.print(Panel.fit(
            f"[#50fa7b]✅ Sucesso![/]\n\n"
            f"[#f8f8f2]📁 {len(results)} arquivos baixados[/]\n"
            f"[#f8f8f2]📂 Pasta: [/][#8be9fd]./figma/[/]\n"
            f"[#f8f8f2]📄 Formato: [/][#bd93f9]{format_type.upper()}[/]\n"
            f"[#f8f8f2]📏 Escala: [/][#bd93f9]{scale}x[/]\n\n"
            f"[#6272a4]💡 Requests usados: ~{len(results) + 1}/30 (minuto)[/]",
            title="[#50fa7b]Download Concluído[/]",
            border_style="#50fa7b"
        ))
    except Exception as e:
        console.print()
        console.print(Panel.fit(
            f"[#ff5555]❌ Erro durante o download[/]\n\n"
            f"[#f8f8f2]Detalhes: {str(e)}[/]\n\n"
            f"[#6272a4]💡 Verifique o File Key e sua conexão[/]",
            title="[#ff5555]Erro[/]",
            border_style="#ff5555"
        ))


def get_file_info(file_key):
    """Obtém informações do arquivo Figma."""
    if not FIGMA_TOKEN:
        raise Exception("FIGMA_TOKEN não configurado")
    
    headers = {'X-Figma-Token': FIGMA_TOKEN}
    response = requests.get(f'{FIGMA_BASE_URL}/files/{file_key}', headers=headers)
    response.raise_for_status()
    return response.json()


def export_figma(file_key, format_type="png", scale=1.0, nodes=None):
    """Exporta designs do Figma."""
    if not FIGMA_TOKEN:
        raise Exception("FIGMA_TOKEN não configurado")
    
    headers = {'X-Figma-Token': FIGMA_TOKEN}
    
    # Se nodes não especificados, buscar todos os frames
    if not nodes:
        console.print("  🔍 [#6272a4]Buscando frames no arquivo...[/]")
        
        file_info = get_file_info(file_key)
        node_list = []
        
        def extract_nodes(node):
            if node.get('type') == 'FRAME':
                node_list.append(node['id'])
            for child in node.get('children', []):
                extract_nodes(child)
        
        for page in file_info['document']['children']:
            extract_nodes(page)
        
        nodes = node_list[:10]  # Limitar a 10 frames
        console.print(f"  📋 [#50fa7b]Encontrados {len(nodes)} frames[/]")
    else:
        nodes = [n.strip() for n in nodes.split(',') if n.strip()]
    
    if not nodes:
        raise Exception("Nenhum frame encontrado para exportar")
    
    console.print("  🎨 [#6272a4]Solicitando export ao Figma...[/]")
    
    # Solicitar export
    params = {
        'ids': ','.join(nodes),
        'format': format_type,
        'scale': scale
    }
    
    response = requests.get(f'{FIGMA_BASE_URL}/images/{file_key}', 
                          headers=headers, params=params)
    response.raise_for_status()
    
    export_data = response.json()
    images = export_data.get('images', {})
    
    if not images:
        raise Exception("Nenhuma imagem gerada pelo Figma")
    
    console.print("  📥 [#6272a4]Baixando arquivos...[/]")
    
    # Criar diretório
    output_dir = Path('figma')
    output_dir.mkdir(exist_ok=True)
    
    downloaded = []
    
    with Progress() as progress:
        task = progress.add_task("[#bd93f9]Baixando designs...", total=len(images))
        
        for i, (node_id, image_url) in enumerate(images.items()):
            if not image_url:
                continue
            
            filename = f"figma_export_{i+1}.{format_type}"
            filepath = output_dir / filename
            
            # Download
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            downloaded.append({
                'nome': filename,
                'tamanho': f"{len(img_response.content) // 1024}KB",
                'node_id': node_id
            })
            
            console.print(f"  📁 [#50fa7b]{filename}[/] [#6272a4]({len(img_response.content) // 1024}KB)[/]")
            progress.advance(task)
    
    return downloaded


def list_components(file_key):
    """Lista componentes do arquivo Figma."""
    if not FIGMA_TOKEN:
        raise Exception("FIGMA_TOKEN não configurado")
    
    headers = {'X-Figma-Token': FIGMA_TOKEN}
    response = requests.get(f'{FIGMA_BASE_URL}/files/{file_key}/components', headers=headers)
    response.raise_for_status()
    return response.json()


# Manter compatibilidade
def run_figma_cli():
    """Alias para compatibilidade."""
    run_figclone_cli()

def run_figma_ui():
    """Alias para compatibilidade."""
    run_figclone_cli()
