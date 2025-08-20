"""
🎨 Dracula Theme - Modern CLI Colors
Baseado no padrão ouro do Gemini CLI
"""

# Dracula Theme - Cores principais
DRACULA_THEME = {
    # Cores base
    'background': '#282a36',
    'current_line': '#44475a',
    'foreground': '#f8f8f2',
    'comment': '#6272a4',
    'selection': '#44475a',
    
    # Cores de destaque
    'cyan': '#8be9fd',
    'green': '#50fa7b',
    'orange': '#ffb86c',
    'pink': '#ff79c6',
    'purple': '#bd93f9',
    'red': '#ff5555',
    'yellow': '#f1fa8c',
    
    # Cores semânticas para UI
    'primary': '#bd93f9',      # Roxo principal
    'secondary': '#6272a4',    # Cinza secundário
    'accent': '#ff79c6',       # Rosa de destaque
    'success': '#50fa7b',      # Verde sucesso
    'warning': '#f1fa8c',      # Amarelo aviso
    'error': '#ff5555',        # Vermelho erro
    'info': '#8be9fd',         # Ciano informação
    
    # Gradientes para header
    'gradient': ['#ff79c6', '#bd93f9', '#8be9fd'],
    
    # Bordas e separadores
    'border': '#6272a4',
    'border_focused': '#bd93f9',
    'separator': '#44475a',
}

# Estilos CSS para Textual
DRACULA_CSS = f"""
/* Tema Dracula Global */
Screen {{
    background: {DRACULA_THEME['background']};
    color: {DRACULA_THEME['foreground']};
}}

/* Header */
.header {{
    background: {DRACULA_THEME['current_line']};
    color: {DRACULA_THEME['pink']};
    text-style: bold;
    height: 5;
}}

.header-title {{
    color: {DRACULA_THEME['purple']};
    text-style: bold;
}}

.header-subtitle {{
    color: {DRACULA_THEME['comment']};
}}

/* Footer */
.footer {{
    background: {DRACULA_THEME['current_line']};
    color: {DRACULA_THEME['foreground']};
    height: 3;
}}

.footer-info {{
    color: {DRACULA_THEME['cyan']};
}}

.footer-shortcuts {{
    color: {DRACULA_THEME['comment']};
}}

/* Menu Principal */
.menu-container {{
    padding: 1;
    border: solid {DRACULA_THEME['purple']};
    background: {DRACULA_THEME['background']};
}}

.menu-item {{
    padding: 1 2;
    margin: 0 1;
    color: {DRACULA_THEME['foreground']};
    background: {DRACULA_THEME['background']};
}}

.menu-item:hover {{
    background: {DRACULA_THEME['current_line']};
    color: {DRACULA_THEME['cyan']};
}}

.menu-item-selected {{
    background: {DRACULA_THEME['purple']};
    color: {DRACULA_THEME['background']};
    text-style: bold;
}}

.menu-item-icon {{
    color: {DRACULA_THEME['pink']};
}}

.menu-item-description {{
    color: {DRACULA_THEME['comment']};
}}

/* Painéis de informação */
.info-panel {{
    border: solid {DRACULA_THEME['cyan']};
    background: {DRACULA_THEME['background']};
    padding: 1;
}}

.status-panel {{
    border: solid {DRACULA_THEME['green']};
    background: {DRACULA_THEME['background']};
    padding: 1;
}}

.warning-panel {{
    border: solid {DRACULA_THEME['warning']};
    background: {DRACULA_THEME['background']};
    padding: 1;
}}

.error-panel {{
    border: solid {DRACULA_THEME['error']};
    background: {DRACULA_THEME['background']};
    padding: 1;
}}

/* Botões e controles */
.button {{
    background: {DRACULA_THEME['purple']};
    color: {DRACULA_THEME['background']};
    text-style: bold;
    padding: 0 2;
}}

.button:hover {{
    background: {DRACULA_THEME['pink']};
}}

.button-secondary {{
    background: {DRACULA_THEME['comment']};
    color: {DRACULA_THEME['foreground']};
}}

/* Input e formulários */
.input {{
    background: {DRACULA_THEME['current_line']};
    color: {DRACULA_THEME['foreground']};
    border: solid {DRACULA_THEME['comment']};
}}

.input:focus {{
    border: solid {DRACULA_THEME['purple']};
}}

/* Tabelas e listas */
.table-header {{
    background: {DRACULA_THEME['purple']};
    color: {DRACULA_THEME['background']};
    text-style: bold;
}}

.table-row {{
    color: {DRACULA_THEME['foreground']};
}}

.table-row:hover {{
    background: {DRACULA_THEME['current_line']};
}}

/* Indicadores de status */
.status-success {{
    color: {DRACULA_THEME['success']};
}}

.status-warning {{
    color: {DRACULA_THEME['warning']};
}}

.status-error {{
    color: {DRACULA_THEME['error']};
}}

.status-info {{
    color: {DRACULA_THEME['info']};
}}

/* Barras de progresso */
.progress-bar {{
    background: {DRACULA_THEME['current_line']};
}}

.progress-bar-fill {{
    background: {DRACULA_THEME['purple']};
}}

/* Scrollbars */
.scrollbar {{
    background: {DRACULA_THEME['current_line']};
}}

.scrollbar-thumb {{
    background: {DRACULA_THEME['purple']};
}}

/* Tooltips e ajuda */
.tooltip {{
    background: {DRACULA_THEME['current_line']};
    color: {DRACULA_THEME['foreground']};
    border: solid {DRACULA_THEME['comment']};
}}

.help-text {{
    color: {DRACULA_THEME['comment']};
    text-style: italic;
}}
"""

# Ícones e símbolos usando Unicode
ICONS = {
    'search': '🔍',
    'figma': '🎨', 
    'repo': '📦',
    'status': '📊',
    'config': '⚙️',
    'help': '❓',
    'tools': '🛠️',
    'ai': '🤖',
    'costs': '💰',
    'setup': '🚀',
    'arrow_right': '▶',
    'arrow_left': '◀',
    'arrow_up': '▲',
    'arrow_down': '▼',
    'check': '✅',
    'cross': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'star': '⭐',
    'heart': '💖',
    'fire': '🔥',
    'rocket': '🚀',
    'gem': '💎',
    'magic': '✨',
}

# Atalhos de teclado
SHORTCUTS = {
    'quit': 'Q',
    'help': 'F1', 
    'back': 'ESC',
    'select': 'ENTER',
    'up': '↑',
    'down': '↓',
    'left': '←',
    'right': '→',
    'refresh': 'F5',
    'search': 'F3',
    'config': 'F2',
}

def get_gradient_text(text: str) -> str:
    """Cria texto com gradiente usando Rich markup"""
    colors = DRACULA_THEME['gradient']
    if len(text) <= 1:
        return f"[{colors[0]}]{text}[/]"
    
    # Distribui as cores ao longo do texto
    result = ""
    for i, char in enumerate(text):
        color_index = int(i * (len(colors) - 1) / (len(text) - 1))
        color = colors[color_index]
        result += f"[{color}]{char}[/]"
    
    return result

def format_shortcut(key: str, description: str) -> str:
    """Formata atalho de teclado com cores"""
    return f"[{DRACULA_THEME['purple']}]{key}[/] {description}"

def format_status(status: str, is_success: bool = True) -> str:
    """Formata status com cores apropriadas"""
    color = DRACULA_THEME['success'] if is_success else DRACULA_THEME['error']
    icon = ICONS['check'] if is_success else ICONS['cross']
    return f"[{color}]{icon} {status}[/]"
