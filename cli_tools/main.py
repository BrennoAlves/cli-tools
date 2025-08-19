#!/usr/bin/env python3
"""
🛠️ Ferramentas CLI - Interface Principal
CLI nativo brasileiro com IA integrada

Uso:
    cli-tools status
    cli-tools search "consulta" -n 3
    cli-tools figma "chave_do_arquivo" --number 3
    cli-tools repo "user/repo" -q "query"
    cli-tools setup
    cli-tools config
    cli-tools costs
    cli-tools help

Versão: 1.1.0
"""

import re
import sys
import click
import subprocess
from pathlib import Path

# Adicionar paths para imports
sys.path.append(str(Path(__file__).parent))
from lib.config import ConfigAPI, validar_chaves_api
from lib.interface import InterfaceLimpa
from lib.config_ia import config_ia, NivelExplicacao

# Versão atual
__version__ = "1.1.0"

def validar_nome_repo(repo):
    """Validar nome do repositório GitHub"""
    if not repo or not isinstance(repo, str):
        return False
    
    # Formato: usuario/repositorio
    if not re.match(r'^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$', repo):
        return False
    
    # Evitar path traversal
    if '..' in repo or repo.startswith('/') or '\\' in repo:
        return False
        
    return True

def validar_consulta(consulta):
    """Validar consulta de busca"""
    if not consulta or not isinstance(consulta, str):
        return False
    
    # Limitar tamanho
    if len(consulta) > 200:
        return False
    
    # Remover caracteres perigosos
    caracteres_perigosos = ['<', '>', '"', "'", '&', ';', '|', '`', '$']
    if any(char in consulta for char in caracteres_perigosos):
        return False
        
    return True

def validar_chave_figma(chave):
    """Validar chave do Figma"""
    if not chave or not isinstance(chave, str):
        return False
    
    # Formato básico de chave Figma
    if not re.match(r'^[a-zA-Z0-9-]+$', chave):
        return False
    
    # Evitar path traversal
    if '..' in chave or '/' in chave or '\\' in chave:
        return False
        
    return True

def sanitizar_caminho(caminho):
    """Sanitizar caminho de saída"""
    if not caminho:
        return None
    
    # Resolver caminho absoluto
    caminho_absoluto = Path(caminho).resolve()
    
    # Verificar se está dentro do diretório atual ou subdiretórios
    try:
        caminho_absoluto.relative_to(Path.cwd())
        return str(caminho_absoluto)
    except ValueError:
        # Caminho fora do diretório atual - usar diretório atual
        return str(Path.cwd() / Path(caminho).name)

def processar_flags_ia(ctx, explain, dry_run, interactive):
    """Processar flags de controle da IA"""
    # Configurar nível de explicação baseado nas flags
    if explain:
        if explain == "debug":
            config_ia.config["nivel_explicacao"] = NivelExplicacao.DEBUG.value
        elif explain == "detailed":
            config_ia.config["nivel_explicacao"] = NivelExplicacao.DETALHADO.value
        else:
            config_ia.config["nivel_explicacao"] = NivelExplicacao.DETALHADO.value
    
    # Configurar modo dry-run
    if dry_run:
        config_ia.config["confirmar_selecoes"] = True
        config_ia.config["mostrar_criterios"] = True
    
    # Configurar modo interativo
    if interactive:
        config_ia.config["modo_interativo"] = True
    
    return config_ia.config

@click.group()
@click.version_option(version=__version__, prog_name="🛠️ CLI Tools")
@click.option('--quiet', '-q', is_flag=True, help='Modo silencioso')
@click.pass_context
def cli(ctx, quiet):
    """🛠️ Kit de ferramentas para desenvolvedores com IA"""
    ctx.ensure_object(dict)
    ctx.obj['quiet'] = quiet

