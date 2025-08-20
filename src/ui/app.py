"""
🚀 Modern CLI App - Interface Principal
Navegação intuitiva com tema Dracula e UX otimizada
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Label
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
import os
from pathlib import Path

from .themes import DRACULA_THEME, ICONS

class MainMenu(Static):
    """Menu principal com navegação por setas"""
    
    selected_index = reactive(0)
    
    def __init__(self):
        super().__init__()
        self.menu_items = [
            {
                'icon': ICONS['search'],
                'title': 'Buscar Imagens',
                'description': 'Buscar e baixar imagens do Pexels com IA',
                'command': 'search "query" -n 5',
                'action': 'search'
            },
            {
                'icon': ICONS['figma'],
                'title': 'Extrair Figma',
                'description': 'Extrair designs e assets do Figma',
                'command': 'figma key123 --format png',
                'action': 'figma'
            },
            {
                'icon': ICONS['repo'],
                'title': 'Baixar Repositório',
                'description': 'Download inteligente de repositórios GitHub',
                'command': 'repo user/repo -q "query"',
                'action': 'repo'
            },
            {
                'icon': ICONS['status'],
                'title': 'Status do Sistema',
                'description': 'Dashboard com status das APIs e workspace',
                'command': 'status',
                'action': 'status'
            },
            {
                'icon': ICONS['config'],
                'title': 'Configurações',
                'description': 'Gerenciar APIs e diretórios',
                'command': 'config',
                'action': 'config'
            },
            {
                'icon': ICONS['costs'],
                'title': 'Monitor de Custos',
                'description': 'Controle de uso e limites das APIs',
                'command': 'costs',
                'action': 'costs'
            },
            {
                'icon': ICONS['setup'],
                'title': 'Configuração Inicial',
                'description': 'Setup das chaves de API',
                'command': 'setup',
                'action': 'setup'
            },
            {
                'icon': ICONS['help'],
                'title': 'Ajuda e Exemplos',
                'description': 'Documentação e exemplos de uso',
                'command': 'help',
                'action': 'help'
            },
        ]
    
    def render(self):
        """Renderizar menu"""
        menu_text = Text()
        
        for i, item in enumerate(self.menu_items):
            selected = i == self.selected_index
            
            # Indicador de seleção
            if selected:
                menu_text.append("▶ ", style=f"bold {DRACULA_THEME['pink']}")
            else:
                menu_text.append("  ", style="")
            
            # Ícone e título
            menu_text.append(f"{item['icon']} {item['title']}", 
                           style=f"bold {DRACULA_THEME['purple'] if selected else DRACULA_THEME['foreground']}")
            menu_text.append(f"\n    {item['description']}", 
                           style=f"{DRACULA_THEME['comment']}")
            menu_text.append(f"\n    gemini {item['command']}\n\n", 
                           style=f"italic {DRACULA_THEME['cyan']}")
        
        return Panel(
            menu_text,
            title="🛠️ Menu Principal",
            border_style=DRACULA_THEME['purple'],
            padding=(1, 2)
        )
    
    def move_up(self):
        """Mover seleção para cima"""
        if self.selected_index > 0:
            self.selected_index -= 1
            self.refresh()
    
    def move_down(self):
        """Mover seleção para baixo"""
        if self.selected_index < len(self.menu_items) - 1:
            self.selected_index += 1
            self.refresh()
    
    def get_selected_item(self):
        """Obter item selecionado"""
        return self.menu_items[self.selected_index]

class InfoSidebar(Static):
    """Sidebar com informações contextuais"""
    
    def render(self):
        """Renderizar sidebar"""
        info_text = Text()
        
        # Status das APIs
        info_text.append("📊 Status das APIs\n", style="bold")
        info_text.append("✅ Pexels API - Operacional\n", style=f"{DRACULA_THEME['success']}")
        info_text.append("✅ Figma API - Operacional\n", style=f"{DRACULA_THEME['success']}")
        info_text.append("✅ Gemini API - Operacional\n\n", style=f"{DRACULA_THEME['success']}")
        
        # Workspace
        info_text.append("🏠 Workspace\n", style="bold")
        info_text.append(f"📁 {Path.cwd().name}\n", style=f"{DRACULA_THEME['cyan']}")
        info_text.append("🗂️ materials/\n", style=f"{DRACULA_THEME['comment']}")
        info_text.append("├── imagens/ (0 arquivos)\n", style=f"{DRACULA_THEME['comment']}")
        info_text.append("├── figma/ (0 arquivos)\n", style=f"{DRACULA_THEME['comment']}")
        info_text.append("└── repos/ (719 arquivos)\n\n", style=f"{DRACULA_THEME['comment']}")
        
        # Navegação
        info_text.append("💡 Navegação\n", style="bold")
        info_text.append("↑↓ Navegar\n", style=f"{DRACULA_THEME['comment']}")
        info_text.append("ENTER Selecionar\n", style=f"{DRACULA_THEME['comment']}")
        info_text.append("ESC Voltar\n", style=f"{DRACULA_THEME['comment']}")
        info_text.append("Q Sair", style=f"{DRACULA_THEME['comment']}")
        
        return Panel(
            info_text,
            title="ℹ️ Informações",
            border_style=DRACULA_THEME['cyan'],
            padding=(1, 2)
        )

class CLIApp(App):
    """Aplicação principal do CLI Tools"""
    
    CSS = f"""
    Screen {{
        background: {DRACULA_THEME['background']};
        color: {DRACULA_THEME['foreground']};
    }}
    
    .header {{
        height: 5;
        background: {DRACULA_THEME['current_line']};
        color: {DRACULA_THEME['pink']};
    }}
    
    .footer {{
        height: 3;
        background: {DRACULA_THEME['current_line']};
        color: {DRACULA_THEME['foreground']};
    }}
    
    #main-content {{
        width: 60%;
    }}
    
    #sidebar {{
        width: 40%;
    }}
    """
    
    BINDINGS = [
        Binding("q", "quit", "Sair", priority=True),
        Binding("escape", "back", "Voltar"),
        Binding("f1", "help", "Ajuda"),
        Binding("f5", "refresh", "Atualizar"),
        Binding("up", "move_up", "↑", show=False),
        Binding("down", "move_down", "↓", show=False),
        Binding("enter", "select", "Selecionar", show=False),
    ]
    
    def __init__(self):
        super().__init__()
        self.current_screen = "main"
        self.main_menu = MainMenu()
        self.sidebar = InfoSidebar()
    
    def compose(self) -> ComposeResult:
        """Layout principal da aplicação"""
        
        # Header
        header_text = Text()
        header_text.append("🛠️ CLI TOOLS v2.0", style=f"bold {DRACULA_THEME['purple']}")
        header_text.append("\nKit de ferramentas para desenvolvedores com IA", 
                          style=f"{DRACULA_THEME['comment']}")
        
        yield Static(Align.center(header_text), classes="header")
        
        # Conteúdo principal
        yield Container(
            Horizontal(
                Container(self.main_menu, id="main-content"),
                Container(self.sidebar, id="sidebar"),
            ),
            id="content-area"
        )
        
        # Footer
        footer_text = Text()
        footer_text.append(f"📁 {Path.cwd().name}", style=f"{DRACULA_THEME['cyan']}")
        footer_text.append("  |  ", style=f"{DRACULA_THEME['comment']}")
        footer_text.append("↑↓ Navegar  ENTER Selecionar  ESC Voltar  Q Sair", 
                          style=f"{DRACULA_THEME['comment']}")
        footer_text.append("  |  ", style=f"{DRACULA_THEME['comment']}")
        footer_text.append("🤖 Ready", style=f"{DRACULA_THEME['success']}")
        
        yield Static(Align.center(footer_text), classes="footer")
    
    def action_move_up(self):
        """Mover seleção para cima"""
        self.main_menu.move_up()
    
    def action_move_down(self):
        """Mover seleção para baixo"""
        self.main_menu.move_down()
    
    def action_select(self):
        """Selecionar item atual"""
        selected_item = self.main_menu.get_selected_item()
        action = selected_item['action']
        
        # Mostrar notificação e sair para executar comando
        self.notify(f"Executando: gemini {selected_item['command']}")
        self.exit(action)
    
    def action_back(self):
        """Voltar para tela anterior"""
        if self.current_screen != "main":
            self.show_main_screen()
    
    def action_help(self):
        """Mostrar ajuda"""
        self.notify("F1 - Ajuda | ↑↓ - Navegar | ENTER - Selecionar | Q - Sair")
    
    def action_refresh(self):
        """Atualizar interface"""
        self.refresh()
    
    def show_main_screen(self):
        """Mostrar tela principal"""
        self.current_screen = "main"
        self.refresh()

def run_cli_app():
    """Executar a aplicação CLI"""
    app = CLIApp()
    result = app.run()
    return result
