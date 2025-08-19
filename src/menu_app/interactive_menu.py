"""
CLI Tools - Interface Menu Interativa
Navegação por setas, cores vibrantes, estilo "cool"
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, ProgressBar, Label
from textual.reactive import reactive, var
from textual.binding import Binding
from textual.timer import Timer
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
import asyncio
import random
from typing import List, Dict, Any
from datetime import datetime


class MenuOption:
    """Opção do menu com estilo"""
    def __init__(self, title: str, description: str, icon: str, action: str, color: str = "white"):
        self.title = title
        self.description = description
        self.icon = icon
        self.action = action
        self.color = color
        self.selected = False


class InteractiveMenu(App):
    """Interface menu interativa com navegação por setas"""
    
    TITLE = "CLI Tools v2.0"
    SUB_TITLE = "Menu Interativo"
    
    CSS = """
    Screen {
        background: #0d1117;
        color: #c9d1d9;
    }
    
    #header {
        height: 8;
        background: #bd93f9;
        color: #282a36;
        content-align: center middle;
        text-style: bold;
        margin: 1;
        border: heavy #8be9fd;
    }
    
    #main-container {
        layout: horizontal;
        height: 1fr;
        margin: 0 1;
    }
    
    #menu-panel {
        width: 1fr;
        background: #161b22;
        border: solid #30363d;
        padding: 1;
        margin: 0 1 0 0;
    }
    
    #info-panel {
        width: 1fr;
        background: #0d1117;
        border: solid #21262d;
        padding: 1;
    }
    
    #footer {
        height: 3;
        background: #161b22;
        border: solid #30363d;
        margin: 1;
        padding: 1;
    }
    
    .menu-item {
        height: 3;
        margin: 0 0 1 0;
        padding: 0 1;
        border: solid transparent;
        background: #21262d;
    }
    
    .menu-item-selected {
        border: solid #f78166;
        background: #332621;
        color: #f78166;
        text-style: bold;
    }
    
    .menu-item-icon {
        color: #58a6ff;
        text-style: bold;
    }
    
    .status-bar {
        background: #0d1117;
        color: #7d8590;
        height: 1;
        margin: 1 0 0 0;
    }
    
    #progress-container {
        height: 3;
        margin: 1 0;
        background: #161b22;
        border: solid #30363d;
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑ Subir", priority=True),
        Binding("down,j", "cursor_down", "↓ Descer", priority=True),
        Binding("enter", "select", "⏎ Selecionar", priority=True),
        Binding("escape,q", "quit", "Sair", priority=True),
        Binding("r", "refresh", "🔄 Atualizar"),
        Binding("h", "help", "❓ Ajuda"),
    ]
    
    # Estado reativo
    selected_index = reactive(0)
    is_loading = reactive(False)
    status_message = reactive("Pronto")
    
    def __init__(self):
        super().__init__()
        self.console = Console()
        self.menu_options = self.create_menu_options()
        self.setup_timers()
    
    def create_menu_options(self) -> List[MenuOption]:
        """Criar opções do menu com estilo"""
        return [
            MenuOption(
                "🔍 Buscar Imagens", 
                "Encontre e baixe imagens incríveis do Pexels",
                "🖼️", 
                "search",
                "#58a6ff"
            ),
            MenuOption(
                "🎨 Extrair Figma", 
                "Baixe designs e assets direto do Figma",
                "🎭", 
                "figma",
                "#f78166"
            ),
            MenuOption(
                "📦 Baixar Repositório", 
                "Clone repos com seleção inteligente de arquivos",
                "📁", 
                "repo",
                "#56d364"
            ),
            MenuOption(
                "📊 Status do Sistema", 
                "Veja saúde das APIs e estatísticas",
                "📈", 
                "status",
                "#e3b341"
            ),
            MenuOption(
                "⚙️ Configurações", 
                "Configure chaves de API e preferências",
                "🔧", 
                "config",
                "#bc8cff"
            ),
            MenuOption(
                "🎯 Ferramentas Extras", 
                "Utilitários e funcionalidades avançadas",
                "🛠️", 
                "tools",
                "#ff7b72"
            ),
        ]
    
    def setup_timers(self):
        """Configurar timers para animações"""
        self.status_timer = None
        self.animation_timer = None
    
    def compose(self) -> ComposeResult:
        """Compor interface"""
        # Header animado
        yield Static(self.get_animated_header(), id="header")
        
        # Container principal
        with Container(id="main-container"):
            # Panel do menu
            with Vertical(id="menu-panel"):
                yield Static("🎮 MENU PRINCIPAL", classes="menu-title")
                yield Static("", id="menu-items")
                yield Static("", classes="status-bar", id="status-bar")
            
            # Panel de informações
            with Vertical(id="info-panel"):
                yield Static("ℹ️ INFORMAÇÕES", classes="info-title")
                yield Static("", id="info-content")
                yield Static("", id="stats-display")
        
        # Container de progresso
        with Container(id="progress-container"):
            yield ProgressBar(id="progress-bar", show_eta=False)
            yield Static("", id="progress-text")
        
        # Footer com atalhos
        yield Static(self.get_footer_text(), id="footer")
    
    def get_animated_header(self) -> str:
        """Header com gradiente animado"""
        return """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗  ║
║ ██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝  ║
║ ██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗  ║
║ ╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║  ║
║  ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝  ║
║                                                                      ║
║                    🚀 Kit de Ferramentas v2.0 🚀                     ║
╚══════════════════════════════════════════════════════════════════════╝
        """
    
    def get_footer_text(self) -> str:
        """Texto do footer com atalhos"""
        return """
┌─ CONTROLES ─────────────────────────────────────────────────────────┐
│ ↑↓ Navegar  │  ⏎ Selecionar  │  Q Sair  │  R Atualizar  │  H Ajuda │
└─────────────────────────────────────────────────────────────────────┘
        """
    
    def on_mount(self) -> None:
        """Inicialização"""
        self.update_menu_display()
        self.update_info_display()
        self.update_status("Sistema inicializado")
        
        # Iniciar animações
        self.set_interval(2.0, self.animate_status)
        self.set_interval(0.5, self.update_stats)
    
    def update_menu_display(self) -> None:
        """Atualizar display do menu"""
        menu_text = Text()
        
        for i, option in enumerate(self.menu_options):
            # Indicador de seleção
            if i == self.selected_index:
                prefix = "▶ "
                style = "bold reverse"
                bg_color = "#332621"
            else:
                prefix = "  "
                style = "dim"
                bg_color = None
            
            # Linha do menu
            line = f"{prefix}{option.icon} {option.title}"
            menu_text.append(line + "\n", style=style)
        
        self.query_one("#menu-items", Static).update(menu_text)
    
    def update_info_display(self) -> None:
        """Atualizar painel de informações"""
        if 0 <= self.selected_index < len(self.menu_options):
            option = self.menu_options[self.selected_index]
            
            info_text = Text()
            info_text.append(f"{option.icon} {option.title}\n\n", style="bold #58a6ff")
            info_text.append(f"{option.description}\n\n", style="#c9d1d9")
            
            # Adicionar informações específicas
            if option.action == "search":
                info_text.append("• Busca no Pexels\n", style="#7d8590")
                info_text.append("• Múltiplos formatos\n", style="#7d8590")
                info_text.append("• Download automático\n", style="#7d8590")
            elif option.action == "figma":
                info_text.append("• Extração de assets\n", style="#7d8590")
                info_text.append("• Formatos PNG/SVG/JPG\n", style="#7d8590")
                info_text.append("• Organização automática\n", style="#7d8590")
            elif option.action == "repo":
                info_text.append("• Seleção inteligente\n", style="#7d8590")
                info_text.append("• Análise com IA\n", style="#7d8590")
                info_text.append("• Filtros personalizados\n", style="#7d8590")
            elif option.action == "status":
                info_text.append("• Status das APIs\n", style="#7d8590")
                info_text.append("• Métricas de uso\n", style="#7d8590")
                info_text.append("• Saúde do sistema\n", style="#7d8590")
            elif option.action == "config":
                info_text.append("• Chaves de API\n", style="#7d8590")
                info_text.append("• Configurações globais\n", style="#7d8590")
                info_text.append("• Preferências de usuário\n", style="#7d8590")
            elif option.action == "tools":
                info_text.append("• Utilitários diversos\n", style="#7d8590")
                info_text.append("• Funcionalidades extras\n", style="#7d8590")
                info_text.append("• Ferramentas avançadas\n", style="#7d8590")
            
            self.query_one("#info-content", Static).update(info_text)
    
    def update_stats(self) -> None:
        """Atualizar estatísticas em tempo real"""
        now = datetime.now()
        stats_text = Text()
        
        stats_text.append("📊 ESTATÍSTICAS\n\n", style="bold #e3b341")
        stats_text.append(f"🕐 {now.strftime('%H:%M:%S')}\n", style="#7d8590")
        stats_text.append(f"📅 {now.strftime('%d/%m/%Y')}\n", style="#7d8590")
        stats_text.append(f"🔥 APIs: 3/3 Online\n", style="#56d364")
        stats_text.append(f"💾 Workspace: 584MB\n", style="#58a6ff")
        stats_text.append(f"⚡ Performance: {random.randint(85, 99)}%\n", style="#f78166")
        
        self.query_one("#stats-display", Static).update(stats_text)
    
    def update_status(self, message: str) -> None:
        """Atualizar barra de status"""
        self.status_message = message
        status_text = f"💡 {message}"
        self.query_one("#status-bar", Static).update(status_text)
    
    def animate_status(self) -> None:
        """Animar mensagens de status"""
        messages = [
            "Sistema operacional",
            "APIs conectadas",
            "Workspace configurado",
            "Pronto para uso",
            "Aguardando comando..."
        ]
        message = random.choice(messages)
        self.update_status(message)
    
    def action_cursor_up(self) -> None:
        """Mover cursor para cima"""
        self.selected_index = (self.selected_index - 1) % len(self.menu_options)
        self.update_menu_display()
        self.update_info_display()
        self.update_status(f"Selecionado: {self.menu_options[self.selected_index].title}")
    
    def action_cursor_down(self) -> None:
        """Mover cursor para baixo"""
        self.selected_index = (self.selected_index + 1) % len(self.menu_options)
        self.update_menu_display()
        self.update_info_display()
        self.update_status(f"Selecionado: {self.menu_options[self.selected_index].title}")
    
    def action_select(self) -> None:
        """Selecionar opção atual"""
        if 0 <= self.selected_index < len(self.menu_options):
            option = self.menu_options[self.selected_index]
            self.execute_action(option.action)
    
    def action_refresh(self) -> None:
        """Atualizar interface"""
        self.update_status("Atualizando...")
        self.update_menu_display()
        self.update_info_display()
        self.update_status("Interface atualizada")
    
    def action_help(self) -> None:
        """Mostrar ajuda"""
        self.update_status("Use ↑↓ para navegar, ⏎ para selecionar")
    
    async def execute_action(self, action: str) -> None:
        """Executar ação selecionada"""
        self.update_status(f"Executando {action}...")
        
        # Mostrar progresso
        progress = self.query_one("#progress-bar", ProgressBar)
        progress_text = self.query_one("#progress-text", Static)
        
        progress.update(total=100)
        
        if action == "search":
            await self.simulate_search()
        elif action == "figma":
            await self.simulate_figma()
        elif action == "repo":
            await self.simulate_repo()
        elif action == "status":
            await self.simulate_status()
        elif action == "config":
            await self.simulate_config()
        elif action == "tools":
            await self.simulate_tools()
        
        # Limpar progresso
        progress.update(progress=0)
        progress_text.update("")
        self.update_status("Operação concluída")
    
    async def simulate_search(self) -> None:
        """Simular busca de imagens"""
        progress = self.query_one("#progress-bar", ProgressBar)
        progress_text = self.query_one("#progress-text", Static)
        
        steps = [
            "Conectando ao Pexels...",
            "Buscando imagens...",
            "Analisando resultados...",
            "Baixando arquivos...",
            "Organizando workspace..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.update(f"🔍 {step}")
            progress.update(progress=(i + 1) * 20)
            await asyncio.sleep(0.5)
        
        self.update_status("✅ 5 imagens baixadas com sucesso!")
    
    async def simulate_figma(self) -> None:
        """Simular extração do Figma"""
        progress = self.query_one("#progress-bar", ProgressBar)
        progress_text = self.query_one("#progress-text", Static)
        
        steps = [
            "Conectando ao Figma...",
            "Analisando arquivo...",
            "Extraindo assets...",
            "Convertendo formatos...",
            "Salvando arquivos..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.update(f"🎨 {step}")
            progress.update(progress=(i + 1) * 20)
            await asyncio.sleep(0.6)
        
        self.update_status("✅ Designs extraídos com sucesso!")
    
    async def simulate_repo(self) -> None:
        """Simular download de repositório"""
        progress = self.query_one("#progress-bar", ProgressBar)
        progress_text = self.query_one("#progress-text", Static)
        
        steps = [
            "Analisando repositório...",
            "Consultando IA...",
            "Selecionando arquivos...",
            "Clonando conteúdo...",
            "Organizando estrutura..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.update(f"📦 {step}")
            progress.update(progress=(i + 1) * 20)
            await asyncio.sleep(0.7)
        
        self.update_status("✅ Repositório baixado com sucesso!")
    
    async def simulate_status(self) -> None:
        """Simular verificação de status"""
        progress = self.query_one("#progress-bar", ProgressBar)
        progress_text = self.query_one("#progress-text", Static)
        
        steps = [
            "Verificando APIs...",
            "Testando conectividade...",
            "Coletando métricas...",
            "Analisando performance...",
            "Gerando relatório..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.update(f"📊 {step}")
            progress.update(progress=(i + 1) * 20)
            await asyncio.sleep(0.4)
        
        self.update_status("✅ Sistema funcionando perfeitamente!")
    
    async def simulate_config(self) -> None:
        """Simular configuração"""
        progress = self.query_one("#progress-bar", ProgressBar)
        progress_text = self.query_one("#progress-text", Static)
        
        steps = [
            "Carregando configurações...",
            "Validando chaves...",
            "Testando APIs...",
            "Salvando preferências...",
            "Aplicando mudanças..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.update(f"⚙️ {step}")
            progress.update(progress=(i + 1) * 20)
            await asyncio.sleep(0.5)
        
        self.update_status("✅ Configurações atualizadas!")
    
    async def simulate_tools(self) -> None:
        """Simular ferramentas extras"""
        progress = self.query_one("#progress-bar", ProgressBar)
        progress_text = self.query_one("#progress-text", Static)
        
        steps = [
            "Carregando ferramentas...",
            "Inicializando módulos...",
            "Preparando interface...",
            "Configurando ambiente...",
            "Pronto para uso..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.update(f"🛠️ {step}")
            progress.update(progress=(i + 1) * 20)
            await asyncio.sleep(0.3)
        
        self.update_status("✅ Ferramentas carregadas!")


if __name__ == "__main__":
    app = InteractiveMenu()
    app.run()
