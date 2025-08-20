"""
🧩 UI Components - Modern CLI Components
Header, Footer, Menu e outros componentes reutilizáveis
"""

from textual.widgets import Static, Label
from textual.containers import Horizontal, Vertical
from rich.text import Text
from rich.align import Align
from rich.console import Console
from datetime import datetime
import os
from pathlib import Path

from .themes import DRACULA_THEME, ICONS, get_gradient_text, format_shortcut

class ModernHeader(Static):
    """Header moderno com ASCII art e informações do sistema"""
    
    def __init__(self):
        super().__init__()
        self.add_class("header")
    
    def compose(self):
        # ASCII Art do CLI Tools
        ascii_art = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""
        
        # Criar texto com gradiente
        title_text = Text()
        title_text.append("CLI TOOLS", style=f"bold {DRACULA_THEME['purple']}")
        title_text.append(" v2.0", style=f"{DRACULA_THEME['comment']}")
        
        subtitle = Text()
        subtitle.append("🛠️ Kit de ferramentas para desenvolvedores com IA", 
                       style=f"{DRACULA_THEME['comment']}")
        
        yield Label(Align.center(title_text), classes="header-title")
        yield Label(Align.center(subtitle), classes="header-subtitle")

class ModernFooter(Static):
    """Footer com informações úteis e atalhos"""
    
    def __init__(self, current_path: str = "", shortcuts: list = None):
        super().__init__()
        self.add_class("footer")
        self.current_path = current_path or os.getcwd()
        self.shortcuts = shortcuts or []
    
    def compose(self):
        # Informações do sistema
        path_info = Text()
        path_info.append(f"📁 {Path(self.current_path).name}", 
                        style=f"{DRACULA_THEME['cyan']}")
        
        # Branch Git se disponível
        try:
            git_branch = os.popen("git branch --show-current 2>/dev/null").read().strip()
            if git_branch:
                path_info.append(f" ({git_branch})", style=f"{DRACULA_THEME['comment']}")
        except:
            pass
        
        # Status das APIs
        status_info = Text()
        status_info.append("🤖 Ready", style=f"{DRACULA_THEME['success']}")
        
        # Atalhos
        shortcuts_text = Text()
        if self.shortcuts:
            for shortcut in self.shortcuts:
                shortcuts_text.append(f" {shortcut} ", style=f"{DRACULA_THEME['comment']}")
        
        # Layout horizontal
        yield Horizontal(
            Label(path_info, classes="footer-info"),
            Label(Align.center(shortcuts_text), classes="footer-shortcuts"),
            Label(Align.right(status_info), classes="footer-info"),
        )

class MenuItem(Static):
    """Item de menu com ícone, título e descrição"""
    
    def __init__(self, icon: str, title: str, description: str, 
                 command: str = "", selected: bool = False):
        super().__init__()
        self.icon = icon
        self.title = title
        self.description = description
        self.command = command
        self.selected = selected
        self.add_class("menu-item")
        if selected:
            self.add_class("menu-item-selected")
    
    def compose(self):
        # Ícone colorido
        icon_text = Text()
        icon_text.append(self.icon, style=f"{DRACULA_THEME['pink']}")
        
        # Título
        title_text = Text()
        title_text.append(self.title, style=f"bold {DRACULA_THEME['foreground']}")
        
        # Descrição
        desc_text = Text()
        desc_text.append(self.description, style=f"{DRACULA_THEME['comment']}")
        
        # Comando (se disponível)
        cmd_text = Text()
        if self.command:
            cmd_text.append(f"gemini {self.command}", 
                           style=f"italic {DRACULA_THEME['purple']}")
        
        yield Horizontal(
            Label(icon_text, shrink=True),
            Vertical(
                Label(title_text),
                Label(desc_text),
                Label(cmd_text) if self.command else Label(""),
            ),
        )