@cli.command()
@click.pass_context
def status(ctx):
    """📊 Mostrar status completo do sistema"""
    
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Status das Ferramentas CLI", "Visão geral completa")
    
    # Verificar APIs
    problemas = validar_chaves_api()
    configs = {
        'pexels': {
            'ok': 'pexels' not in problemas,
            'info': 'API de busca de imagens' if 'pexels' not in problemas else problemas['pexels']
        },
        'figma': {
            'ok': 'figma' not in problemas,
            'info': 'API de extração de designs' if 'figma' not in problemas else problemas['figma']
        },
        'gemini': {
            'ok': 'gemini' not in problemas,
            'info': 'IA para seleção inteligente' if 'gemini' not in problemas else problemas['gemini']
        }
    }
    
    ui.mostrar_status_config(configs)
    
    # Mostrar dashboard de uso
    if not ctx.obj['quiet']:
        from lib.controle_uso import controlador_uso
        controlador_uso.mostrar_dashboard_uso()
    
    if not ctx.obj['quiet']:
        # Mostrar comandos disponíveis
        comandos = [
            {
                'nome': 'search',
                'uso': 'search "consulta" --count 3',
                'descricao': 'Buscar e baixar imagens'
            },
            {
                'nome': 'figma',
                'uso': 'figma "chave_do_arquivo" --max 3',
                'descricao': 'Extrair designs do Figma'
            },
            {
                'nome': 'repo',
                'uso': 'repo "user/repo" "query IA"',
                'descricao': 'Baixar repositório com IA'
            },
            {
                'nome': 'setup',
                'uso': 'setup',
                'descricao': 'Configurar sistema inicial'
            },
            {
                'nome': 'config',
                'uso': 'config',
                'descricao': 'Gerenciar configurações'
            },
            {
                'nome': 'costs',
                'uso': 'costs',
                'descricao': 'Monitorar custos das APIs'
            },
            {
                'nome': 'help',
                'uso': 'help',
                'descricao': 'Ajuda detalhada'
            }
        ]
        
        ui.mostrar_ajuda(comandos)

@cli.command()
@click.pass_context
def setup(ctx):
    """🔧 Configurar sistema inicial"""
    from lib.controle_uso import controlador_uso
    controlador_uso.setup_inicial()

@cli.command()
@click.pass_context
def config(ctx):
    """⚙️ Gerenciar configurações das APIs"""
    
    ui = InterfaceLimpa(ctx.obj['quiet'])
    ui.mostrar_cabecalho("Configuração das APIs", "Gerenciar chaves e configurações")
    
    # Mostrar configurações atuais
    print("📋 Configurações Atuais:")
    print()
    
    configs = [
        ("PEXELS_API_KEY", ConfigAPI.PEXELS_API_KEY, "Busca de imagens"),
        ("FIGMA_API_TOKEN", ConfigAPI.FIGMA_API_TOKEN, "Extração de designs"),
        ("GEMINI_API_KEY", ConfigAPI.GEMINI_API_KEY, "IA para seleção inteligente")
    ]
    
    for nome, valor, descricao in configs:
        status = "✅ Configurada" if valor else "❌ Não configurada"
        valor_mostrar = f"{valor[:10]}..." if valor and len(valor) > 10 else "Não definida"
        print(f"  {nome}:")
        print(f"    Status: {status}")
        print(f"    Valor: {valor_mostrar}")
        print(f"    Uso: {descricao}")
        print()
    
    print("📝 Para configurar:")
    print("  1. Edite o arquivo .env na raiz do projeto")
    print("  2. Adicione suas chaves de API")
    print("  3. Execute 'cli-tools setup' para verificar")
    print()
    
    arquivo_env = Path(__file__).parent.parent / ".env"
    print(f"📁 Arquivo de configuração: {arquivo_env}")

