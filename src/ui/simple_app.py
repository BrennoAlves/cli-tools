"""
🎨 Simple CLI Menu - Inspirado no Gemini CLI
Interface simples, leve e elegante para seleção de opções
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from rich.align import Align
from rich.console import Console
from pathlib import Path
import os

class SimpleMenu(Static):
    """Menu simples com navegação por setas - estilo Gemini CLI"""
    
    selected_index = reactive(0)
    
    def __init__(self):
        super().__init__()
        self.menu_items = [
            ("🔍", "Search Images", "search", "Buscar imagens no Pexels"),
            ("🎨", "Extract Figma", "figma", "Extrair designs do Figma"),
            ("📦", "Download Repo", "repo", "Baixar repositório GitHub"),
            ("📊", "Status", "status", "Ver status do sistema"),
            ("⚙️", "Config", "config", "Configurar APIs"),
            ("💰", "Costs", "costs", "Monitor de custos"),
            ("🚀", "Setup", "setup", "Configuração inicial"),
            ("❓", "Help", "help", "Ajuda e exemplos"),
        ]
    
    def render(self):
        """Renderizar menu simples e limpo"""
        console = Console()
        
        # Header simples
        header = Text()
        header.append("CLI Tools", style="bold #bd93f9")
        header.append(" - Developer Toolkit", style="#6272a4")
        
        # Menu items
        menu_text = Text()
        menu_text.append("\n")
        
        for i, (icon, title, cmd, desc) in enumerate(self.menu_items):
            is_selected = i == self.selected_index
            
            if is_selected:
                # Item selecionado - estilo Gemini CLI
                menu_text.append("  ▶ ", style="bold #ff79c6")
                menu_text.append(f"{icon} {title}", style="bold #f8f8f2")
                menu_text.append(f"  {desc}", style="#6272a4")
            else:
                # Item normal
                menu_text.append("    ", style="")
                menu_text.append(f"{icon} {title}", style="#f8f8f2")
                menu_text.append(f"  {desc}", style="#6272a4")
            
            menu_text.append("\n")
        
        # Footer com informações
        footer = Text()
        footer.append("\n")
        footer.append("  ↑↓ Navigate  ", style="#6272a4")
        footer.append("Enter", style="bold #bd93f9")
        footer.append(" Select  ", style="#6272a4")
        footer.append("Q", style="bold #bd93f9")
        footer.append(" Quit", style="#6272a4")
        
        # Status
        status = Text()
        status.append(f"\n  📁 {Path.cwd().name}", style="#8be9fd")
        status.append("  •  ", style="#6272a4")
        status.append("🤖 Ready", style="#50fa7b")
        
        # Combinar tudo
        result = Text()
        result.append_text(header)
        result.append_text(menu_text)
        result.append_text(footer)
        result.append_text(status)
        
        return Align.center(result)
    
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
    
    def get_selected_command(self):
        """Obter comando selecionado"""
        return self.menu_items[self.selected_index][2]

class SimpleApp(App):
    """App simples inspirado no Gemini CLI"""
    
    CSS = """
    Screen {
        background: #282a36;
        color: #f8f8f2;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("up", "move_up", "Up", show=False),
        Binding("down", "move_down", "Down", show=False),
        Binding("enter", "select", "Select", show=False),
        Binding("escape", "quit", "Quit", show=False),
    ]
    
    def __init__(self):
        super().__init__()
        self.menu = SimpleMenu()
    
    def compose(self) -> ComposeResult:
        """Layout minimalista"""
        yield Container(
            Vertical(
                self.menu,
            ),
            id="main"
        )
    
    def action_move_up(self):
        """Mover para cima"""
        self.menu.move_up()
    
    def action_move_down(self):
        """Mover para baixo"""
        self.menu.move_down()
    
    def action_select(self):
        """Selecionar opção"""
        command = self.menu.get_selected_command()
        self.exit(command)

def run_simple_menu():
    """Executar menu simples"""
    app = SimpleApp()
    return app.run()
