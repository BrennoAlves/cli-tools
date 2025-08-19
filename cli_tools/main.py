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

Versão: 1.1.0 - Workspace Inteligente
"""

import re
import sys
import click
import subprocess
import os
from pathlib import Path

# Capturar diretório atual do usuário no início
USER_CURRENT_DIR = os.getcwd()

# Adicionar paths para imports
sys.path.append(str(Path(__file__).parent))
from core.config import ConfigAPI, validar_chaves_api
from core.interface import InterfaceLimpa
from core.config_ia import config_ia, NivelExplicacao
from core.config_diretorios import config_diretorios

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

def sanitizar_caminho(caminho, tipo_material='imagens'):
    """Sanitizar caminho de saída com suporte a diretórios configurados"""
    if not caminho:
        # Se não especificado, usar diretório configurado para o tipo
        return config_diretorios.obter_diretorio(tipo_material)
    
    # Usar diretório preservado pelo wrapper
    user_cwd = os.environ.get('USER_PWD', os.getcwd())
    
    if caminho == '.':
        return user_cwd
    elif caminho == 'default':
        # Usar diretório padrão configurado
        return config_diretorios.obter_diretorio(tipo_material)
    else:
        output_path = Path(caminho)
        if not output_path.is_absolute():
            caminho = str(Path(user_cwd) / output_path)
        else:
            caminho = str(output_path)
    
    # Verificar se não é caminho perigoso
    if caminho.startswith('/etc') or caminho.startswith('/root'):
        return config_diretorios.obter_diretorio(tipo_material)
    
    return caminho

def processar_flags_ia(ctx, explain, dry_run, interactive):
    """Processar flags de controle da IA"""
    # Configurar nível de explicação baseado nas flags
    if explain:
        if explain == "debug":
            config_ia.config["nivel_explicacao"] = NivelExplicacao.DEBUG.value
        elif explain == "detalhado":
            config_ia.config["nivel_explicacao"] = NivelExplicacao.DETALHADO.value
        elif explain == "silencioso":
            config_ia.config["nivel_explicacao"] = NivelExplicacao.SILENCIOSO.value
        else:  # basico
            config_ia.config["nivel_explicacao"] = NivelExplicacao.BASICO.value
    
    # Configurar modo dry-run
    if dry_run:
        config_ia.config["confirmar_selecoes"] = True
        config_ia.config["mostrar_criterios"] = True
    
    # Configurar modo interativo
    if interactive:
        config_ia.config["modo_interativo"] = True
    
    return config_ia.config

@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="🛠️ CLI Tools")
@click.option('--quiet', '-q', is_flag=True, help='Modo silencioso')
@click.pass_context
def cli(ctx, quiet):
    """🛠️ Kit de ferramentas para desenvolvedores com IA"""
    ctx.ensure_object(dict)
    ctx.obj['quiet'] = quiet
    
    # Se nenhum comando foi especificado, abrir navegação interativa
    if ctx.invoked_subcommand is None:
        try:
            from core.navegacao_cli import navegador_cli
            navegador_cli.navegar()
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
        except Exception as e:
            print(f"\n❌ Erro na navegação: {e}")
            print("💡 Use 'cli-tools --help' para ver comandos disponíveis")

@cli.command()
@click.option('--dashboard', '-d', type=click.Choice(['a', 'b', 'c', 'd', 'table', 'panels', 'layout', 'live']), 
              help='Tipo de dashboard: a/table=Tabela, b/panels=Painéis, c/layout=Layout, d/live=Tempo Real')
@click.option('--legacy', is_flag=True, help='Usar interface antiga (compatibilidade)')
@click.pass_context
def status(ctx, dashboard, legacy):
    """📊 Mostrar status completo do sistema
    
    Dashboards disponíveis:
    - a/table: Rich Table simples com informações de APIs
    - b/panels: Rich Panel com seções organizadas por serviço  
    - c/layout: Rich Layout com múltiplas colunas e gráficos
    - d/live: Rich Live Dashboard com updates em tempo real
    """
    
    # Se modo legacy ou quiet, usar interface antiga
    if legacy or ctx.obj['quiet']:
        _status_legacy(ctx)
        return
    
    # Usar dashboards Rich avançados
    from core.rich_dashboards_simple import rich_dashboards_simple
    
    # Se não especificou dashboard, mostrar menu de seleção
    if not dashboard:
        from rich.console import Console
        from rich.prompt import Prompt
        from rich.panel import Panel
        from rich.text import Text
        
        console = Console()
        
        menu_text = """[bold magenta]🎯 CLI Tools - Seleção de Dashboard[/bold magenta]

Escolha o tipo de dashboard que deseja visualizar:

[bold cyan]a) table[/bold cyan]  - Rich Table simples com informações de APIs
[bold cyan]b) panels[/bold cyan] - Rich Panel com seções organizadas por serviço  
[bold cyan]c) layout[/bold cyan] - Rich Layout com múltiplas colunas e gráficos
[bold cyan]d) live[/bold cyan]   - Rich Live Dashboard com updates em tempo real

