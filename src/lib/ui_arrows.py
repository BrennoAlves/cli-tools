"""
Interface navegável por setas como Gemini CLI.
"""

from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label
from textual.containers import Vertical, Container
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
from rich.align import Align
import asyncio

# Tema Dracula
DRACULA = {
    'background': '#282a36',
    'foreground': '#f8f8f2', 
    'cyan': '#8be9fd',
    'purple': '#bd93f9',
    'pink': '#ff79c6',
    'green': '#50fa7b',
    'red': '#ff5555',
    'orange': '#ffb86c'
}

class HeaderWidget(Static):
    def render(self):
        ascii_art = """
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"""
        
        text = Text()
        text.append("\n")
        for i, line in enumerate(ascii_art.strip().split("\n")):
            color = [DRACULA["cyan"], DRACULA["purple"], DRACULA["pink"]][i % 3]
            text.append(line + "\n", style=f"bold {color}")
        text.append("\nKit de ferramentas para desenvolvedores v2.0\n", 
                   style=DRACULA["cyan"])
        return Align.center(text)

class MenuListItem(ListItem):
    def __init__(self, label: str, description: str, action: str):
        super().__init__()
        self.label = label
        self.description = description
        self.action = action
        
    def compose(self) -> ComposeResult:
        yield Label(f"{self.label:<15} {self.description}")

class MainMenuScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑ Cima"),
        Binding("down,j", "cursor_down", "↓ Baixo"),
        Binding("enter", "select", "Enter"),
        Binding("q,escape", "quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        yield HeaderWidget()
        yield Container(
            ListView(
                MenuListItem("search", "Buscar e baixar imagens do Pexels", "search"),
                MenuListItem("figma", "Extrair designs do Figma", "figma"),
                MenuListItem("repo", "Baixar repositório com IA", "repo"),
                MenuListItem("status", "Exibir status do sistema", "status"),
                MenuListItem("config", "Configurar APIs e workspace", "config"),
                MenuListItem("quit", "Sair do programa", "quit"),
                id="menu_list"
            ),
            classes="menu-container"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "search":
                self.app.push_screen(SearchMenuScreen())
            elif item.action == "figma":
                self.app.push_screen(FigmaMenuScreen())
            elif item.action == "repo":
                self.app.push_screen(RepoMenuScreen())
            elif item.action == "status":
                self.app.push_screen(StatusScreen())
            elif item.action == "config":
                self.app.push_screen(ConfigMenuScreen())
            elif item.action == "quit":
                self.app.exit()

class SearchMenuScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑ Cima"),
        Binding("down,j", "cursor_down", "↓ Baixo"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "back", "← Voltar"),
    ]

    def __init__(self):
        super().__init__()
        self.query = ""
        self.count = 1
        self.orientation = ""
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Label("🔍 Buscar Imagens", classes="screen-title")
        yield Container(
            ListView(
                MenuListItem("query", f"Consulta: {self.query or '(vazio)'}", "query"),
                MenuListItem("count", f"Quantidade: {self.count}", "count"),
                MenuListItem("orientation", f"Orientação: {self.orientation or 'qualquer'}", "orientation"),
                MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
                MenuListItem("execute", "🚀 Executar busca", "execute"),
                MenuListItem("back", "← Voltar", "back"),
                id="search_list"
            ),
            Static(id="result"),
            classes="form-container"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "query":
                self.app.push_screen(InputScreen("Digite a consulta:", self.query, self.set_query))
            elif item.action == "count":
                self.app.push_screen(InputScreen("Digite a quantidade:", str(self.count), self.set_count))
            elif item.action == "orientation":
                self.app.push_screen(SelectScreen("Orientação:", 
                    [("Qualquer", ""), ("Paisagem", "landscape"), ("Retrato", "portrait"), ("Quadrado", "square")],
                    self.orientation, self.set_orientation))
            elif item.action == "output":
                self.app.push_screen(InputScreen("Digite o diretório:", self.output, self.set_output))
            elif item.action == "execute":
                self.execute_search()
            elif item.action == "back":
                self.app.pop_screen()

    def set_query(self, value: str):
        self.query = value
        self.refresh_list()

    def set_count(self, value: str):
        try:
            self.count = int(value) if value else 1
        except ValueError:
            self.count = 1
        self.refresh_list()

    def set_orientation(self, value: str):
        self.orientation = value
        self.refresh_list()

    def set_output(self, value: str):
        self.output = value
        self.refresh_list()

    def refresh_list(self):
        list_view = self.query_one("#search_list", ListView)
        list_view.clear()
        list_view.extend([
            MenuListItem("query", f"Consulta: {self.query or '(vazio)'}", "query"),
            MenuListItem("count", f"Quantidade: {self.count}", "count"),
            MenuListItem("orientation", f"Orientação: {self.orientation or 'qualquer'}", "orientation"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar busca", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    async def execute_search(self):
        if not self.query.strip():
            self.query_one("#result", Static).update("❌ Digite uma consulta de busca")
            return
        
        result_widget = self.query_one("#result", Static)
        result_widget.update("🔄 Buscando imagens...")
        
        try:
            from src.lib.apis import pexels_download_files
            files = await asyncio.to_thread(
                pexels_download_files, 
                self.query, 
                count=self.count, 
                orientation=self.orientation or None,
                output=self.output or None
            )
            
            if files:
                text = f"✅ {len(files)} imagem(s) baixada(s):\n"
                for f in files:
                    text += f"📁 {f['nome']} ({f['tamanho']})\n"
                result_widget.update(text)
            else:
                result_widget.update("⚠️ Nenhuma imagem encontrada")
                
        except Exception as e:
            result_widget.update(f"❌ Erro: {str(e)}")

    def action_back(self):
        self.app.pop_screen()
