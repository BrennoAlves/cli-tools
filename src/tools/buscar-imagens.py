#!/usr/bin/env python3
"""
🖼️ Ferramenta para Buscar Imagens
Busque e baixe imagens via API do Pexels

Uso:
    python tools/buscar-imagens.py search "reunião de negócios" --count 5
    python tools/buscar-imagens.py download "escritório startup" --output ./imagens/
    python tools/buscar-imagens.py urls "interface dashboard" --orientation landscape
"""

import sys
import json
import requests
import click
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Adicionar lib ao path
sys.path.append(str(Path(__file__).parent.parent))
from core.config import ConfigAPI, validar_chaves_api
from core.config_diretorios import ConfigDiretorios
from core.interface import InterfaceLimpa

class FerramentaBuscaImagens:
    """Ferramenta de busca e download de imagens"""
    
    def __init__(self, silencioso: bool = False):
        config = ConfigAPI()
        self.chave_api = config.pexels_key
        self.url_base = "https://api.pexels.com/v1"
        self.headers = {"Authorization": self.chave_api}
        self.silencioso = silencioso
        self.ui = InterfaceLimpa(silencioso)
        
        # Configurar diretórios usando ConfigDiretorios
        config_dirs = ConfigDiretorios()
        self.dir_imagens = config_dirs.imagens_dir
        self.dir_ferramenta = Path(__file__).parent.parent
        self.dir_cache = self.dir_ferramenta / "cache"
        self.dir_logs = self.dir_ferramenta / "logs"
        
        # Criar diretórios necessários
        self.dir_imagens.mkdir(parents=True, exist_ok=True)
        self.dir_cache.mkdir(exist_ok=True)
        self.dir_logs.mkdir(exist_ok=True)
        
        # Cache de metadados
        self.cache_metadata = self.dir_cache / "metadata.json"
        self._carregar_cache_metadata()
        
        if not self.chave_api:
            self.ui.mostrar_erro("Chave da API do Pexels não configurada")
            sys.exit(1)
    
    def _carregar_cache_metadata(self):
        """Carregar cache de metadados"""
        try:
            if self.cache_metadata.exists():
                with open(self.cache_metadata, 'r', encoding='utf-8') as f:
                    self.metadata_cache = json.load(f)
            else:
                self.metadata_cache = {}
        except (json.JSONDecodeError, FileNotFoundError):
            self.metadata_cache = {}
    
    def _salvar_cache_metadata(self):
        """Salvar cache de metadados"""
        try:
            with open(self.cache_metadata, 'w', encoding='utf-8') as f:
                json.dump(self.metadata_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Erro ao salvar cache: {e}", "ERROR")
    
    def _gerar_hash_url(self, url: str) -> str:
        """Gerar hash único para URL"""
        return hashlib.md5(url.encode()).hexdigest()[:12]
    
    def _verificar_cache(self, url: str, caminho_arquivo: Path) -> bool:
        """Verificar se arquivo está em cache e é válido"""
        if not caminho_arquivo.exists():
            return False
        
        url_hash = self._gerar_hash_url(url)
        
        # Verificar metadados
        if url_hash in self.metadata_cache:
            metadata = self.metadata_cache[url_hash]
            arquivo_stat = caminho_arquivo.stat()
            
            # Verificar se o arquivo não foi modificado
            if (arquivo_stat.st_size == metadata.get('size', 0) and 
                arquivo_stat.st_mtime == metadata.get('mtime', 0)):
                return True
        
        return False
    
    def _atualizar_cache(self, url: str, caminho_arquivo: Path):
        """Atualizar cache com informações do arquivo"""
        url_hash = self._gerar_hash_url(url)
        arquivo_stat = caminho_arquivo.stat()
        
        self.metadata_cache[url_hash] = {
            'url': url,
            'arquivo': str(caminho_arquivo),
            'size': arquivo_stat.st_size,
            'mtime': arquivo_stat.st_mtime,
            'timestamp': datetime.now().isoformat()
        }
        
        self._salvar_cache_metadata()
    
    def log(self, mensagem: str, nivel: str = "INFO"):
        """Registrar atividade"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada_log = f"[{timestamp}] {nivel}: {mensagem}\n"
        
        arquivo_log = self.dir_logs / f"busca_imagens_{datetime.now().strftime('%Y%m%d')}.log"
        with open(arquivo_log, "a", encoding="utf-8") as f:
            f.write(entrada_log)
    
    def buscar_imagens(self, consulta: str, por_pagina: int = 10, **filtros) -> Dict:
        """Buscar imagens via API do Pexels"""
        
        # Verificar limite antes de fazer request
        from core.controle_uso import controlador_uso
        
        pode_fazer, mensagem = controlador_uso.verificar_limite("pexels", 1)
        
        if not pode_fazer:
            if not controlador_uso.confirmar_excesso_limite("pexels", 1):
                return {"photos": [], "error": "Operação cancelada para não exceder free tier"}
        
        if not self.silencioso:
            self.ui.mostrar_status(f"Buscando por '{consulta}'...")
        
        self.log(f"Buscando por: '{consulta}'")
        
        params = {
            "query": consulta,
            "per_page": min(por_pagina, 80)
        }
        params.update(filtros)
            
        try:
            response = requests.get(
                f"{self.url_base}/search",
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            # Registrar uso após sucesso
            controlador_uso.registrar_uso("pexels", 1)
            
            dados = response.json()
            self.log(f"Encontradas {len(dados.get('photos', []))} imagens")
            return dados
            
        except requests.exceptions.RequestException as e:
            self.log(f"Erro na busca: {e}", "ERROR")
            return {"photos": [], "error": str(e)}
    
    def baixar_imagens(self, consulta: str, quantidade: int = 3, 
                      dir_saida: str = None, **filtros) -> List[Dict]:
        """Buscar e baixar imagens"""
        
        # Buscar imagens
        resultados = self.buscar_imagens(consulta, por_pagina=quantidade, **filtros)
        
        if "error" in resultados:
            self.ui.mostrar_erro(f"Busca falhou: {resultados['error']}")
            return []
        
        fotos = resultados.get("photos", [])
        if not fotos:
            self.ui.mostrar_erro("Nenhuma imagem encontrada")
            return []
        
        arquivos_baixados = []
        
        # Baixar cada imagem com progresso simples
        for i, foto in enumerate(fotos, 1):
            if not self.silencioso:
                self.ui.mostrar_progresso(i, len(fotos), f"Baixando imagem {i}")
            
            url = foto["src"]["medium"]
            consulta_segura = "".join(c for c in consulta if c.isalnum() or c in (' ', '-', '_')).rstrip()
            consulta_segura = consulta_segura.replace(' ', '_')
            nome_arquivo = f"{consulta_segura}_{i}_{foto['id']}.webp"
            
            caminho_arquivo = self._baixar_imagem_unica(url, nome_arquivo, dir_saida)
            if caminho_arquivo:
                arquivos_baixados.append({
                    'caminho': caminho_arquivo,
                    'nome': Path(caminho_arquivo).name,
                    'tamanho': f"{Path(caminho_arquivo).stat().st_size / (1024 * 1024):.2f} MB"
                })
        
        return arquivos_baixados
    
    def _baixar_imagem_unica(self, url: str, nome_arquivo: str, dir_saida: str = None) -> str:
        """Baixar uma única imagem"""
        # Validar URL
        if not url.startswith(('https://images.pexels.com/', 'https://www.pexels.com/')):
            self.log(f"URL não autorizada: {url}", "ERROR")
            return None
        
        # Sanitizar nome do arquivo
        nome_arquivo = "".join(c for c in nome_arquivo if c.isalnum() or c in '._-')
        if not nome_arquivo or len(nome_arquivo) < 3:
            nome_arquivo = f"imagem_{hash(url) % 10000}.webp"
        
        if dir_saida:
            caminho_saida = Path(dir_saida)
        else:
            caminho_saida = self.dir_imagens
            
        caminho_saida.mkdir(parents=True, exist_ok=True)
        caminho_arquivo = caminho_saida / nome_arquivo
        
        # Verificar cache inteligente
        if self._verificar_cache(url, caminho_arquivo):
            self.log(f"Arquivo encontrado no cache: {caminho_arquivo}")
            return str(caminho_arquivo)
        
        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            
            # Verificar tipo de conteúdo
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                self.log(f"Conteúdo não é imagem: {content_type}", "ERROR")
                return None
            
            # Verificar tamanho (máximo 50MB)
            if len(response.content) > 50 * 1024 * 1024:
                self.log("Imagem muito grande (>50MB)", "ERROR")
                return None
            
            with open(caminho_arquivo, "wb") as f:
                f.write(response.content)
                
            # Atualizar cache
            self._atualizar_cache(url, caminho_arquivo)
                
            self.log(f"Baixado: {caminho_arquivo}")
            return str(caminho_arquivo)
            
        except requests.exceptions.RequestException as e:
            self.log(f"Erro no download: {e}", "ERROR")
            return None

# Comandos CLI
@click.group()
@click.option('--quiet', '-q', is_flag=True, help='Modo silencioso')
@click.pass_context
def cli(ctx, quiet):
    """🖼️ Ferramenta de Busca de Imagens - Interface limpa para API do Pexels"""
    ctx.ensure_object(dict)
    ctx.obj['quiet'] = quiet
    
    # Validar configuração
    problemas = validar_chaves_api()
    if 'pexels' in problemas:
        ui = InterfaceLimpa(quiet)
        ui.mostrar_erro(f"API do Pexels: {problemas['pexels']}")
        sys.exit(1)

@cli.command()
@click.argument('consulta')
@click.option('--count', '-c', default=5, help='Número de resultados')
@click.option('--orientation', type=click.Choice(['landscape', 'portrait', 'square']), help='Orientação da imagem')
@click.option('--size', type=click.Choice(['large', 'medium', 'small']), help='Tamanho da imagem')
@click.option('--color', help='Filtro de cor')
@click.option('--format', 'formato_saida', type=click.Choice(['json', 'tabela', 'urls']), default='tabela', help='Formato de saída')
@click.pass_context
def search(ctx, consulta, count, orientation, size, color, formato_saida):
    """Buscar imagens"""
    
    ferramenta = FerramentaBuscaImagens(silencioso=ctx.obj['quiet'])
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Busca de Imagens", f"Consulta: {consulta}")
    
    # Preparar filtros
    filtros = {}
    if orientation: filtros['orientation'] = orientation
    if size: filtros['size'] = size
    if color: filtros['color'] = color
    
    # Buscar
    resultados = ferramenta.buscar_imagens(consulta, por_pagina=count, **filtros)
    
    if "error" in resultados:
        ui.mostrar_erro(f"Busca falhou: {resultados['error']}")
        sys.exit(1)
    
    fotos = resultados.get("photos", [])
    
    if formato_saida == "json":
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
    elif formato_saida == "urls":
        for foto in fotos:
            print(foto["src"]["medium"])
    else:  # tabela
        # Preparar dados para exibição
        dados_imagem = []
        for foto in fotos:
            dados_imagem.append({
                'id': foto['id'],
                'fotografo': foto['photographer'],
                'largura': foto['width'],
                'altura': foto['height'],
                'url': foto['src']['medium']
            })
        
        ui.mostrar_resultados(f"Resultados da Busca por '{consulta}'", dados_imagem)

@cli.command()
@click.argument('consulta')
@click.option('--count', '-c', default=5, help='Número de resultados')
@click.option('--orientation', type=click.Choice(['landscape', 'portrait', 'square']), help='Orientação da imagem')
@click.option('--size', type=click.Choice(['large', 'medium', 'small']), help='Tamanho da imagem')
@click.option('--color', help='Filtro de cor')
@click.option('--quality', type=click.Choice(['original', 'large', 'medium', 'small']), default='medium', help='Qualidade da URL')
@click.pass_context
def urls(ctx, consulta, count, orientation, size, color, quality):
    """Obter apenas URLs das imagens"""
    
    ferramenta = FerramentaBuscaImagens(silencioso=True)  # Sempre silencioso para URLs
    
    # Preparar filtros
    filtros = {}
    if orientation: filtros['orientation'] = orientation
    if size: filtros['size'] = size
    if color: filtros['color'] = color
    
    # Buscar
    resultados = ferramenta.buscar_imagens(consulta, por_pagina=count, **filtros)
    
    if "error" in resultados:
        print(f"Erro: {resultados['error']}", file=sys.stderr)
        sys.exit(1)
    
    fotos = resultados.get("photos", [])
    
    for foto in fotos:
        src = foto["src"]
        if quality == "original":
            print(src["original"])
        elif quality == "large":
            print(src["large"])
        elif quality == "small":
            print(src["small"])
        else:  # medium
            print(src["medium"])

@cli.command()
@click.argument('consulta')
@click.option('--count', '-c', default=3, help='Número de imagens')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--orientation', type=click.Choice(['landscape', 'portrait', 'square']), help='Orientação da imagem')
@click.option('--size', type=click.Choice(['large', 'medium', 'small']), help='Tamanho da imagem')
@click.option('--color', help='Filtro de cor')
@click.option('--min-width', type=int, help='Largura mínima em pixels')
@click.option('--min-height', type=int, help='Altura mínima em pixels')
@click.option('--category', help='Categoria específica')
@click.option('--locale', default='en-US', help='Localização para busca')
@click.option('--per-page', type=int, default=15, help='Resultados por página')
@click.option('--skip-cache', is_flag=True, help='Pular cache e baixar novamente')
@click.pass_context
def download(ctx, consulta, count, output, orientation, size, color, min_width, min_height, category, locale, per_page, skip_cache):
    """Baixar imagens"""
    
    ferramenta = FerramentaBuscaImagens(silencioso=ctx.obj['quiet'])
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    # Configurar skip cache se solicitado
    if skip_cache:
        ferramenta.metadata_cache = {}
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Download de Imagens", f"Consulta: {consulta}")
    
    # Preparar filtros avançados
    filtros = {}
    if orientation: filtros['orientation'] = orientation
    if size: filtros['size'] = size
    if color: filtros['color'] = color
    if min_width: filtros['min_width'] = min_width
    if min_height: filtros['min_height'] = min_height
    if category: filtros['category'] = category
    if locale: filtros['locale'] = locale
    
    # Ajustar per_page baseado no count
    filtros['per_page'] = min(per_page, count)
    
    # Baixar
    arquivos = ferramenta.baixar_imagens(consulta, quantidade=count, dir_saida=output, **filtros)
    
    if arquivos:
        ui.mostrar_sucesso(f"Baixadas {len(arquivos)} imagens")
        if not ctx.obj['quiet']:
            for arquivo in arquivos:
                print(f"  📁 {arquivo['nome']} ({arquivo['tamanho']})")
    else:
        ui.mostrar_erro("Nenhuma imagem foi baixada")

@cli.command()
@click.pass_context
def status(ctx):
    """Mostrar status da configuração"""
    
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    # Verificar APIs
    problemas = validar_chaves_api()
    configs = {
        'pexels': {
            'ok': 'pexels' not in problemas,
            'info': 'API de busca de imagens' if 'pexels' not in problemas else problemas['pexels']
        }
    }
    
    ui.mostrar_status_config(configs)

@cli.command()
@click.option('--all', 'limpar_tudo', is_flag=True, help='Limpar todo o cache')
@click.option('--older-than', type=int, help='Limpar arquivos mais antigos que N dias')
@click.pass_context
def cache(ctx, limpar_tudo, older_than):
    """Gerenciar cache de imagens"""
    
    ferramenta = FerramentaBuscaImagens(silencioso=ctx.obj['quiet'])
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Gerenciamento de Cache", "Limpeza de arquivos")
    
    if limpar_tudo:
        # Limpar todo o cache
        try:
            if ferramenta.cache_metadata.exists():
                ferramenta.cache_metadata.unlink()
            ferramenta.metadata_cache = {}
            ui.mostrar_sucesso("Cache limpo completamente")
        except Exception as e:
            ui.mostrar_erro(f"Erro ao limpar cache: {e}")
    
    elif older_than:
        # Limpar arquivos antigos
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=older_than)
        
        removidos = 0
        for url_hash, metadata in list(ferramenta.metadata_cache.items()):
            try:
                timestamp = datetime.fromisoformat(metadata.get('timestamp', ''))
                if timestamp < cutoff_date:
                    arquivo = Path(metadata['arquivo'])
                    if arquivo.exists():
                        arquivo.unlink()
                    del ferramenta.metadata_cache[url_hash]
                    removidos += 1
            except (ValueError, KeyError, FileNotFoundError):
                # Remove entrada inválida
                del ferramenta.metadata_cache[url_hash]
                removidos += 1
        
        ferramenta._salvar_cache_metadata()
        ui.mostrar_sucesso(f"Removidos {removidos} arquivos antigos")
    
    else:
        # Mostrar estatísticas do cache
        total_arquivos = len(ferramenta.metadata_cache)
        tamanho_total = 0
        
        for metadata in ferramenta.metadata_cache.values():
            tamanho_total += metadata.get('size', 0)
        
        tamanho_mb = tamanho_total / (1024 * 1024)
        
        if not ctx.obj['quiet']:
            print(f"📊 Cache Statistics:")
            print(f"  Arquivos: {total_arquivos}")
            print(f"  Tamanho: {tamanho_mb:.2f} MB")
            print(f"  Localização: {ferramenta.cache_metadata}")

if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        ui = InterfaceLimpa()
        ui.mostrar_erro("Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        ui = InterfaceLimpa()
        ui.mostrar_erro(f"Erro inesperado: {e}")
        sys.exit(1)