@cli.command(name='ai-config')
@click.option('--interactive', '-i', is_flag=True, help='Configuração interativa')
@click.option('--show', is_flag=True, help='Mostrar configuração atual')
@click.option('--explain', type=click.Choice(['silent', 'basic', 'detailed', 'debug']), help='Definir nível de explicação')
@click.pass_context
def ai_config(ctx, interactive, show, explain):
    """🤖 Configurar comportamento da IA"""
    
    if show:
        config_ia.mostrar_config_atual()
        return
    
    if explain:
        from lib.config_ia import NivelExplicacao
        nivel_map = {
            'silent': NivelExplicacao.SILENCIOSO,
            'basic': NivelExplicacao.BASICO,
            'detailed': NivelExplicacao.DETALHADO,
            'debug': NivelExplicacao.DEBUG
        }
        config_ia.set_nivel_explicacao(nivel_map[explain])
        click.echo(f"✅ Nível de explicação definido para: {explain}")
        return
    
    if interactive:
        config_ia.configuracao_interativa()
        return
    
    # Mostrar help se nenhuma opção foi passada
    click.echo(ctx.get_help())
    
    if not arquivo_env.exists():
        print("⚠️  Arquivo .env não encontrado!")
        print("💡 Copie .env.example para .env e configure suas chaves")

@cli.command()
@click.pass_context
def costs(ctx):
    """💰 Monitorar custos e uso das APIs"""
    
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Monitor de Custos", "Controle de uso das APIs")
    
    # Mostrar dashboard detalhado
    from lib.controle_uso import controlador_uso
    controlador_uso.mostrar_dashboard_uso()
    
    if not ctx.obj['quiet']:
        print()
        print("💡 Dicas para Economizar:")
        print("  • Use --count menor para menos requests")
        print("  • Monitore o dashboard regularmente")
        print("  • Configure alertas antes de atingir limites")
        print("  • Use cache local quando possível")
        print()
        print("🔧 Comandos Úteis:")
        print("  cli-tools setup    # Atualizar limites via IA")
        print("  cli-tools config   # Verificar configurações")
        print("  cli-tools status   # Status geral")

@cli.command()
@click.pass_context
def help(ctx):
    """❓ Ajuda e exemplos de uso"""
    
    ui = InterfaceLimpa(ctx.obj['quiet'])
    ui.mostrar_cabecalho("Ferramentas CLI", "Ajuda e exemplos")
    
    print("🛠️ Kit de ferramentas para desenvolvedores com IA")
    print()
    
    print("Comandos:")
    print("  status     Mostrar status do sistema")
    print("  search     Buscar e baixar imagens")
    print("  figma      Extrair designs do Figma")
    print("  repo       Baixar repositório com IA")
    print("  setup      Configurar sistema")
    print("  config     Gerenciar configurações")
    print("  costs      Monitorar custos")
    print()
    
    print("Exemplos:")
    print("  cli-tools search \"escritório\" --count 3")
    print("  cli-tools figma \"abc123\" --format png")
    print("  cli-tools repo \"user/repo\" \"apenas CSS\"")
    print("  cli-tools setup")
    print()
    
    print("Para mais detalhes: cli-tools <comando> --help")

@cli.command()
@click.argument('consulta')
@click.option('--count', '-c', '--number', '-n', default=3, help='Número de imagens')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--orientation', type=click.Choice(['landscape', 'portrait', 'square']), help='Orientação')
@click.option('--json', 'output_json', is_flag=True, help='Saída em formato JSON')
@click.pass_context
def search(ctx, consulta, count, output, orientation, output_json):
    """🖼️ Buscar e baixar imagens"""
    
    # Validar entrada
    if not validar_consulta(consulta):
        click.echo("❌ Consulta inválida. Use apenas texto simples sem caracteres especiais.")
        return
    
    # Limitar count
    if count > 50:
        click.echo("⚠️ Limitando busca a 50 imagens por questões de segurança.")
        count = 50
    
    # Sanitizar output
    if output:
        output = sanitizar_caminho(output)
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "tools" / "buscar-imagens.py"),
        "download",
        consulta,
        "--count", str(count)
    ]
    
    if ctx.obj['quiet']:
        cmd.insert(-3, "--quiet")
    
    if output:
        cmd.extend(["--output", output])
    
    if orientation:
        cmd.extend(["--orientation", orientation])
    
    if output_json:
        cmd.extend(["--json"])
    
    subprocess.run(cmd)

