"""
ASCII Art responsivo para CLI Tools
Inspirado no gemini-cli com diferentes tamanhos
"""

# ASCII Art Grande (terminal >= 75 colunas)
LARGE_ASCII = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""

# ASCII Art Médio (terminal >= 50 colunas)
MEDIUM_ASCII = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""

# ASCII Art Pequeno (terminal >= 35 colunas)
SMALL_ASCII = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""

# ASCII Art Compacto (terminal >= 25 colunas)
COMPACT_ASCII = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""

# ASCII Art Mínimo (terminal >= 15 colunas)
TINY_ASCII = """
╔═══════════╗
║ CLI-TOOLS ║
╚═══════════╝"""

# Texto simples para terminais muito pequenos
TEXT_ONLY = "CLI-TOOLS"

def get_ascii_width(ascii_art: str) -> int:
    """Calcular largura do ASCII art"""
    lines = ascii_art.strip().split('\n')
    return max(len(line) for line in lines) if lines else 0

def get_responsive_ascii(terminal_width: int) -> str:
    """Retornar ASCII art baseado na largura do terminal"""
    
    # Verificar cada tamanho em ordem decrescente
    ascii_options = [
        (75, LARGE_ASCII),
        (50, MEDIUM_ASCII), 
        (35, SMALL_ASCII),
        (25, COMPACT_ASCII),
        (15, TINY_ASCII),
        (0, TEXT_ONLY)
    ]
    
    for min_width, ascii_art in ascii_options:
        if terminal_width >= min_width:
            actual_width = get_ascii_width(ascii_art)
            # Verificar se realmente cabe com margem
            if actual_width <= (terminal_width - 2):
                return ascii_art
    
    return TEXT_ONLY

def get_header_with_subtitle(terminal_width: int, version: str = "2.0") -> str:
    """Gerar header completo com subtítulo"""
    ascii_art = get_responsive_ascii(terminal_width)
    
    # Subtítulos baseados no tamanho
    if terminal_width >= 70:
        subtitle = f"v{version} - Kit de ferramentas para desenvolvedores"
    elif terminal_width >= 50:
        subtitle = f"v{version} - Ferramentas para desenvolvedores"
    elif terminal_width >= 35:
        subtitle = f"v{version} - Ferramentas para devs"
    elif terminal_width >= 25:
        subtitle = f"v{version} - Dev Tools"
    else:
        subtitle = f"v{version}"
    
    # Centralizar subtítulo baseado na largura do ASCII
    ascii_width = get_ascii_width(ascii_art)
    if ascii_width > len(subtitle):
        padding = (ascii_width - len(subtitle)) // 2
        subtitle = " " * padding + subtitle
    
    return f"{ascii_art}\n\n{subtitle}"

# Cores para gradiente (tema Dracula)
GRADIENT_COLORS = ["#bd93f9", "#8be9fd"]  # Purple to Cyan
