"""
Interface e menu interativo minimalista (Textual).
"""

from .config import (
    get_theme, set_theme, get_ui_top_pad,
    get_api_key, set_api_key, get_workspace, set_workspace,
)
from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button, Select
from textual.containers import Vertical, Center, Container
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from rich.align import Align

DRACULA = {
    'background': '#282a36',
    'foreground': '#f8f8f2',
    'comment': '#6272a4',
    'cyan': '#8be9fd',
    'purple': '#bd93f9',
    'pink': '#ff79c6',
}

ICONS = {
    'search': '🔍', 'figma': '🎨', 'repo': '📦', 'status': '📊',
    'config': '⚙️', 'costs': '💰', 'setup': '🚀', 'help': '❓'
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


class MenuApp(App):
    CSS = f"""
    Screen {{ background: transparent; color: {DRACULA['foreground']}; }}
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
        Binding("q", "back", show=True, description="Voltar"),
        Binding("escape", "back", show=False),
        Binding("ctrl+q", "quit", show=True, description="Sair"),
    ]

    def __init__(self):
        super().__init__()
        self.menu = SimpleMenu()
        self.top_spacer = Static()
        self._theme = get_theme()
        self._stack = []  # pilha de telas

    def compose(self) -> ComposeResult:
        # Container de conteúdo trocável
        content = Container(id="content")
        root = Center(Vertical(self.top_spacer, Header(), content), id="root")
        return [root]

    def on_mount(self) -> None:
        root = self.query_one('#root')
        root.set_class(self._theme == 'dracula', 'theme-dracula')
        root.set_class(self._theme == 'transparent', 'theme-transparent')
        self.top_spacer.styles.height = get_ui_top_pad()
        # Montar menu inicial no container de conteúdo
        self._content = self.query_one('#content', Container)
        self._stack = []
        self._set_content(self.menu, push=True)

    def action_move_up(self):
        self.menu.move_up()

    def action_move_down(self):
        self.menu.move_down()

    def action_select(self):
        action = self.menu.current_action()
        if action == 'search':
            self._push_screen(SearchForm())
        elif action == 'figma':
            self._push_screen(FigmaForm())
        elif action == 'repo':
            self._push_screen(RepoForm())
        elif action == 'status':
            self._push_screen(OutputScreen(['status','--simple']))
        elif action == 'help':
            self._push_screen(OutputScreen(['help']))
        elif action == 'config':
            self._push_screen(ConfigForm())
        elif action == 'costs':
            self._push_screen(OutputScreen(['costs']))
        else:
            self.exit(action)

    def action_toggle_theme(self):
        self._theme = 'dracula' if self._theme == 'transparent' else 'transparent'
        root = self.query_one('#root')
        root.set_class(self._theme == 'dracula', 'theme-dracula')
        root.set_class(self._theme == 'transparent', 'theme-transparent')
        self.notify(f"Tema: {self._theme}")
        set_theme(self._theme)

    # Navegação interna
    def _set_content(self, widget: Static, push: bool = False):
        # Remove conteúdo atual e monta o novo
        if hasattr(self, '_content') and self._content is not None:
            for child in list(self._content.children):
                child.remove()
            self._content.mount(widget)
        if push:
            self._stack.append(widget)

    def _push_screen(self, widget: Static):
        self._set_content(widget, push=True)

    def _pop_screen(self):
        if self._stack:
            self._stack.pop()
            if not self._stack:
                # Voltar para o menu
                self._set_content(self.menu, push=True)
            else:
                self._set_content(self._stack[-1], push=False)

    def action_back(self):
        self._pop_screen()


class OutputScreen(Static):
    """Executa um comando do CLI e mostra a saída dentro da UI."""
    def __init__(self, args: list[str]):
        super().__init__()
        self.args = args

    def on_mount(self):
        text = Text()
        text.append(f"$ cli-tools {' '.join(self.args)}\n\n", style=DRACULA['comment'])
        if self.args and self.args[0] == 'status':
            from src.lib.utils import get_status_text
            out = get_status_text(simple=True)
            text.append(out, style=DRACULA['foreground'])
        elif self.args and self.args[0] == 'help':
            out = (
                "Comandos:\n"
                "  search  - Buscar imagens (Pexels)\n"
                "  figma   - Extrair designs\n"
                "  repo    - Baixar repositório\n"
                "  status  - Status do sistema\n"
                "  ui      - Interface interativa\n"
            )
            text.append(out, style=DRACULA['foreground'])
        elif self.args and self.args[0] == 'costs':
            out = (
                "Custos (estimativa offline):\n"
                "  Pexels: grátis (limites por hora)\n"
                "  Figma: grátis (varia por uso)\n"
                "  Gemini: gratuito limitado (configure GEMINI_API_KEY)\n"
            )
            text.append(out, style=DRACULA['foreground'])
        else:
            from src.lib.apis import run_cli
            rc, out, err = run_cli(self.args, capture=True)
            if out:
                text.append(out, style=DRACULA['foreground'])
            if err:
                text.append("\n" + err, style=DRACULA['pink'])
        text.append("\n[Esc] Voltar", style=DRACULA['comment'])
        self.update(Align.center(text))

    def key_escape(self):
        self.app._pop_screen()


class BaseListForm(Static):
    selected_index = reactive(0)
    title = ""

    def __init__(self):
        super().__init__()
        self.items = []  # [{'label':str,'type':'text|choice|action','value':str,'choices':list}]
        self._editing = False
        self._input = Input()
        self._result: Text | None = None

    def render(self):
        t = Text()
        if self.title:
            t.append(self.title + "\n\n", style=f"bold {DRACULA['purple']}")
        for i, it in enumerate(self.items):
            sel = (i == self.selected_index)
            prefix = "▶ " if sel else "  "
            color = DRACULA['purple'] if sel else DRACULA['foreground']
            if it.get('type') == 'action':
                t.append(prefix, style=DRACULA['pink'] if sel else DRACULA['comment'])
                t.append(it['label'] + "\n", style=f"bold {color}")
            else:
                val = it.get('value', '') or ''
                t.append(prefix, style=DRACULA['pink'] if sel else DRACULA['comment'])
                t.append(f"{it['label']}: ", style=f"bold {color}")
                t.append(str(val) + "\n", style=DRACULA['comment'])
        t.append("\n↑↓ Navegar  Enter Selecionar/Editar  Q/Esc Voltar  Ctrl+Q Sair\n", style=DRACULA['comment'])
        if self._result:
            t.append("\n")
            t.append(self._result)
        return Align.center(t)

    def move_up(self):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.refresh()

    def move_down(self):
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self.refresh()

    def action_up(self):
        self.move_up()

    def action_down(self):
        self.move_down()

    def action_select(self):
        it = self.items[self.selected_index]
        if it.get('type') == 'action':
            handler = it.get('handler')
            if handler:
                handler()
        elif it.get('type') == 'choice':
            choices = it.get('choices') or []
            cur = it.get('value')
            if choices:
                try:
                    idx = [c[1] for c in choices].index(cur)
                except ValueError:
                    idx = -1
                nxt = choices[(idx + 1) % len(choices)]
                it['value'] = nxt[1]
                self.refresh()
        else:  # text
            self._editing = True
            self._input.value = str(it.get('value') or '')
            # Monta input temporário abaixo
            self.mount(Center(self._input))
            self._input.focus()

    def on_input_submitted(self, event: Input.Submitted):
        if not self._editing:
            return
        it = self.items[self.selected_index]
        it['value'] = event.value.strip()
        self._editing = False
        self._input.remove()
        self.refresh()

    def key_escape(self):
        if self._editing:
            self._editing = False
            self._input.remove()
            self.refresh()
        else:
            self.app.action_back()


class SearchForm(BaseListForm):
    def __init__(self):
        super().__init__()
        self.title = "Buscar Imagens"
        self.items = [
            {"label": "Consulta", "type": "text", "value": ""},
            {"label": "Qtd", "type": "text", "value": "1"},
            {"label": "Orientação", "type": "choice", "value": "", "choices": [("—",""),("landscape","landscape"),("portrait","portrait"),("square","square")]},
            {"label": "Output", "type": "text", "value": ""},
            {"label": "Executar", "type": "action", "handler": self._run},
            {"label": "Voltar", "type": "action", "handler": self.app.action_back},
        ]
        self._result = None

    def _run(self):
        from src.lib.apis import pexels_download_files
        q = self.items[0]['value'] or ''
        try:
            c = int(self.items[1]['value'] or '1')
        except ValueError:
            c = 1
        ori = self.items[2]['value'] or None
        out = self.items[3]['value'] or None
        t = Text()
        t.append(f"$ search '{q}' -c {c}\n\n", style=DRACULA['comment'])
        try:
            files = pexels_download_files(q, count=c, orientation=ori, output=out)
            if files:
                for f in files:
                    t.append(f"📁 {f['nome']} ({f['tamanho']})\n")
            else:
                t.append("⚠️ Nenhum arquivo gerado.")
        except Exception as e:
            t.append(f"❌ {e}", style=DRACULA['pink'])
        self._result = t
        self.refresh()


class FigmaForm(BaseListForm):
    def __init__(self):
        super().__init__()
        self.title = "Extrair Figma"
        self.items = [
            {"label": "File Key", "type": "text", "value": ""},
            {"label": "Max", "type": "text", "value": "3"},
            {"label": "Formato", "type": "choice", "value": "png", "choices": [(x,x) for x in ['png','webp','jpg','svg','pdf']]},
            {"label": "Modo", "type": "choice", "value": "all", "choices": [(x,x) for x in ['all','components','css']]},
            {"label": "Output", "type": "text", "value": ""},
            {"label": "Executar", "type": "action", "handler": self._run},
            {"label": "Voltar", "type": "action", "handler": self.app.action_back},
        ]
        self._result = None

    def _run(self):
        from src.lib.apis import figma_download_files
        key = self.items[0]['value'] or ''
        try:
            max_images = int(self.items[1]['value'] or '3')
        except ValueError:
            max_images = 3
        fmt = self.items[2]['value'] or 'png'
        mode = self.items[3]['value'] or 'all'
        out = self.items[4]['value'] or None
        t = Text()
        t.append(f"$ figma {key} -n {max_images} -f {fmt} --mode {mode}\n\n", style=DRACULA['comment'])
        try:
            files = figma_download_files(key, fmt=fmt, scale=1.0, output=out, nodes=None, max_images=max_images, mode=mode)
            if files:
                for f in files:
                    t.append(f"📁 {f['nome']} ({f['tamanho']})\n")
            else:
                t.append("⚠️ Nenhum arquivo gerado.")
        except Exception as e:
            t.append(f"❌ {e}", style=DRACULA['pink'])
        self._result = t
        self.refresh()


class RepoForm(BaseListForm):
    def __init__(self):
        super().__init__()
        self.title = "Baixar Repositório"
        self.items = [
            {"label": "Repositório", "type": "text", "value": ""},
            {"label": "Query (IA)", "type": "text", "value": ""},
            {"label": "Sem IA", "type": "choice", "value": "", "choices": [("não",""),("sim","1")]},
            {"label": "Clone Completo", "type": "choice", "value": "", "choices": [("não",""),("sim","1")]},
            {"label": "Output", "type": "text", "value": ""},
            {"label": "Executar", "type": "action", "handler": self._run},
            {"label": "Voltar", "type": "action", "handler": self.app.action_back},
        ]
        self._result = None

    def _run(self):
        from src.lib.apis import repo_download_auto
        repo = self.items[0]['value'] or ''
        query = self.items[1]['value'] or None
        no_ai = (self.items[2]['value'] == '1')
        all_clone = (self.items[3]['value'] == '1')
        out = self.items[4]['value'] or None
        t = Text()
        t.append(f"$ repo {repo} {query or ''} {'--no-ai' if no_ai else ''} {'--all' if all_clone else ''}\n\n", style=DRACULA['comment'])
        try:
            path = repo_download_auto(repo, query=query, output=out, no_ai=no_ai, all_clone=all_clone)
            t.append(f"📦 Repositório salvo em: {path}")
        except Exception as e:
            t.append(f"❌ {e}", style=DRACULA['pink'])
        self._result = t
        self.refresh()


class ConfigForm(BaseListForm):
    def __init__(self):
        super().__init__()
        self.title = "Configurações"
        self.items = [
            {"label": "Workspace", "type": "text", "value": get_workspace()},
            {"label": "PEXELS_API_KEY", "type": "text", "value": get_api_key('pexels') or ''},
            {"label": "FIGMA_API_TOKEN", "type": "text", "value": get_api_key('figma') or ''},
            {"label": "GEMINI_API_KEY", "type": "text", "value": get_api_key('gemini') or ''},
            {"label": "Tema", "type": "choice", "value": get_theme(), "choices": [("transparent","transparent"),("dracula","dracula")]},
            {"label": "Salvar", "type": "action", "handler": self._save},
            {"label": "Voltar", "type": "action", "handler": self.app.action_back},
        ]
        self._result = None

    def _save(self):
        ws = self.items[0]['value'] or ''
        pex = self.items[1]['value'] or ''
        fig = self.items[2]['value'] or ''
        gem = self.items[3]['value'] or ''
        thm = self.items[4]['value'] or 'transparent'
        try:
            if ws:
                set_workspace(ws)
            if pex:
                set_api_key('pexels', pex)
            if fig:
                set_api_key('figma', fig)
            if gem:
                set_api_key('gemini', gem)
            set_theme(thm)
            self.app.notify('Configurações salvas')
        except Exception as e:
            self.app.notify(f'Erro: {e}')


def interactive_menu():
    return MenuApp().run()
