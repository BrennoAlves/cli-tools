"""
Menu interativo simplificado (Textual): ASCII + lista de opções.
Centralizado, com alternância de tema (T) e espaçamento superior configurável.
"""

import os
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Vertical, Center
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from rich.align import Align


# Tema Dracula mínimo e ícones inline para evitar dependências cruzadas
DRACULA = {
    'background': '#282a36',
    'foreground': '#f8f8f2',
    'comment': '#6272a4',
    'cyan': '#8be9fd',
    'purple': '#bd93f9',
    'pink': '#ff79c6',
}

ICONS = {
    'search': '🔍',
    'figma': '🎨',
    'repo': '📦',
    'status': '📊',
    'config': '⚙️',
    'costs': '💰',
    'setup': '🚀',
    'help': '❓',
}


class Header(Static):
    def render(self):
        ascii_art = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""
        lines = ascii_art.strip().split("\n")
        out = Text()
        # Espaço extra para afastar do topo
        out.append("\n\n")
        colors = [DRACULA["cyan"], DRACULA["purple"], DRACULA["pink"]]
        for i, line in enumerate(lines):
            color = colors[min(i * len(colors) // len(lines), len(colors) - 1)]
            out.append(line + "\n", style=f"bold {color}")
        out.append("\n", style=DRACULA["comment"])  # espaçamento
        return Align.center(out)


class SimpleMenu(Static):
    selected_index = reactive(0)

    def __init__(self):
        super().__init__()
        self.items = [
            {"icon": ICONS["search"], "label": "Buscar Imagens", "desc": "Pexels com filtros", "action": "search"},
            {"icon": ICONS["figma"], "label": "Extrair Figma", "desc": "Designs e assets", "action": "figma"},
            {"icon": ICONS["repo"], "label": "Baixar Repositório", "desc": "GitHub com IA", "action": "repo"},
            {"icon": ICONS["status"], "label": "Status", "desc": "APIs e workspace", "action": "status"},
            {"icon": ICONS["config"], "label": "Configurações", "desc": "APIs e diretórios", "action": "config"},
            {"icon": ICONS["costs"], "label": "Custos", "desc": "Uso das APIs", "action": "costs"},
            {"icon": ICONS["setup"], "label": "Setup", "desc": "Configuração inicial", "action": "setup"},
            {"icon": ICONS["help"], "label": "Ajuda", "desc": "Exemplos rápidos", "action": "help"},
        ]

    def render(self):
        t = Text()
        for i, item in enumerate(self.items):
            selected = i == self.selected_index
            prefix = "▶ " if selected else "  "
            color = DRACULA["purple"] if selected else DRACULA["foreground"]
            t.append(prefix, style=DRACULA["pink"] if selected else DRACULA["comment"])
            t.append(f"{item['icon']} {item['label']}", style=f"bold {color}")
            t.append(f" — {item['desc']}\n", style=DRACULA["comment"])
        t.append("\n↑↓ Navegar   Enter Selecionar   T Tema   Q/Esc Sair", style=DRACULA["comment"])
        return Align.center(t)

    def move_up(self):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.refresh()

    def move_down(self):
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self.refresh()

    def current_action(self) -> str:
        return self.items[self.selected_index]["action"]


def _read_theme_from_env_files() -> str | None:
    candidates = [Path.cwd() / '.env', Path.home() / '.local' / 'share' / 'cli-tools' / '.env']
    for env_path in candidates:
        try:
            if env_path.exists():
                for line in env_path.read_text(encoding='utf-8').splitlines():
                    if line.strip().startswith('CLI_THEME='):
                        value = line.split('=', 1)[1].strip().strip('"').strip("'")
                        if value:
                            return value
        except Exception:
            continue
    return None


def _normalize_theme(value: str | None) -> str:
    v = (value or 'transparent').lower().strip()
    return v if v in ('transparent', 'dracula') else 'transparent'


def _get_initial_theme() -> str:
    env_value = os.getenv('CLI_THEME')
    if env_value:
        return _normalize_theme(env_value)
    file_value = _read_theme_from_env_files()
    if file_value:
        return _normalize_theme(file_value)
    return 'transparent'


def _persist_theme(theme: str) -> None:
    try:
        env_file = Path.cwd() / '.env'
        lines = []
        if env_file.exists():
            lines = env_file.read_text(encoding='utf-8').splitlines()
        written = False
        for i, line in enumerate(lines):
            if line.startswith('CLI_THEME='):
                lines[i] = f'CLI_THEME={theme}'
                written = True
                break
        if not written:
            lines.append(f'CLI_THEME={theme}')
        env_file.write_text("\n".join(lines) + "\n", encoding='utf-8')
    except Exception:
        try:
            global_env = Path.home() / '.local' / 'share' / 'cli-tools' / '.env'
            global_env.parent.mkdir(parents=True, exist_ok=True)
            content = global_env.read_text(encoding='utf-8') if global_env.exists() else ''
            if 'CLI_THEME=' in content:
                new_content = []
                for line in content.splitlines():
                    new_content.append(f'CLI_THEME={theme}' if line.startswith('CLI_THEME=') else line)
                content = "\n".join(new_content)
            else:
                if content and not content.endswith('\n'):
                    content += "\n"
                content += f'CLI_THEME={theme}\n'
            global_env.write_text(content, encoding='utf-8')
        except Exception:
            pass


class MenuApp(App):
    CSS = f"""
    Screen {{
        background: transparent;
        color: {DRACULA['foreground']};
    }}
    Static {{ background: transparent; }}
    #root {{ height: 100%; width: 100%; align: center middle; }}
    .theme-dracula {{ background: {DRACULA['background']}; }}
    .theme-transparent {{ background: transparent; }}
    """

    BINDINGS = [
        Binding("up", "move_up", show=False),
        Binding("down", "move_down", show=False),
        Binding("enter", "select", show=False),
        Binding("t", "toggle_theme", show=True, description="Toggle theme"),
        Binding("q", "quit", show=False),
        Binding("escape", "quit", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.menu = SimpleMenu()
        self.top_spacer = Static()
        self._theme = _get_initial_theme()

    def compose(self) -> ComposeResult:
        root = Center(
            Vertical(
                self.top_spacer,
                Header(),
                self.menu,
            ),
            id="root",
        )
        return [root]

    def on_mount(self) -> None:
        root = self.query_one('#root')
        root.set_class(self._theme == 'dracula', 'theme-dracula')
        root.set_class(self._theme == 'transparent', 'theme-transparent')
        # Espaçamento superior (linhas)
        try:
            top_pad = int(os.getenv('CLI_UI_TOP_PAD', '6'))
        except ValueError:
            top_pad = 6
        self.top_spacer.styles.height = top_pad

    def action_move_up(self):
        self.menu.move_up()

    def action_move_down(self):
        self.menu.move_down()

    def action_select(self):
        self.exit(self.menu.current_action())

    def action_toggle_theme(self):
        self._theme = 'dracula' if self._theme == 'transparent' else 'transparent'
        root = self.query_one('#root')
        root.set_class(self._theme == 'dracula', 'theme-dracula')
        root.set_class(self._theme == 'transparent', 'theme-transparent')
        self.notify(f"Tema: {self._theme}")
        _persist_theme(self._theme)


def run_cli_app():
    return MenuApp().run()

