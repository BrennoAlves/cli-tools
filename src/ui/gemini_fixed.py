"""
🎨 Gemini CLI Fixed - Interface corrigida
Fundo limpo, português, navegação funcionando, menus organizados
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from pathlib import Path

class CliToolsHeader(Static):
    """ASCII Art CLI TOOLS com gradiente"""
    
    def render(self):
        ascii_art = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""
        
        lines = ascii_art.strip().split('\n')
        result = Text()
        
        # Gradiente: cyan → purple → pink
        colors = ["#8be9fd", "#bd93f9", "#ff79c6"]
        
        for i, line in enumerate(lines):
            color_index = min(i * len(colors) // len(lines), len(colors) - 1)
            color = colors[color_index]
            result.append(line + "\n", style=f"bold {color}")
        
        return result

class CliToolsTips(Static):
    """Dicas em português"""
    
    def render(self):
        tips = Text()
        tips.append("Navegação:\n", style="#f8f8f2")
        tips.append("↑↓ Navegar  •  Enter Selecionar  •  q Sair\n", style="#50fa7b")
        tips.append("\n", style="#f8f8f2")
        return tips

class CliToolsContext(Static):
    """Contexto atual"""
    
    def render(self):
        context = Text()
        context.append(f"Usando: CLI Tools v2.0 - {Path.cwd().name}", style="#6272a4")
        return context

class CliToolsPrompt(Static):
    """Prompt de comando"""
    
    def render(self):
        prompt = Text()
        prompt.append("> ", style="#50fa7b")
        prompt.append("█", style="#f8f8f2")
        return prompt

class CliToolsCommands(Static):
    """Lista de comandos principais navegável"""
    
    selected_index = reactive(0)
    
    def __init__(self):
        super().__init__()
        # Apenas comandos PRINCIPAIS, não submenus
        self.commands = [
            ("buscar", "Buscar e baixar imagens do Pexels"),
            ("figma", "Extrair designs e assets do Figma"),
            ("repo", "Baixar repositórios GitHub com IA"),
            ("status", "Ver status das APIs e sistema"),
            ("config", "Configurar chaves de API"),
            ("custos", "Monitorar uso e custos das APIs"),
            ("setup", "Configuração inicial do sistema"),
            ("ajuda", "Mostrar ajuda e exemplos"),
        ]
    
    def render(self):
        result = Text()
        
        for i, (cmd, desc) in enumerate(self.commands):
            is_selected = i == self.selected_index
            
            # Comando navegável
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
    
    def move_down(self):
        if self.selected_index < len(self.commands) - 1:
            self.selected_index += 1
    
    def get_selected_command(self):
        return self.commands[self.selected_index][0]

class CliToolsFooter(Static):
    """Footer com informações do sistema"""
    
    def render(self):
        footer = Text()
        
        # Esquerda - diretório
        footer.append(f"~/{Path.cwd().name}", style="#8be9fd")
        footer.append(" (cli-tools)", style="#6272a4")
        
        # Centro - status
        footer.append("                    pronto", style="#50fa7b")
        
        # Direita - versão
        footer.append("                                        cli-tools-v2.0", style="#8be9fd")
        footer.append(" (100% contexto)", style="#6272a4")
        
        return footer

class CliToolsApp(App):
    """App principal - replica do Gemini CLI"""
    
    # Usar tela alternativa para não sobrepor o terminal
    ENABLE_COMMAND_PALETTE = False
    
    CSS = """
    Screen {
        background: #282a36;
        color: #f8f8f2;
    }
    
    Container {
        background: transparent;
    }
    
    Static {
        background: transparent;
    }
    
    #prompt-container {
        border: solid #6272a4;
        height: 3;
        margin: 1 0;
        background: transparent;
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
        self.commands = CliToolsCommands()
    
    def compose(self) -> ComposeResult:
        """Layout igual ao Gemini CLI"""
        yield Vertical(
            # Header ASCII
            CliToolsHeader(),
            
            # Tips
            CliToolsTips(),
            
            # Context
            CliToolsContext(),
            
            # Commands (navegável) - SEM prompt area
            self.commands,
            
            # Footer
            CliToolsFooter(),
        )
    
    def action_move_up(self):
        """Navegar para cima"""
        self.commands.move_up()
        self.commands.refresh()
    
    def action_move_down(self):
        """Navegar para baixo"""
        self.commands.move_down()
        self.commands.refresh()
    
    def action_select(self):
        """Selecionar comando"""
        command = self.commands.get_selected_command()
        
        # Mapear comandos em português para inglês
        command_map = {
            "buscar": "search",
            "figma": "figma", 
            "repo": "repo",
            "status": "status",
            "config": "config",
            "custos": "costs",
            "setup": "setup",
            "ajuda": "help"
        }
        
        english_command = command_map.get(command, command)
        self.exit(english_command)

def run_cli_tools_interface():
    """Executar interface CLI Tools"""
    app = CliToolsApp()
    return app.run()