[blue]💡 Dica: Use --dashboard/-d para ir direto: cli-tools status -d a[/blue]"""
        
        console.print(Panel(menu_text, title="Dashboard Selection", border_style="magenta"))
        
        dashboard = Prompt.ask(
            "\n[bold magenta]Selecione o dashboard[/bold magenta]",
            choices=["a", "b", "c", "d", "table", "panels", "layout", "live"],
            default="a"
        )
    
    # Mapear aliases
    dashboard_map = {
        'a': 'table',
        'b': 'panels', 
        'c': 'layout',
        'd': 'live',
        'table': 'table',
        'panels': 'panels',
        'layout': 'layout', 
        'live': 'live'
    }
    
    dashboard_type = dashboard_map.get(dashboard, 'table')
    
    # Executar dashboard selecionado
    if dashboard_type == 'table':
        rich_dashboards_simple.dashboard_version_a_table()
    elif dashboard_type == 'panels':
        rich_dashboards_simple.dashboard_version_b_panels()
    elif dashboard_type == 'layout':
        rich_dashboards_simple.dashboard_version_c_layout()
    elif dashboard_type == 'live':
        rich_dashboards_simple.dashboard_version_d_live()


def _status_legacy(ctx):
    """Versão legacy do comando status para compatibilidade"""
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
        from core.controle_uso import controlador_uso
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
    from core.controle_uso import controlador_uso
    controlador_uso.setup_inicial()

@cli.command()
@click.option('--workspace', help='Configurar diretório principal de trabalho')
@click.option('--imagens', help='Configurar diretório para imagens')
@click.option('--figma', help='Configurar diretório para designs Figma')
@click.option('--repos', help='Configurar diretório para repositórios')
@click.option('--show-dirs', is_flag=True, help='Mostrar diretórios configurados')
@click.pass_context
def config(ctx, workspace, imagens, figma, repos, show_dirs):
    """⚙️ Gerenciar configurações das APIs e diretórios"""
    
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    # Gerenciar diretórios
    if workspace:
        if config_diretorios.configurar_workspace(workspace):
            click.echo(f"✅ Workspace configurado: {workspace}")
        else:
            click.echo(f"❌ Erro ao configurar workspace: {workspace}")
        return
    
    if imagens:
        if config_diretorios.configurar_diretorio_especifico('imagens', imagens):
            click.echo(f"✅ Diretório de imagens configurado: {imagens}")
        else:
            click.echo(f"❌ Erro ao configurar diretório de imagens: {imagens}")
        return
    
    if figma:
        if config_diretorios.configurar_diretorio_especifico('figma', figma):
            click.echo(f"✅ Diretório Figma configurado: {figma}")
        else:
            click.echo(f"❌ Erro ao configurar diretório Figma: {figma}")
        return
    
    if repos:
        if config_diretorios.configurar_diretorio_especifico('repos', repos):
            click.echo(f"✅ Diretório de repositórios configurado: {repos}")
        else:
            click.echo(f"❌ Erro ao configurar diretório de repositórios: {repos}")
        return
    
    if show_dirs:
        status = config_diretorios.status()
        click.echo("\n📁 Diretórios Configurados:")
        click.echo(f"  Workspace: {status['workspace']} {'✅' if status['workspace_exists'] else '❌'}")
        click.echo(f"  Imagens:   {status['imagens']} {'✅' if status['imagens_exists'] else '❌'}")
        click.echo(f"  Figma:     {status['figma']} {'✅' if status['figma_exists'] else '❌'}")
        click.echo(f"  Repos:     {status['repos']} {'✅' if status['repos_exists'] else '❌'}")
        return
    
    # Mostrar configuração completa
    ui.mostrar_cabecalho("Configuração Completa", "APIs e Diretórios")
    
    # APIs
    print("🔑 APIs:")
    config_api = ConfigAPI()
    configs = [
        ("PEXELS_API_KEY", config_api.pexels_key, "Busca de imagens"),
        ("FIGMA_API_TOKEN", config_api.figma_token, "Extração de designs"),
        ("GEMINI_API_KEY", config_api.gemini_key, "IA para seleção inteligente")
    ]
    
    for nome, valor, descricao in configs:
        status = "✅ Configurada" if valor else "❌ Não configurada"
        print(f"  {nome}: {status}")
    
    print()
    
    # Diretórios
    status = config_diretorios.status()
    print("📁 Diretórios:")
    print(f"  Workspace: {status['workspace']} {'✅' if status['workspace_exists'] else '❌'}")
    print(f"  Imagens:   {status['imagens']} {'✅' if status['imagens_exists'] else '❌'}")
    print(f"  Figma:     {status['figma']} {'✅' if status['figma_exists'] else '❌'}")
    print(f"  Repos:     {status['repos']} {'✅' if status['repos_exists'] else '❌'}")
    print()
    
    print("🔧 Comandos de configuração:")
    print("  cli-tools config --workspace /novo/caminho")
    print("  cli-tools config --imagens /caminho/imagens")
    print("  cli-tools config --show-dirs")
    print()
    
    arquivo_env = Path(__file__).parent.parent / ".env"
    print(f"📁 Arquivo de configuração: {arquivo_env}")

@cli.command(name='ai-config')
@click.option('--interactive', '-i', is_flag=True, help='Configuração interativa')
@click.option('--show', is_flag=True, help='Mostrar configuração atual')
@click.option('--explain', type=click.Choice(['silencioso', 'basico', 'detalhado', 'debug']), help='Definir nível de explicação')
@click.option('--modelo', type=click.Choice(['conservador', 'equilibrado', 'yolo']), help='Aplicar modelo pré-configurado')
@click.pass_context
def ai_config(ctx, interactive, show, explain, modelo):
    """🤖 Configurar comportamento da IA"""
    
    if show:
        config_ia.mostrar_config_atual()
        return
    
    if modelo:
        from core.config_ia import ModeloIA
        modelo_map = {
            'conservador': ModeloIA.CONSERVADOR,
            'equilibrado': ModeloIA.EQUILIBRADO,
            'yolo': ModeloIA.YOLO
        }
        config_ia.aplicar_modelo(modelo_map[modelo])
        
        modelo_desc = {
            'conservador': '🛡️  Conservador - Máxima segurança e transparência',
            'equilibrado': '⚖️  Equilibrado - Padrão balanceado',
            'yolo': '🚀 YOLO - Rápido e direto'
        }
        
        click.echo(f"✅ Modelo {modelo_desc[modelo]} aplicado!")
        return
    
    if explain:
        from core.config_ia import NivelExplicacao
        nivel_map = {
            'silencioso': NivelExplicacao.SILENCIOSO,
            'basico': NivelExplicacao.BASICO,
            'detalhado': NivelExplicacao.DETALHADO,
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

@cli.command()
@click.pass_context
def costs(ctx):
    """💰 Monitorar custos e uso das APIs"""
    
    ui = InterfaceLimpa(ctx.obj['quiet'])
    
    if not ctx.obj['quiet']:
        ui.mostrar_cabecalho("Monitor de Custos", "Controle de uso das APIs")
    
    # Mostrar dashboard detalhado
    from core.controle_uso import controlador_uso
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
@click.option('--output', '-o', help='Diretório de saída (. = atual, default = configurado)')
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
    
    # Sanitizar output usando sistema de diretórios
    output_path = sanitizar_caminho(output, 'imagens')
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "tools" / "buscar-imagens.py"),
        "download",
        consulta,
        "--count", str(count)
    ]
    
    if ctx.obj['quiet']:
        cmd.insert(-3, "--quiet")
    
    if output_path:
        cmd.extend(["--output", output_path])
    
    if orientation:
        cmd.extend(["--orientation", orientation])
    
    if output_json:
        cmd.extend(["--format", "json"])
    
    subprocess.run(cmd)
    
    if orientation:
        cmd.extend(["--orientation", orientation])
    
    if output_json:
        cmd.extend(["--format", "json"])
    
    subprocess.run(cmd)

@cli.command()
@click.argument('chave_arquivo')
@click.option('--max', '--number', '-n', default=3, help='Máximo de imagens')
@click.option('--format', '-f', default='png', help='Formato da imagem')
@click.option('--output', '-o', help='Diretório de saída (. = atual, default = configurado)')
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
    
    # Sanitizar output usando sistema de diretórios
    output_path = sanitizar_caminho(output, 'figma')
    
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
    
    if output_path:
        cmd.extend(["--output", output_path])
    
    subprocess.run(cmd)

@cli.command()
@click.argument('repositorio')
@click.argument('query', required=False)
@click.option('--query', '-q', 'query_flag', help='Query para seleção IA')
@click.option('--output', '-o', help='Diretório de saída (. = atual, default = configurado)')
@click.option('--explain', type=click.Choice(['silencioso', 'basico', 'detalhado', 'debug']), help='Nível de explicação da IA')
@click.option('--dry-run', is_flag=True, help='Mostrar o que seria feito sem executar')
@click.option('--interactive', '-i', is_flag=True, help='Modo interativo')
@click.option('--no-ai', is_flag=True, help='Baixar repositório completo sem IA')
@click.option('--json', 'output_json', is_flag=True, help='Saída em formato JSON')
@click.pass_context
def repo(ctx, repositorio, query, query_flag, output, explain, dry_run, interactive, no_ai, output_json):
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
    
    # Sanitizar output usando sistema de diretórios
    output_path = sanitizar_caminho(output, 'repos')
    
    # Determinar modo de operação
    if no_ai:
        # Modo sem IA - sempre clone completo
        modo = "clone"
    elif query:
        # Modo com IA - seleção inteligente
        modo = "smart"
    else:
        # Modo padrão - clone completo
        modo = "clone"
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "tools" / "baixar-repo.py"),
        modo,
        repositorio
    ]
    
    # Adicionar query apenas se não for --no-ai
    if query and not no_ai:
        cmd.append(query)
    
    if ctx.obj['quiet']:
        cmd.insert(-2, "--quiet")
    
    if output_path:
        cmd.extend(["--output", output_path])
    
    if explain and not no_ai:
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
