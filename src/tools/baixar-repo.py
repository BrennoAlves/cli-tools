#!/usr/bin/env python3
"""
📦 Ferramenta para Baixar Repositórios
Baixe repositórios do GitHub com seleção inteligente via IA

Uso:
    python tools/baixar-repo.py clone "facebook/react" --output ./referencias/
    python tools/baixar-repo.py smart "vercel/next.js" --query "apenas CSS e componentes"
    python tools/baixar-repo.py list --category frontend
    python tools/baixar-repo.py update "facebook/react"
"""

import sys
import json
import requests
import click
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import tempfile
import zipfile
import io

# Adicionar lib ao path
sys.path.append(str(Path(__file__).parent.parent))
from core.config import ConfigAPI, validar_chaves_api
from core.interface import InterfaceLimpa

class BaixadorRepositorio:
    """Ferramenta para baixar e gerenciar repositórios de referência"""
    
    def __init__(self, silencioso: bool = False):
        self.silencioso = silencioso
        self.ui = InterfaceLimpa(silencioso)
        
        # Configurar diretórios
        self.dir_ferramenta = Path(__file__).parent.parent
        self.dir_referencias = self.dir_ferramenta / "referencias"
        self.dir_logs = self.dir_ferramenta / "logs"
        self.arquivo_indice = self.dir_referencias / "indice.json"
        
        self.dir_referencias.mkdir(exist_ok=True)
        self.dir_logs.mkdir(exist_ok=True)
        
        # Carregar índice de repositórios
        self.indice = self._carregar_indice()
    
    def log(self, mensagem: str, nivel: str = "INFO"):
        """Registrar atividade"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada_log = f"[{timestamp}] {nivel}: {mensagem}\n"
        
        arquivo_log = self.dir_logs / f"baixar_repo_{datetime.now().strftime('%Y%m%d')}.log"
        with open(arquivo_log, "a", encoding="utf-8") as f:
            f.write(entrada_log)
    
    def _carregar_indice(self) -> Dict:
        """Carregar índice de repositórios baixados"""
        if self.arquivo_indice.exists():
            with open(self.arquivo_indice, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"repositorios": {}, "categorias": {}}
    
    def _salvar_indice(self):
        """Salvar índice de repositórios"""
        with open(self.arquivo_indice, 'w', encoding='utf-8') as f:
            json.dump(self.indice, f, indent=2, ensure_ascii=False)
    
    def obter_info_repo(self, repo: str) -> Dict:
        """Obter informações do repositório via GitHub API"""
        
        # Verificar limite antes de fazer request
        from core.controle_uso import controlador_uso
        
        pode_fazer, mensagem = controlador_uso.verificar_limite("github", 1)
        
        if not pode_fazer:
            if not controlador_uso.confirmar_excesso_limite("github", 1):
                return {"error": "Operação cancelada para não exceder free tier"}
        
        if not self.silencioso:
            self.ui.mostrar_status(f"Obtendo informações de {repo}...")
        
        self.log(f"Buscando informações do repositório: {repo}")
        
        try:
            # GitHub API pública (sem autenticação)
            response = requests.get(
                f"https://api.github.com/repos/{repo}",
                timeout=30
            )
            response.raise_for_status()
            
            # Registrar uso após sucesso
            controlador_uso.registrar_uso("github", 1)
            
            dados = response.json()
            self.log(f"Repositório encontrado: {dados.get('name', 'N/A')}")
            return dados
            
        except requests.exceptions.RequestException as e:
            self.log(f"Erro ao obter informações: {e}", "ERROR")
            return {"error": str(e)}
    
    def listar_arquivos_repo(self, repo: str, branch: str = "main") -> List[str]:
        """Listar todos os arquivos do repositório"""
        if not self.silencioso:
            self.ui.mostrar_status(f"Listando arquivos de {repo}...")
        
        try:
            # Tentar main primeiro, depois master
            for branch_nome in [branch, "main", "master"]:
                try:
                    response = requests.get(
                        f"https://api.github.com/repos/{repo}/git/trees/{branch_nome}?recursive=1",
                        timeout=30
                    )
                    if response.status_code == 200:
                        break
                except:
                    continue
            
            response.raise_for_status()
            dados = response.json()
            
            # Extrair apenas arquivos (não diretórios)
            arquivos = []
            for item in dados.get("tree", []):
                if item["type"] == "blob":  # arquivo
                    arquivos.append(item["path"])
            
            self.log(f"Encontrados {len(arquivos)} arquivos")
            return arquivos
            
        except requests.exceptions.RequestException as e:
            self.log(f"Erro ao listar arquivos: {e}", "ERROR")
            return []
    
    def selecao_inteligente_ia(self, arquivos: List[str], query: str, repo: str) -> List[str]:
        """
        Seleção inteligente de arquivos usando API do Gemini
        Integração direta sem interação manual
        """
        
        # Verificar limite antes de fazer request
        from core.controle_uso import controlador_uso
        
        pode_fazer, mensagem = controlador_uso.verificar_limite("gemini", 1)
        
        if not pode_fazer:
            if not controlador_uso.confirmar_excesso_limite("gemini", 1):
                self.ui.mostrar_erro("Operação cancelada para não exceder free tier do Gemini")
                return []
        
        if not self.silencioso:
            self.ui.mostrar_status("Consultando IA para seleção inteligente...")
        
        # Verificar se tem API key do Gemini
        config = ConfigAPI()
        if not config.gemini_key:
            self.ui.mostrar_erro("GEMINI_API_KEY não configurada. Configure no arquivo .env")
            return []
        
        try:
            # Preparar prompt otimizado para Gemini
            prompt = self._gerar_prompt_gemini(arquivos, query, repo)
            
            # Chamar API do Gemini
            arquivos_selecionados = self._consultar_gemini_api(prompt, arquivos)
            
            if arquivos_selecionados:
                if not self.silencioso:
                    self.ui.mostrar_sucesso(f"IA selecionou {len(arquivos_selecionados)} arquivos")
                return arquivos_selecionados
            else:
                self.ui.mostrar_erro("IA não encontrou arquivos que atendam ao critério")
                return []
                
        except Exception as e:
            self.log(f"Erro na seleção via IA: {e}", "ERROR")
            self.ui.mostrar_erro(f"Erro na consulta à IA: {e}")
            return []
    
    def _gerar_prompt_gemini(self, arquivos: List[str], query: str, repo: str) -> str:
        """Gerar prompt otimizado para API do Gemini"""
        
        # Limitar arquivos para não sobrecarregar a API
        arquivos_limitados = arquivos[:100] if len(arquivos) > 100 else arquivos
        
        prompt = f"""Você é um especialista em análise de código e estrutura de projetos.

