"""
Menu interativo principal, construído com Textual para uma experiência de TUI moderna.
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Container, Horizontal, Vertical
from textual.binding import Binding

from ..core.visuals import DRACULA_THEME

# CSS para o menu, inspirado no tema Dracula
MENU_CSS = f"""
Screen {{
    background: {DRACULA_THEME['background']};
    color: {DRACULA_THEME['foreground']};
}}

Header {{
    background: {DRACULA_THEME['current_line']};
    color: {DRACULA_THEME['pink']};
}}

Footer {{
    background: {DRACULA_THEME['current_line']};
}}

#menu-container {{
    padding: 1;
    width: 100%;
    height: 100%;
    align: center middle;
}}

#menu-options {{
    width: 40%;
    border: solid {DRACULA_THEME['purple']};
}}

#menu-details {{
    width: 60%;
    padding: 0 2;
}}

Label {{
    padding: 1;
}}

.menu-item {{
    content-align: left middle;
    width: 100%;
}}

.menu-item--highlight {{
    background: {DRACULA_THEME['current_line']};
}}

#details-title {{
    color: {DRACULA_THEME['pink']};
}}

#details-description {{
    color: {DRACULA_THEME['foreground']};
}}

#details-keys {{
    padding-top: 2;
    color: {DRACULA_THEME['comment']};
}}
"""

class InteractiveMenuApp(App):
    """App Textual para o menu interativo da CLI."""

    CSS = MENU_CSS
    
    BINDINGS = [
        Binding("q", "quit", "Sair"),
        Binding("up", "cursor_up", "Mover para cima", show=False),
        Binding("down", "cursor_down", "Mover para baixo", show=False),
        Binding("enter", "select_option", "Selecionar", show=False),
    ]

    def __init__(self, menu_options):
        super().__init__()
        self.menu_options = menu_options
        self.selected_index = 0

    def compose(self) -> ComposeResult:
        yield Header(name="🚀 Gemini CLI - Menu Interativo")
        with Container(id="menu-container"):
            with Horizontal():
                with Vertical(id="menu-options"):
                    for i, option in enumerate(self.menu_options):
                        yield Label(f"{option['icon']} {option['title']}", id=f"option-{i}", classes="menu-item")
                with Vertical(id="menu-details"):
                    yield Label("", id="details-title")
                    yield Static("", id="details-description")
                    yield Label("", id="details-keys")
        yield Footer()

    def on_mount(self) -> None:
        self._update_highlight()
        self._update_details()

    def _update_highlight(self):
        for i, _ in enumerate(self.menu_options):
            widget = self.query_one(f"#option-{i}", Label)
            widget.remove_class("menu-item--highlight")
        
        highlighted_widget = self.query_one(f"#option-{self.selected_index}", Label)
        highlighted_widget.add_class("menu-item--highlight")

    def _update_details(self):
        option = self.menu_options[self.selected_index]
        self.query_one("#details-title", Label).update(f"{option['icon']} {option['title']}")
        self.query_one("#details-description", Static).update(option['description'])
        self.query_one("#details-keys", Label).update(f"Pressione [bold]Enter[/bold] para {option['action']}.")

    def action_cursor_up(self) -> None:
        self.selected_index = (self.selected_index - 1) % len(self.menu_options)
        self._update_highlight()
        self._update_details()

    def action_cursor_down(self) -> None:
        self.selected_index = (self.selected_index + 1) % len(self.menu_options)
        self._update_highlight()
        self._update_details()

    def action_select_option(self) -> None:
        # Aqui você executaria a ação real
        # Por enquanto, vamos apenas sair e "retornar" a opção
        self.exit(self.menu_options[self.selected_index]['id'])


def show_interactive_menu(menu_options):
    """Exibe o menu interativo e retorna o ID da opção selecionada."""
    app = InteractiveMenuApp(menu_options)
    selected_option_id = app.run()
    return selected_option_id