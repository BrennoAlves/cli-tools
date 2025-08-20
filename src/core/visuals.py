"""
Módulo central para elementos visuais da CLI.

Define o tema de cores (Dracula), estilos e componentes reutilizáveis
para garantir uma identidade visual consistente em toda a aplicação.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

# Paleta de cores Dracula
DRACULA_THEME = {
    "background": "#282a36",
    "current_line": "#44475a",
    "foreground": "#f8f8f2",
    "comment": "#6272a4",
    "cyan": "#8be9fd",
    "green": "#50fa7b",
    "orange": "#ffb86c",
    "pink": "#ff79c6",
    "purple": "#bd93f9",
    "red": "#ff5555",
    "yellow": "#f1fa8c",
}

# Tema Rich para consistência
cli_theme = Theme({
    "primary": f"bold {DRACULA_THEME['purple']}",
    "secondary": f"bold {DRACULA_THEME['cyan']}",
    "success": f"bold {DRACULA_THEME['green']}",
    "warning": f"bold {DRACULA_THEME['orange']}",
    "error": f"bold {DRACULA_THEME['red']}",
    "info": DRACULA_THEME['comment'],
    "text": DRACULA_THEME['foreground'],
    
    # Estilos de componentes
    "panel.border": DRACULA_THEME['purple'],
    "panel.title": f"bold {DRACULA_THEME['pink']}",
    "table.header": f"bold {DRACULA_THEME['pink']}",
    "table.cell": DRACULA_THEME['foreground'],
    "progress.bar": DRACULA_THEME['green'],
    "progress.percentage": f"bold {DRACULA_THEME['foreground']}",
})

# Console global com o tema aplicado
console = Console(theme=cli_theme)

def styled_panel(content, title, subtitle=""):
    """Cria um painel estilizado com título e subtítulo."""
    
    title_text = Text(title, style="panel.title", justify="left")
    subtitle_text = Text(subtitle, style="info", justify="left")
    
    header = Text.assemble(title_text, "\n", subtitle_text)
    
    return Panel(
        content,
        title=header,
        border_style="panel.border",
        expand=True,
        padding=(1, 2)
    )

def print_header(title: str, subtitle: str = ""):
    """Imprime um cabeçalho estilizado para seções da CLI."""
    header_text = Text.assemble(
        (f"🚀 {title}", "primary"),
        ("\n" + subtitle, "secondary") if subtitle else ""
    )
    console.print(Panel(
        header_text,
        border_style="primary",
        padding=(1, 2),
        expand=False
    ))

def print_success(message: str):
    """Imprime uma mensagem de sucesso."""
    console.print(f"[success]✅ {message}[/success]")

def print_error(message: str):
    """Imprime uma mensagem de erro."""
    console.print(f"[error]❌ {message}[/error]")

def print_warning(message: str):
    """Imprime uma mensagem de aviso."""
    console.print(f"[warning]⚠️ {message}[/warning]")

def print_info(message: str):
    """Imprime uma mensagem informativa."""
    console.print(f"[info]💡 {message}[/info]")