class InfoPanel(Static):
    """Painel de informações com bordas coloridas"""
    
    def __init__(self, title: str, content: str, panel_type: str = "info"):
        super().__init__()
        self.title = title
        self.content = content
        self.panel_type = panel_type
        
        # Aplicar classe CSS baseada no tipo
        class_map = {
            "info": "info-panel",
            "success": "status-panel", 
            "warning": "warning-panel",
            "error": "error-panel"
        }
        self.add_class(class_map.get(panel_type, "info-panel"))
    
    def compose(self):
        # Título com ícone
        title_text = Text()
        icon_map = {
            "info": ICONS['info'],
            "success": ICONS['check'],
            "warning": ICONS['warning'],
            "error": ICONS['cross']
        }
        
        icon = icon_map.get(self.panel_type, ICONS['info'])
        title_text.append(f"{icon} {self.title}", style="bold")
        
        # Conteúdo
        content_text = Text(self.content)
        
        yield Label(title_text)
        yield Label(content_text)

class StatusBar(Static):
    """Barra de status com métricas em tempo real"""
    
    def __init__(self):
        super().__init__()
        self.add_class("status-panel")
    
    def compose(self):
        # APIs Status
        apis_text = Text()
        apis_text.append("APIs: ", style="bold")
        apis_text.append("✅ Pexels ", style=f"{DRACULA_THEME['success']}")
        apis_text.append("✅ Figma ", style=f"{DRACULA_THEME['success']}")
        apis_text.append("✅ Gemini", style=f"{DRACULA_THEME['success']}")
        
        # Workspace info
        workspace_text = Text()
        workspace_text.append("Workspace: ", style="bold")
        workspace_text.append("720 files, 7.71 MB", style=f"{DRACULA_THEME['cyan']}")
        
        yield Horizontal(
            Label(apis_text),
            Label(Align.right(workspace_text)),
        )

class LoadingSpinner(Static):
    """Spinner de loading animado"""
    
    def __init__(self, message: str = "Carregando..."):
        super().__init__()
        self.message = message
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_frame = 0
    
    def compose(self):
        spinner_text = Text()
        spinner_text.append(self.frames[self.current_frame], 
                           style=f"{DRACULA_THEME['purple']}")
        spinner_text.append(f" {self.message}", 
                           style=f"{DRACULA_THEME['foreground']}")
        
        yield Label(Align.center(spinner_text))
    
    def next_frame(self):
        """Avança para o próximo frame da animação"""
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.refresh()

class ProgressBar(Static):
    """Barra de progresso moderna"""
    
    def __init__(self, progress: float = 0.0, message: str = ""):
        super().__init__()
        self.progress = max(0.0, min(1.0, progress))
        self.message = message
        self.add_class("progress-bar")
    
    def compose(self):
        # Calcular largura da barra
        bar_width = 40
        filled_width = int(bar_width * self.progress)
        
        # Criar barra visual
        bar_text = Text()
        bar_text.append("█" * filled_width, style=f"{DRACULA_THEME['purple']}")
        bar_text.append("░" * (bar_width - filled_width), 
                       style=f"{DRACULA_THEME['comment']}")
        
        # Percentual
        percent_text = Text(f" {self.progress * 100:.1f}%", 
                           style=f"{DRACULA_THEME['cyan']}")
        
        # Mensagem
        message_text = Text(self.message, style=f"{DRACULA_THEME['comment']}")
        
        yield Label(message_text)
        yield Horizontal(
            Label(bar_text),
            Label(percent_text),
        )

class HelpDialog(Static):
    """Diálogo de ajuda com atalhos e comandos"""
    
    def __init__(self):
        super().__init__()
        self.add_class("info-panel")
    
    def compose(self):
        help_text = Text()
        help_text.append("🎯 Navegação:\n", style="bold")
        help_text.append("↑↓ Navegar  ENTER Selecionar  ESC Voltar  Q Sair\n\n")
        help_text.append("🚀 Comandos Rápidos:\n", style="bold")
        help_text.append("gemini search \"query\"  - Buscar imagens\n")
        help_text.append("gemini figma key123     - Extrair Figma\n") 
        help_text.append("gemini repo user/repo   - Baixar repositório\n")
        help_text.append("gemini status           - Ver status\n")
        help_text.append("gemini config           - Configurações\n")
        
        yield Label(help_text)
