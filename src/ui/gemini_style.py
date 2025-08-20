"""
🎨 Gemini-Style Menu - Interface minimalista
Inspirado no design limpo e elegante do Gemini CLI
"""

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from rich.align import Align
from pathlib import Path

class GeminiMenu(Static):
    """Menu minimalista estilo Gemini CLI"""
    
    selected_index = reactive(0)
    
    def __init__(self):
        super().__init__()
        self.items = [
            ("Search Images", "search", "🔍 Buscar imagens no Pexels"),
            ("Extract Figma", "figma", "🎨 Extrair designs do Figma"),
            ("Download Repo", "repo", "📦 Baixar repositório GitHub"),
            ("Status", "status", "📊 Ver status do sistema"),
            ("Config", "config", "⚙️ Configurar APIs"),
            ("Costs", "costs", "💰 Monitor de custos"),
            ("Setup", "setup", "🚀 Configuração inicial"),
            ("Help", "help", "❓ Ajuda e exemplos"),
        ]
    
    def render(self):
        """Renderizar menu ultra-limpo"""
        text = Text()
        
        # Header minimalista
        text.append("CLI Tools", style="bold #bd93f9")
        text.append("\n\n")
        
        # Menu items - estilo Gemini CLI
        for i, (title, cmd, desc) in enumerate(self.items):
            is_selected = i == self.selected_index
            
            if is_selected:
                text.append("▶ ", style="bold #ff79c6")
                text.append(title, style="bold #f8f8f2")
            else:
                text.append("  ", style="")
                text.append(title, style="#f8f8f2")
            
            text.append("\n")
        
        # Footer minimalista
        text.append("\n")
        text.append("↑↓ navigate  ", style="#6272a4")
        text.append("enter", style="#bd93f9")
        text.append(" select  ", style="#6272a4")
        text.append("q", style="#bd93f9")
        text.append(" quit", style="#6272a4")
        
        # Status line
        text.append(f"\n\n📁 {Path.cwd().name}", style="#8be9fd")
        text.append("  🤖 ready", style="#50fa7b")
        
        return text
    
    def move_up(self):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.refresh()
    
    def move_down(self):
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self.refresh()
    
    def get_selected(self):
        return self.items[self.selected_index][1]

class GeminiApp(App):
    """App ultra-minimalista"""
    
    CSS = """
    Screen {
        background: #282a36;
        color: #f8f8f2;
        align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", show=False),
        Binding("escape", "quit", show=False),
        Binding("up", "up", show=False),
        Binding("down", "down", show=False),
        Binding("enter", "select", show=False),
    ]
    
    def __init__(self):
        super().__init__()
        self.menu = GeminiMenu()
    
    def compose(self) -> ComposeResult:
        yield self.menu
    
    def action_up(self):
        self.menu.move_up()
    
    def action_down(self):
        self.menu.move_down()
    
    def action_select(self):
        self.exit(self.menu.get_selected())

def run_gemini_menu():
    """Executar menu estilo Gemini"""
    app = GeminiApp()
    return app.run()