@cli.command()
@click.argument('chave_arquivo')
@click.option('--max', '--number', '-n', default=3, help='Máximo de imagens')
@click.option('--format', '-f', default='png', help='Formato da imagem')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--json', 'output_json', is_flag=True, help='Saída em formato JSON')
@click.pass_context
def figma(ctx, chave_arquivo, max, format, output, output_json):
    """🎨 Extrair designs do Figma"""
    
    # Validar chave do arquivo
    if not validar_chave_figma(chave_arquivo):
        click.echo("❌ Chave do arquivo Figma inválida. Use apenas letras, números e hífens.")
        return
    
    # Limitar max
    if max > 20:
        click.echo("⚠️ Limitando extração a 20 designs por questões de segurança.")
        max = 20
    
    # Sanitizar output
    if output:
        output = sanitizar_caminho(output)
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "tools" / "extrator-figma.py"),
        "download",
        chave_arquivo,
        "--max-images", str(max),
        "--format", format
    ]
    
    if ctx.obj['quiet']:
        cmd.insert(-4, "--quiet")
    
    if output:
        cmd.extend(["--output", output])
    
    subprocess.run(cmd)

@cli.command()
@click.argument('repositorio')
@click.argument('query', required=False)
@click.option('--query', '-q', 'query_flag', help='Query para seleção IA')
@click.option('--output', '-o', help='Diretório de saída')
@click.option('--explain', type=click.Choice(['basic', 'detailed', 'debug']), help='Nível de explicação da IA')
@click.option('--dry-run', is_flag=True, help='Mostrar o que seria feito sem executar')
@click.option('--interactive', '-i', is_flag=True, help='Modo interativo')
@click.option('--json', 'output_json', is_flag=True, help='Saída em formato JSON')
@click.pass_context
def repo(ctx, repositorio, query, query_flag, output, explain, dry_run, interactive, output_json):
    """📦 Baixar repositório com seleção IA"""
    
    # Usar query da flag se não foi passada como argumento
    if not query and query_flag:
        query = query_flag
    
    # Validar nome do repositório
    if not validar_nome_repo(repositorio):
        click.echo("❌ Nome do repositório inválido. Use o formato: usuario/repositorio")
        return
    
    # Validar query se fornecida
    if query and not validar_consulta(query):
        click.echo("❌ Query inválida. Use apenas texto simples sem caracteres especiais.")
        return
    
    # Processar flags de IA
    config_ia_atual = processar_flags_ia(ctx, explain, dry_run, interactive)
    
    # Sanitizar output
    if output:
        output = sanitizar_caminho(output)
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "tools" / "baixar-repo.py"),
        "smart" if query else "clone",
        repositorio
    ]
    
    if query:
        cmd.append(query)
    
    if ctx.obj['quiet']:
        cmd.insert(-2, "--quiet")
    
    if output:
        cmd.extend(["--output", output])
    
    if explain:
        cmd.extend(["--explain", explain])
    
    if dry_run:
        cmd.append("--dry-run")
    
    if interactive:
        cmd.append("--interactive")
    
    if output_json:
        cmd.append("--json")
    
    subprocess.run(cmd)

# Comandos de ferramentas individuais (para compatibilidade)
@cli.group()
def tools():
    """🔧 Ferramentas individuais (modo avançado)"""
    pass

@tools.command()
@click.pass_context
def images(ctx):
    """Ferramenta de imagens (modo avançado)"""
    subprocess.run([
        sys.executable,
        str(Path(__file__).parent / "tools" / "buscar-imagens.py"),
        "--help"
    ])

@tools.command()
@click.pass_context
def figma_tool(ctx):
    """Ferramenta do Figma (modo avançado)"""
    subprocess.run([
        sys.executable,
        str(Path(__file__).parent / "tools" / "extrator-figma.py"),
        "--help"
    ])

@tools.command()
@click.pass_context
def repo_tool(ctx):
    """Ferramenta de repositórios (modo avançado)"""
    subprocess.run([
        sys.executable,
        str(Path(__file__).parent / "tools" / "baixar-repo.py"),
        "--help"
    ])

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
