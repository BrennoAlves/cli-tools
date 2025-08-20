"""
🎨 Gemini CLI Replica - Interface idêntica ao Gemini CLI
Replica exata do layout e comportamento do Gemini CLI
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Input
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from rich.align import Align
from pathlib import Path
import os

class GeminiHeader(Static):
    """ASCII Art com gradiente - igual ao Gemini CLI"""
    
    def render(self):
        # ASCII Art "CLI TOOLS" com gradiente azul → roxo → rosa
        ascii_art = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""
        
        # Aplicar gradiente: azul → roxo → rosa
        lines = ascii_art.strip().split('\n')
        result = Text()
        
        colors = ["#8be9fd", "#bd93f9", "#ff79c6"]  # cyan → purple → pink
        
        for i, line in enumerate(lines):
            # Distribuir cores ao longo das linhas
            color_index = int(i * (len(colors) - 1) / (len(lines) - 1))
            color = colors[color_index]
            result.append(line + "\n", style=f"bold {color}")
        
        return result

class GeminiTips(Static):
    """Tips estáticas - igual ao Gemini CLI"""
    
    def render(self):
        tips = Text()
        tips.append("Tips for getting started:\n", style="#f8f8f2")
        tips.append("1. Navigate with arrows, select tools, or use commands.\n", style="#f8f8f2")
        tips.append("2. Be specific for the best results.\n", style="#f8f8f2")
        tips.append("3. /help for more information.\n", style="#f8f8f2")
        return tips

class GeminiContext(Static):
    """Context info - igual ao Gemini CLI"""
    
    def render(self):
        context = Text()
        context.append(f"Using: CLI Tools v2.0 - {Path.cwd().name}", style="#6272a4")
        return context

class GeminiCommandList(Static):
    """Lista de comandos navegável - igual ao Gemini CLI"""
    
    selected_index = reactive(0)
    
    def __init__(self):
        super().__init__()
        self.commands = [
            ("search", "Search and download images from Pexels"),
            ("figma", "Extract designs and assets from Figma"),
            ("repo", "Download GitHub repositories intelligently"),
            ("status", "Show system status and API health"),
            ("config", "Manage API keys and directories"),
            ("costs", "Monitor API usage and costs"),
            ("setup", "Initial system configuration"),
            ("help", "Show help and usage examples"),
            ("about", "Show version and system info"),
            ("clear", "Clear the screen"),
        ]
    
    def render(self):
        result = Text()
        
        for i, (cmd, desc) in enumerate(self.commands):
            is_selected = i == self.selected_index
            
            # Comando (navegável)
            if is_selected:
                result.append(f"{cmd:<12}", style="bold #bd93f9 on #44475a")
            else:
                result.append(f"{cmd:<12}", style="#8be9fd")
            
            # Descrição
            result.append(f" {desc}\n", style="#6272a4")
        
        return result
    
    def move_up(self):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.refresh()
    
    def move_down(self):
        if self.selected_index < len(self.commands) - 1:
            self.selected_index += 1
            self.refresh()
    
    def get_selected_command(self):
        return self.commands[self.selected_index][0]

class GeminiInput(Static):
    """Barra de comando com prompt - igual ao Gemini CLI"""
    
    def __init__(self):
        super().__init__()
        self.command_text = ""
    
    def render(self):
        # Prompt igual ao Gemini CLI
        prompt = Text()
        prompt.append("> ", style="#50fa7b")
        prompt.append("█", style="#f8f8f2")  # Cursor
        return prompt

class GeminiFooter(Static):
    """Footer com informações - igual ao Gemini CLI"""
    
    def render(self):
        footer = Text()
        
        # Lado esquerdo - diretório atual
        footer.append(f"~/{Path.cwd().name}", style="#8be9fd")
        footer.append(" (cli-tools)", style="#6272a4")
        
        # Centro - status
        footer.append("                    ready", style="#6272a4")
        footer.append(" (see /docs)", style="#6272a4")
        
        # Lado direito - modelo
        footer.append("                                        cli-tools-v2.0", style="#8be9fd")
        footer.append(" (100% context left)", style="#6272a4")
        
        return footer

class GeminiReplicaApp(App):
    """App que replica exatamente o Gemini CLI"""
    
    CSS = """
    Screen {
        background: #282a36;
        color: #f8f8f2;
    }
    
    #header {
        height: auto;
        margin: 1 0;
    }
    
    #tips {
        height: auto;
        margin: 1 0;
    }
    
    #context {
        height: auto;
        margin: 1 0;
    }
    
    #input-area {
        height: 3;
        border: solid #6272a4;
        margin: 1 0;
    }
    
    #commands {
        height: auto;
        margin: 1 0;
    }
    
    #footer {
        height: 1;
        dock: bottom;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", show=False),
        Binding("escape", "quit", show=False),
        Binding("up", "move_up", show=False),
        Binding("down", "move_down", show=False),
        Binding("enter", "select", show=False),
        Binding("ctrl+c", "quit", show=False),
    ]
    
    def __init__(self):
        super().__init__()
        self.header = GeminiHeader()
        self.tips = GeminiTips()
        self.context = GeminiContext()
        self.input_area = GeminiInput()
        self.commands = GeminiCommandList()
        self.footer = GeminiFooter()
    
    def compose(self) -> ComposeResult:
        """Layout exato do Gemini CLI"""
        yield Container(
            Vertical(
                # Header com ASCII art
                Container(self.header, id="header"),
                
                # Tips
                Container(self.tips, id="tips"),
                
                # Context
                Container(self.context, id="context"),
                
                # Input area
                Container(self.input_area, id="input-area"),
                
                # Commands list (navegável)
                Container(self.commands, id="commands"),
                
                # Footer
                Container(self.footer, id="footer"),
            )
        )
    
    def action_move_up(self):
        """Navegar para cima na lista de comandos"""
        self.commands.move_up()
    
    def action_move_down(self):
        """Navegar para baixo na lista de comandos"""
        self.commands.move_down()
    
    def action_select(self):
        """Selecionar comando atual"""
        command = self.commands.get_selected_command()
        self.exit(command)

def run_gemini_replica():
    """Executar replica do Gemini CLI"""
    app = GeminiReplicaApp()
    return app.run()
