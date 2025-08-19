#!/usr/bin/env python3
"""
🎨 Extrator de Designs do Figma
Extraia designs de arquivos do Figma

Uso:
    python tools/extrator-figma.py info "chave_do_arquivo"
    python tools/extrator-figma.py download "chave_do_arquivo" --format png --scale 2
    python tools/extrator-figma.py extract "chave_do_arquivo" --output info_design.json
"""

import sys
import json
import requests
import click
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import time

# Adicionar lib ao path
sys.path.append(str(Path(__file__).parent.parent))
from lib.config import ConfigAPI, validar_chaves_api
from lib.interface import InterfaceLimpa

class ExtratorFigma:
    """Ferramenta de extração de designs do Figma"""
    
    def __init__(self, silencioso: bool = False):
        config = ConfigAPI()
        self.token_api = config.figma_token
        self.url_base = "https://api.figma.com/v1"
        self.headers = {
            "X-Figma-Token": self.token_api,
            "Content-Type": "application/json"
        }
        self.silencioso = silencioso
        self.ui = InterfaceLimpa(silencioso)
        
        # Configurar diretórios
        self.dir_ferramenta = Path(__file__).parent.parent
        self.dir_cache = self.dir_ferramenta / "cache"
        self.dir_exportacoes = self.dir_ferramenta / "exportacoes"
        self.dir_logs = self.dir_ferramenta / "logs"
        
        self.dir_cache.mkdir(exist_ok=True)
        self.dir_exportacoes.mkdir(exist_ok=True)
        self.dir_logs.mkdir(exist_ok=True)
        
        if not self.token_api:
            self.ui.mostrar_erro("Token da API do Figma não configurado")
            sys.exit(1)
    
    def log(self, mensagem: str, nivel: str = "INFO"):
        """Registrar atividade"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada_log = f"[{timestamp}] {nivel}: {mensagem}\n"
        
        arquivo_log = self.dir_logs / f"extrator_figma_{datetime.now().strftime('%Y%m%d')}.log"
        with open(arquivo_log, "a", encoding="utf-8") as f:
            f.write(entrada_log)
    
    def obter_info_arquivo(self, chave_arquivo: str) -> Dict:
        """Obter informações do arquivo do Figma"""
        
        # Verificar limite antes de fazer request
        from lib.controle_uso import controlador_uso
        
        pode_fazer, mensagem = controlador_uso.verificar_limite("figma", 1)
        
        if not pode_fazer:
            if not controlador_uso.confirmar_excesso_limite("figma", 1):
                return {"error": "Operação cancelada para não exceder free tier"}
        
        if not self.silencioso:
            self.ui.mostrar_status(f"Obtendo informações do arquivo {chave_arquivo}...")
        
        self.log(f"Obtendo informações do arquivo: {chave_arquivo}")
        
        try:
            response = requests.get(
                f"{self.url_base}/files/{chave_arquivo}",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            # Registrar uso após sucesso
            controlador_uso.registrar_uso("figma", 1)
            
            dados = response.json()
            self.log(f"Arquivo encontrado: {dados.get('name', 'Sem nome')}")
            return dados
            
        except requests.exceptions.RequestException as e:
            self.log(f"Erro ao obter informações do arquivo: {e}", "ERROR")
            return {"error": str(e)}
    
    def baixar_imagens(self, chave_arquivo: str, formato: str = "png", 
                      escala: float = 1.0, dir_saida: str = None,
                      ids_nos: List[str] = None, max_imagens: int = 10) -> List[Dict]:
        """Baixar imagens do arquivo do Figma"""
        
        # Obter informações do arquivo
        info_arquivo = self.obter_info_arquivo(chave_arquivo)
        if "error" in info_arquivo:
            self.ui.mostrar_erro(f"Falha ao obter informações do arquivo: {info_arquivo['error']}")
            return []
        
        nome_arquivo = info_arquivo.get("name", "arquivo_figma").replace(" ", "_")
        
        # Se não especificou nós, pegar frames principais
        if not ids_nos:
            if not self.silencioso:
                self.ui.mostrar_status("Analisando estrutura do arquivo...")
            
            info_nos = self._extrair_info_nos(info_arquivo)
            ids_nos = [
                no["id"] for no in info_nos 
                if no["tipo"] in ["FRAME", "COMPONENT", "COMPONENT_SET"] 
                and no.get("pai") == ""
                and no.get("visivel", True)
            ][:max_imagens]
        
        if not ids_nos:
            self.ui.mostrar_erro("Nenhum nó baixável encontrado")
            return []
        
        # Obter URLs das imagens
        if not self.silencioso:
            self.ui.mostrar_status(f"Gerando URLs de download para {len(ids_nos)} itens...")
        
        dados_imagens = self._obter_urls_imagens(chave_arquivo, ids_nos, formato, escala)
        
        if "error" in dados_imagens:
            self.ui.mostrar_erro(f"Falha ao obter URLs das imagens: {dados_imagens['error']}")
            return []
        
        imagens = dados_imagens.get("images", {})
        if not imagens:
            self.ui.mostrar_erro("Nenhuma URL de imagem gerada")
            return []
        
        arquivos_baixados = []
        
        # Mostrar progresso
        progresso = self.ui.mostrar_progresso(f"Baixando {len(imagens)} arquivos", len(imagens))
        
        if progresso:
            with progresso:
                tarefa = progresso.add_task("Baixando...", total=len(imagens))
                
                for i, (id_no, url_imagem) in enumerate(imagens.items(), 1):
                    if not url_imagem:
                        progresso.advance(tarefa)
                        continue
                    
                    nome_arquivo_final = f"{nome_arquivo}_{id_no}_{i}.{formato}"
                    progresso.update(tarefa, description=f"Baixando {nome_arquivo_final[:30]}...")
                    
                    caminho_arquivo = self._baixar_imagem_unica(url_imagem, nome_arquivo_final, dir_saida)
                    if caminho_arquivo:
                        arquivos_baixados.append({
                            'caminho': caminho_arquivo,
                            'nome': Path(caminho_arquivo).name,
                            'tamanho': f"{Path(caminho_arquivo).stat().st_size / (1024 * 1024):.2f} MB"
                        })
                    
                    progresso.advance(tarefa)
                    time.sleep(0.2)  # Rate limiting
        else:
            # Modo silencioso
            for i, (id_no, url_imagem) in enumerate(imagens.items(), 1):
                if not url_imagem:
                    continue
                
                nome_arquivo_final = f"{nome_arquivo}_{id_no}_{i}.{formato}"
                caminho_arquivo = self._baixar_imagem_unica(url_imagem, nome_arquivo_final, dir_saida)
                if caminho_arquivo:
                    arquivos_baixados.append({
                        'caminho': caminho_arquivo,
                        'nome': Path(caminho_arquivo).name,
                        'tamanho': f"{Path(caminho_arquivo).stat().st_size / (1024 * 1024):.2f} MB"
                    })
                
                time.sleep(0.2)  # Rate limiting
        
        return arquivos_baixados
    
    def _obter_urls_imagens(self, chave_arquivo: str, ids_nos: List[str], formato: str, escala: float) -> Dict:
        """Obter URLs das imagens da API do Figma"""
        self.log(f"Obtendo URLs para {len(ids_nos)} imagens")
        
        params = {
            "format": formato,
            "scale": escala,
            "ids": ",".join(ids_nos)
        }
        
        try:
            response = requests.get(
                f"{self.url_base}/images/{chave_arquivo}",
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            dados = response.json()
            imagens = dados.get("images", {})
            self.log(f"Obtidas {len(imagens)} URLs de imagem")
            return dados
            
        except requests.exceptions.RequestException as e:
            self.log(f"Erro ao obter URLs: {e}", "ERROR")
            return {"images": {}, "error": str(e)}
    
    def _baixar_imagem_unica(self, url: str, nome_arquivo: str, dir_saida: str = None) -> str:
        """Baixar uma única imagem"""
        if dir_saida:
            caminho_saida = Path(dir_saida)
        else:
            caminho_saida = self.dir_exportacoes
            
        caminho_saida.mkdir(parents=True, exist_ok=True)
        caminho_arquivo = caminho_saida / nome_arquivo
        
        # Verificar se existe
        if caminho_arquivo.exists():
            self.log(f"Arquivo já existe: {caminho_arquivo}")
            return str(caminho_arquivo)
        
        try:
            # Timeout mais curto para SVG
            timeout = 60 if nome_arquivo.endswith('.svg') else ConfigAPI.DOWNLOAD_TIMEOUT
            
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            with open(caminho_arquivo, "wb") as f:
                f.write(response.content)
                
            self.log(f"Baixado: {caminho_arquivo}")
            return str(caminho_arquivo)
            
        except requests.exceptions.Timeout:
            self.log(f"Timeout no download: {nome_arquivo}", "WARNING")
            return None
        except requests.exceptions.RequestException as e:
            self.log(f"Erro no download: {e}", "ERROR")
            return None
    
    def _extrair_info_nos(self, dados_arquivo: Dict) -> List[Dict]:
        """Extrair informações dos nós dos dados do arquivo"""
        info_nos = []
        
        def percorrer_no(no, nome_pai=""):
            info_no = {
                "id": no.get("id"),
                "nome": no.get("name"),
                "tipo": no.get("type"),
                "pai": nome_pai,
                "visivel": no.get("visible", True)
            }
            
            # Adicionar dimensões se disponíveis
            if "absoluteBoundingBox" in no:
                bbox = no["absoluteBoundingBox"]
                info_no["dimensoes"] = {
                    "largura": bbox.get("width"),
                    "altura": bbox.get("height")
                }
            
            info_nos.append(info_no)
            
            # Processar filhos recursivamente
            if "children" in no:
                for filho in no["children"]:
                    percorrer_no(filho, no.get("name", ""))
        
        # Processar documento
        documento = dados_arquivo.get("document", {})
        if "children" in documento:
            for pagina in documento["children"]:
                percorrer_no(pagina)
        
        return info_nos
    
    def extrair_info_design(self, chave_arquivo: str, arquivo_saida: str = None) -> Dict:
        """Extrair informações completas de design"""
        
        # Obter informações do arquivo
        info_arquivo = self.obter_info_arquivo(chave_arquivo)
        if "error" in info_arquivo:
            return info_arquivo
        
        if not self.silencioso:
            self.ui.mostrar_status("Analisando estrutura do design...")
        
        info_nos = self._extrair_info_nos(info_arquivo)
        
        # Compilar informações
        info_design = {
            "nome_arquivo": info_arquivo.get("name"),
            "chave_arquivo": chave_arquivo,
            "ultima_modificacao": info_arquivo.get("lastModified"),
            "versao": info_arquivo.get("version"),
            "extraido_em": datetime.now().isoformat(),
            "resumo": {
                "total_nos": len(info_nos),
                "frames": len([n for n in info_nos if n["tipo"] == "FRAME"]),
                "componentes": len([n for n in info_nos if n["tipo"] == "COMPONENT"]),
                "nos_texto": len([n for n in info_nos if n["tipo"] == "TEXT"]),
            },
            "nos": info_nos[:100]  # Limitar para evitar arquivos enormes
        }
        
        # Salvar em arquivo se especificado
        if arquivo_saida:
            caminho_saida = Path(arquivo_saida)
            if not caminho_saida.is_absolute():
                caminho_saida = self.dir_exportacoes / arquivo_saida
            
            with open(caminho_saida, "w", encoding="utf-8") as f:
                json.dump(info_design, f, indent=2, ensure_ascii=False)
            
            self.log(f"Informações de design salvas: {caminho_saida}")
        
        return info_design

# Comandos CLI
@click.group()
@click.option('--quiet', '-q', is_flag=True, help='Modo silencioso')
@click.pass_context
def cli(ctx, quiet):
    """🎨 Extrator de Designs do Figma - Interface limpa para API do Figma"""
    ctx.ensure_object(dict)
    ctx.obj['quiet'] = quiet
    
    # Validar configuração
    problemas = validar_chaves_api()
    if 'figma' in problemas:
        ui = InterfaceLimpa(quiet)
        ui.mostrar_erro(f"API do Figma: {problemas['figma']}")
        sys.exit(1)

@cli.command()
@click.argument('chave_arquivo')
@click.option('--format', 'formato_saida', type=click.Choice(['json', 'tabela']), default='tabela', help='Formato de saída')
@click.pass_context
def info(ctx, chave_arquivo, formato_saida):
    """Obter informações do arquivo do Figma"""
    
    extrator = ExtratorFigma(silencioso=ctx.obj['quiet'])
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Informações do Arquivo Figma", f"Arquivo: {chave_arquivo}")
    
    info_arquivo = extrator.obter_info_arquivo(chave_arquivo)
    
    if "error" in info_arquivo:
        ui.mostrar_erro(f"Falha ao obter informações do arquivo: {info_arquivo['error']}")
        sys.exit(1)
    
    if formato_saida == "json":
        print(json.dumps(info_arquivo, indent=2, ensure_ascii=False))
    else:  # tabela
        if not ctx.obj['quiet']:
            dados = [
                ["Nome", info_arquivo.get('name', 'N/A')],
                ["Chave", chave_arquivo],
                ["Modificado", info_arquivo.get('lastModified', 'N/A')],
                ["Versão", str(info_arquivo.get('version', 'N/A'))]
            ]
            
            tabela = ui.criar_tabela("Informações do Arquivo", ["Propriedade", "Valor"], dados)
            ui.console.print(tabela)
        else:
            print(f"{info_arquivo.get('name', 'N/A')}|{chave_arquivo}|{info_arquivo.get('lastModified', 'N/A')}")

@cli.command()
@click.argument('chave_arquivo')
@click.option('--format', type=click.Choice(['png', 'jpg', 'svg', 'pdf']), default='png', help='Formato da imagem')
@click.option('--scale', type=float, default=1.0, help='Escala da imagem (0.01 a 4.0)')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--nodes', help='IDs específicos dos nós (separados por vírgula)')
@click.option('--max-images', type=int, default=5, help='Máximo de imagens automáticas')
@click.pass_context
def download(ctx, chave_arquivo, format, scale, output, nodes, max_images):
    """Baixar imagens do arquivo do Figma"""
    
    extrator = ExtratorFigma(silencioso=ctx.obj['quiet'])
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Download do Figma", f"Arquivo: {chave_arquivo}")
    
    ids_nos = None
    if nodes:
        ids_nos = [n.strip() for n in nodes.split(",")]
    
    arquivos = extrator.baixar_imagens(
        chave_arquivo,
        formato=format,
        escala=scale,
        dir_saida=output,
        ids_nos=ids_nos,
        max_imagens=max_images
    )
    
    if arquivos:
        ui.mostrar_sucesso(f"Baixados {len(arquivos)} arquivos", arquivos)
    else:
        ui.mostrar_erro("Nenhum arquivo foi baixado")

@cli.command()
@click.argument('chave_arquivo')
@click.option('--output', '-o', default='info_design.json', help='Arquivo JSON de saída')
@click.option('--format', 'formato_saida', type=click.Choice(['json', 'resumo']), default='resumo', help='Formato de saída')
@click.pass_context
def extract(ctx, chave_arquivo, output, formato_saida):
    """Extrair informações de design"""
    
    extrator = ExtratorFigma(silencioso=ctx.obj['quiet'])
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Análise de Design", f"Arquivo: {chave_arquivo}")
    
    info_design = extrator.extrair_info_design(chave_arquivo, output)
    
    if "error" in info_design:
        ui.mostrar_erro(f"Análise falhou: {info_design['error']}")
        sys.exit(1)
    
    if formato_saida == "json":
        print(json.dumps(info_design, indent=2, ensure_ascii=False))
    else:  # resumo
        if not ctx.obj['quiet']:
            resumo = info_design["resumo"]
            
            dados = [
                ["Arquivo", info_design['nome_arquivo']],
                ["Total de Nós", resumo['total_nos']],
                ["Frames", resumo['frames']],
                ["Componentes", resumo['componentes']],
                ["Nós de Texto", resumo['nos_texto']],
                ["Saída", output]
            ]
            
            tabela = ui.criar_tabela("Análise de Design", ["Propriedade", "Valor"], dados)
            ui.console.print(tabela)
            
            ui.mostrar_sucesso(f"Análise completa, salva em {output}")
        else:
            resumo = info_design["resumo"]
            print(f"{info_design['nome_arquivo']}|{resumo['total_nos']}|{resumo['frames']}|{resumo['componentes']}")

@cli.command()
@click.pass_context
def status(ctx):
    """Mostrar status da configuração"""
    
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    # Verificar APIs
    problemas = validar_chaves_api()
    configs = {
        'figma': {
            'ok': 'figma' not in problemas,
            'info': 'API de extração de designs' if 'figma' not in problemas else problemas['figma']
        }
    }
    
    ui.mostrar_status_config(configs)

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