TAREFA: Analisar lista de arquivos de um repositório e selecionar apenas os que atendem ao critério específico.

REPOSITÓRIO: {repo}
CRITÉRIO: "{query}"

ARQUIVOS DISPONÍVEIS:
"""
        
        for i, arquivo in enumerate(arquivos_limitados, 1):
            prompt += f"{i}. {arquivo}\n"
        
        prompt += f"""
INSTRUÇÕES:
1. Analise cada arquivo considerando:
   - Extensão e tipo de arquivo
   - Caminho e estrutura de diretórios
   - Contexto do projeto {repo}
   - Critério específico: "{query}"

2. Selecione APENAS arquivos que atendem EXATAMENTE ao critério
3. Responda APENAS com os números dos arquivos selecionados
4. Formato: números separados por vírgula (exemplo: 1,5,12,25)
5. Se nenhum arquivo atender: responda "NENHUM"

EXEMPLOS DE CRITÉRIOS:
- "apenas CSS" → .css, .scss, .less, .styl
- "só configurações" → .json, .yml, .yaml, .toml, config files
- "componentes React" → .jsx, .tsx em pastas de componentes
- "apenas JavaScript" → .js, .mjs, .ts (não .json)

RESPOSTA (apenas números):"""
        
        return prompt
    
    def _consultar_gemini_api(self, prompt: str, arquivos: List[str]) -> List[str]:
        """Consultar API do Gemini para seleção de arquivos"""
        
        # URL correta da API do Gemini 1.5 Flash
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,  # Baixa temperatura para respostas mais precisas
                "maxOutputTokens": 1000,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        try:
            config = ConfigAPI()
            response = requests.post(
                f"{url}?key={config.gemini_key}",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            # Registrar uso após sucesso
            from core.controle_uso import controlador_uso
            controlador_uso.registrar_uso("gemini", 1)
            
            dados = response.json()
            
            # Extrair resposta do Gemini
            if "candidates" in dados and len(dados["candidates"]) > 0:
                texto_resposta = dados["candidates"][0]["content"]["parts"][0]["text"].strip()
                
                self.log(f"Resposta do Gemini: {texto_resposta}")
                
                # Processar resposta
                return self._processar_resposta_gemini(texto_resposta, arquivos)
            else:
                self.log("Resposta vazia do Gemini", "WARNING")
                return []
                
        except requests.exceptions.RequestException as e:
            self.log(f"Erro na API do Gemini: {e}", "ERROR")
            raise Exception(f"Erro na consulta ao Gemini: {e}")
    
    def _processar_resposta_gemini(self, resposta: str, arquivos: List[str]) -> List[str]:
        """Processar resposta do Gemini e retornar arquivos selecionados"""
        
        resposta = resposta.strip()
        
        if resposta.upper() == "NENHUM":
            return []
        
        try:
            # Extrair números da resposta
            import re
            numeros = re.findall(r'\b\d+\b', resposta)
            
            arquivos_selecionados = []
            for num_str in numeros:
                num = int(num_str)
                if 1 <= num <= len(arquivos):
                    arquivos_selecionados.append(arquivos[num - 1])
            
            self.log(f"Arquivos selecionados pelo Gemini: {len(arquivos_selecionados)}")
            return arquivos_selecionados
            
        except Exception as e:
            self.log(f"Erro ao processar resposta do Gemini: {e}", "ERROR")
            return []
    
    def clonar_repositorio(self, repo: str, output_dir: str = None, categoria: str = None) -> bool:
        """Clonar repositório completo"""
        
        if not self.silencioso:
            self.ui.mostrar_cabecalho("Clone de Repositório", f"Repo: {repo}")
        
        # Extrair nome do repositório (parte após a barra)
        nome_repo = repo.split("/")[-1]
        
        # Definir diretório de saída
        if output_dir:
            # Criar pasta individual para o repo dentro do output_dir
            dir_base = Path(output_dir)
            dir_base.mkdir(parents=True, exist_ok=True)
            dir_destino = dir_base / nome_repo
        else:
            # Usar estrutura padrão com pasta individual
            categoria_dir = categoria or "geral"
            dir_destino = self.dir_referencias / categoria_dir / nome_repo
        
        # Verificar se diretório já existe e está vazio
        if dir_destino.exists() and any(dir_destino.iterdir()):
            self.ui.mostrar_erro(f"Diretório {dir_destino} já existe e não está vazio")
            return False
        
        # Criar diretório pai se não existir
        dir_destino.parent.mkdir(parents=True, exist_ok=True)
        
        # Verificar se git está disponível
        if not shutil.which("git"):
            self.ui.mostrar_erro("Git não encontrado. Usando download via ZIP...")
            return self._baixar_via_zip(repo, dir_destino)
        
        # Clonar via git
        try:
            if not self.silencioso:
                self.ui.mostrar_status("Clonando repositório...")
            
            cmd = ["git", "clone", f"https://github.com/{repo}.git", str(dir_destino)]
            resultado = subprocess.run(cmd, capture_output=True, text=True)
            
            if resultado.returncode == 0:
                self._registrar_repo(repo, str(dir_destino), categoria, "clone")
                self.log(f"Repositório clonado: {repo} -> {dir_destino}")
                if not self.silencioso:
                    self.ui.mostrar_sucesso(f"Repositório clonado em: {dir_destino}")
                return True
            else:
                self.ui.mostrar_erro(f"Erro no git clone: {resultado.stderr}")
                return False
                
        except Exception as e:
            self.ui.mostrar_erro(f"Erro ao clonar: {e}")
            return False
    
    def _baixar_via_zip(self, repo: str, dir_destino: Path) -> bool:
        """Baixar repositório via ZIP (fallback)"""
        try:
            if not self.silencioso:
                self.ui.mostrar_status("Baixando via ZIP...")
            
            response = requests.get(f"https://github.com/{repo}/archive/refs/heads/main.zip", timeout=60)
            if response.status_code != 200:
                response = requests.get(f"https://github.com/{repo}/archive/refs/heads/master.zip", timeout=60)
            
            response.raise_for_status()
            
            # Criar diretório de destino se não existir
            dir_destino.mkdir(parents=True, exist_ok=True)
            
            # Extrair ZIP
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                zip_file.extractall(dir_destino.parent)
                
                # Renomear pasta extraída para o nome correto
                nome_repo = repo.split("/")[1]
                for item in dir_destino.parent.iterdir():
                    if item.is_dir() and nome_repo in item.name and item != dir_destino:
                        if dir_destino.exists():
                            shutil.rmtree(dir_destino)
                        item.rename(dir_destino)
                        break
            
            if not self.silencioso:
                self.ui.mostrar_sucesso(f"Repositório baixado via ZIP em: {dir_destino}")
            return True
            
        except Exception as e:
            self.ui.mostrar_erro(f"Erro no download ZIP: {e}")
            return False
    
    def baixar_arquivos_especificos(self, repo: str, arquivos: List[str], output_dir: str = None) -> bool:
        """Baixar apenas arquivos específicos"""
        
        if not arquivos:
            self.ui.mostrar_erro("Nenhum arquivo especificado")
            return False
        
        if not self.silencioso:
            self.ui.mostrar_cabecalho("Download de Arquivos Específicos", f"Repo: {repo}")
        
        # Definir diretório
        if output_dir:
            dir_destino = Path(output_dir)
        else:
            dir_destino = self.dir_referencias / "especificos" / repo.replace("/", "_")
        
        dir_destino.mkdir(parents=True, exist_ok=True)
        
        # Baixar cada arquivo
        arquivos_baixados = []
        total = len(arquivos)
        
        for i, arquivo in enumerate(arquivos, 1):
            if not self.silencioso:
                self.ui.mostrar_progresso(i, total, arquivo)
            
            if self._baixar_arquivo_unico(repo, arquivo, dir_destino):
                arquivos_baixados.append(arquivo)
        
        if arquivos_baixados:
            self._registrar_repo(repo, str(dir_destino), "especificos", "arquivos", arquivos_baixados)
            self.ui.mostrar_sucesso(f"Baixados {len(arquivos_baixados)} arquivos")
            return True
        else:
            self.ui.mostrar_erro("Nenhum arquivo foi baixado")
            return False
    
    def _baixar_arquivo_unico(self, repo: str, arquivo: str, dir_destino: Path) -> bool:
        """Baixar um único arquivo"""
        try:
            # URL do arquivo raw no GitHub
            url = f"https://raw.githubusercontent.com/{repo}/main/{arquivo}"
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                # Tentar branch master
                url = f"https://raw.githubusercontent.com/{repo}/master/{arquivo}"
                response = requests.get(url, timeout=30)
            
            response.raise_for_status()
            
            # Criar estrutura de diretórios
            arquivo_destino = dir_destino / arquivo
            arquivo_destino.parent.mkdir(parents=True, exist_ok=True)
            
            # Salvar arquivo
            with open(arquivo_destino, 'wb') as f:
                f.write(response.content)
            
            self.log(f"Arquivo baixado: {arquivo}")
            return True
            
        except Exception as e:
            self.log(f"Erro ao baixar {arquivo}: {e}", "ERROR")
            return False
    
    def _registrar_repo(self, repo: str, caminho: str, categoria: str = None, tipo: str = "clone", arquivos: List[str] = None):
        """Registrar repositório no índice"""
        self.indice["repositorios"][repo] = {
            "caminho": caminho,
            "categoria": categoria or "geral",
            "tipo": tipo,
            "baixado_em": datetime.now().isoformat(),
            "arquivos": arquivos or []
        }
        
        # Atualizar categorias
        cat = categoria or "geral"
        if cat not in self.indice["categorias"]:
            self.indice["categorias"][cat] = []
        if repo not in self.indice["categorias"][cat]:
            self.indice["categorias"][cat].append(repo)
        
        self._salvar_indice()
    
    def listar_repositorios(self, categoria: str = None) -> List[Dict]:
        """Listar repositórios baixados"""
        repos = []
        
        for repo, info in self.indice["repositorios"].items():
            if categoria and info["categoria"] != categoria:
                continue
            
            repos.append({
                "repo": repo,
                "categoria": info["categoria"],
                "tipo": info["tipo"],
                "baixado_em": info["baixado_em"],
                "caminho": info["caminho"],
                "arquivos_count": len(info.get("arquivos", []))
            })
        
        return repos
    
    def atualizar_repositorio(self, repo: str) -> bool:
        """Atualizar repositório existente"""
        if repo not in self.indice["repositorios"]:
            self.ui.mostrar_erro(f"Repositório {repo} não encontrado")
            return False
        
        info = self.indice["repositorios"][repo]
        caminho = Path(info["caminho"])
        
        if not caminho.exists():
            self.ui.mostrar_erro(f"Diretório não encontrado: {caminho}")
            return False
        
        if info["tipo"] == "clone" and (caminho / ".git").exists():
            # Atualizar via git pull
            try:
                if not self.silencioso:
                    self.ui.mostrar_status(f"Atualizando {repo}...")
                
                resultado = subprocess.run(
                    ["git", "pull"], 
                    cwd=caminho, 
                    capture_output=True, 
                    text=True
                )
                
                if resultado.returncode == 0:
                    self.ui.mostrar_sucesso(f"Repositório {repo} atualizado")
                    return True
                else:
                    self.ui.mostrar_erro(f"Erro no git pull: {resultado.stderr}")
                    return False
                    
            except Exception as e:
                self.ui.mostrar_erro(f"Erro ao atualizar: {e}")
                return False
        else:
            # Re-baixar para outros tipos
            self.ui.mostrar_status(f"Re-baixando {repo}...")
            return self.clonar_repositorio(repo, str(caminho), info["categoria"])

# Comandos CLI
@click.group()
@click.option('--quiet', '-q', is_flag=True, help='Modo silencioso')
@click.pass_context
def cli(ctx, quiet):
    """📦 Baixador de Repositórios - Gerencie repositórios de referência"""
    ctx.ensure_object(dict)
    ctx.obj['quiet'] = quiet

@cli.command()
@click.argument('repo')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--category', '-c', help='Categoria do repositório')
@click.option('--json', 'output_json', is_flag=True, help='Saída em formato JSON')
@click.pass_context
def clone(ctx, repo, output, category, output_json):
    """Clonar repositório completo"""
    
    baixador = BaixadorRepositorio(silencioso=ctx.obj['quiet'])
    
    # Saída JSON
    if output_json:
        import json
        resultado = {
            "repositorio": repo,
            "tipo": "clone_completo",
            "categoria": category,
            "output": output
        }
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        return
    
    sucesso = baixador.clonar_repositorio(repo, output, category)
    
    if not sucesso:
        sys.exit(1)

@cli.command()
@click.argument('repo')
@click.argument('query')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--explain', type=click.Choice(['basic', 'detailed', 'debug']), help='Nível de explicação da IA')
@click.option('--dry-run', is_flag=True, help='Mostrar o que seria feito sem executar')
@click.option('--interactive', '-i', is_flag=True, help='Modo interativo')
@click.option('--json', 'output_json', is_flag=True, help='Saída em formato JSON')
@click.pass_context
def smart(ctx, repo, query, output, explain, dry_run, interactive, output_json):
    """Seleção inteligente de arquivos via IA"""
    
    baixador = BaixadorRepositorio(silencioso=ctx.obj['quiet'])
    
    # Configurar nível de explicação se fornecido
    if explain:
        baixador.nivel_explicacao = explain
    
    # Listar arquivos do repositório
    arquivos = baixador.listar_arquivos_repo(repo)
    
    if not arquivos:
        baixador.ui.mostrar_erro("Não foi possível listar arquivos do repositório")
        sys.exit(1)
    
    # Seleção inteligente via IA
    arquivos_selecionados = baixador.selecao_inteligente_ia(arquivos, query, repo)
    
    if not arquivos_selecionados:
        baixador.ui.mostrar_erro("Nenhum arquivo selecionado")
        sys.exit(1)
    
    # Modo dry-run: apenas mostrar o que seria feito
    if dry_run:
        baixador.ui.mostrar_cabecalho("Modo Dry-Run", "Arquivos que seriam baixados")
        for i, arquivo in enumerate(arquivos_selecionados, 1):
            print(f"{i:2d}. {arquivo}")
        print(f"\nTotal: {len(arquivos_selecionados)} arquivos")
        print("Use sem --dry-run para baixar os arquivos.")
        return
    
    # Modo interativo: pedir confirmação
    if interactive:
        baixador.ui.mostrar_cabecalho("Modo Interativo", "Confirmar seleção")
        for i, arquivo in enumerate(arquivos_selecionados, 1):
            print(f"{i:2d}. {arquivo}")
        
        resposta = input(f"\nBaixar {len(arquivos_selecionados)} arquivos? [S/n]: ").strip().lower()
        if resposta == 'n':
            print("❌ Operação cancelada pelo usuário.")
            return
    
    # Saída JSON
    if output_json:
        import json
        resultado = {
            "repositorio": repo,
            "query": query,
            "arquivos_selecionados": arquivos_selecionados,
            "total": len(arquivos_selecionados)
        }
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        return
    
    # Baixar arquivos selecionados
    sucesso = baixador.baixar_arquivos_especificos(repo, arquivos_selecionados, output)
    
    if not sucesso:
        sys.exit(1)

@cli.command()
@click.option('--category', '-c', help='Filtrar por categoria')
@click.pass_context
def list(ctx, category):
    """Listar repositórios baixados"""
    
    baixador = BaixadorRepositorio(silencioso=ctx.obj['quiet'])
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    repos = baixador.listar_repositorios(category)
    
    if not repos:
        ui.mostrar_erro("Nenhum repositório encontrado")
        return
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Repositórios Baixados", f"Total: {len(repos)}")
        
        dados_tabela = []
        for repo in repos:
            dados_tabela.append([
                repo['repo'],
                repo['categoria'],
                repo['tipo'],
                repo['baixado_em'][:10],  # apenas data
                str(repo['arquivos_count']) if repo['tipo'] == 'arquivos' else 'completo'
            ])
        
        tabela = ui.criar_tabela(
            "Repositórios",
            ["Repositório", "Categoria", "Tipo", "Data", "Arquivos"],
            dados_tabela
        )
        ui.console.print(tabela)
    else:
        for repo in repos:
            print(f"{repo['repo']}|{repo['categoria']}|{repo['caminho']}")

@cli.command()
@click.argument('repo')
@click.pass_context
def update(ctx, repo):
    """Atualizar repositório existente"""
    
    baixador = BaixadorRepositorio(silencioso=ctx.obj['quiet'])
    
    sucesso = baixador.atualizar_repositorio(repo)
    
    if not sucesso:
        sys.exit(1)

@cli.command()
@click.pass_context
def status(ctx):
    """Mostrar status dos repositórios"""
    
    baixador = BaixadorRepositorio(silencioso=ctx.obj['quiet'])
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    repos = baixador.listar_repositorios()
    categorias = baixador.indice.get("categorias", {})
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Status dos Repositórios")
        
        # Estatísticas
        dados_stats = [
            ["Total de Repositórios", len(repos)],
            ["Categorias", len(categorias)],
            ["Espaço Usado", "Calculando..."]  # TODO: calcular tamanho
        ]
        
        tabela_stats = ui.criar_tabela("Estatísticas", ["Métrica", "Valor"], dados_stats)
        ui.console.print(tabela_stats)
        
        # Categorias
        if categorias:
            dados_cats = []
            for cat, repos_cat in categorias.items():
                dados_cats.append([cat, len(repos_cat)])
            
            tabela_cats = ui.criar_tabela("Por Categoria", ["Categoria", "Repositórios"], dados_cats)
            ui.console.print(tabela_cats)

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
