"""
Interface navegável por setas como Gemini CLI - versão unificada.
"""

from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Input
from textual.containers import Vertical, Container
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
from rich.align import Align
import asyncio

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
        Binding("up,k", "cursor_up", "↑"),
        Binding("down,j", "cursor_down", "↓"),
        Binding("enter", "select", "Enter"),
        Binding("q,escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("CLI TOOLS v2.0", classes="header")
        yield ListView(
            MenuListItem("search", "Buscar e baixar imagens do Pexels", "search"),
            MenuListItem("figma", "Extrair designs do Figma", "figma"),
            MenuListItem("repo", "Baixar repositório com IA", "repo"),
            MenuListItem("status", "Exibir status do sistema", "status"),
            MenuListItem("config", "Configurar APIs e workspace", "config"),
            MenuListItem("quit", "Sair do programa", "quit"),
            id="main_menu"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "search":
                self.app.push_screen(SearchScreen())
            elif item.action == "figma":
                self.app.push_screen(FigmaScreen())
            elif item.action == "repo":
                self.app.push_screen(RepoScreen())
            elif item.action == "status":
                self.app.push_screen(StatusScreen())
            elif item.action == "config":
                self.app.push_screen(ConfigScreen())
            elif item.action == "quit":
                self.app.exit()

class SearchScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑"),
        Binding("down,j", "cursor_down", "↓"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "back", "Back"),
    ]

    def __init__(self):
        super().__init__()
        self.query = ""
        self.count = 1
        self.orientation = ""
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Static("🔍 BUSCAR IMAGENS", classes="header")
        yield ListView(
            MenuListItem("query", f"Consulta: {self.query or '(vazio)'}", "query"),
            MenuListItem("count", f"Quantidade: {self.count}", "count"),
            MenuListItem("orientation", f"Orientação: {self.orientation or 'qualquer'}", "orientation"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar busca", "execute"),
            MenuListItem("back", "← Voltar", "back"),
            id="search_menu"
        )
        yield Static("", id="result")

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
        self.refresh_menu()

    def set_count(self, value: str):
        try:
            self.count = int(value) if value else 1
        except ValueError:
            self.count = 1
        self.refresh_menu()

    def set_orientation(self, value: str):
        self.orientation = value
        self.refresh_menu()

    def set_output(self, value: str):
        self.output = value
        self.refresh_menu()

    def refresh_menu(self):
        menu = self.query_one("#search_menu", ListView)
        menu.clear()
        menu.extend([
            MenuListItem("query", f"Consulta: {self.query or '(vazio)'}", "query"),
            MenuListItem("count", f"Quantidade: {self.count}", "count"),
            MenuListItem("orientation", f"Orientação: {self.orientation or 'qualquer'}", "orientation"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar busca", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    async def execute_search(self):
        if not self.query.strip():
            self.query_one("#result", Static).update("❌ Digite uma consulta")
            return
        
        result = self.query_one("#result", Static)
        result.update("🔄 Buscando...")
        
        try:
            from .apis import pexels_download_files
            files = await asyncio.to_thread(
                pexels_download_files, 
                self.query, 
                count=self.count, 
                orientation=self.orientation or None,
                output=self.output or None
            )
            
            if files:
                text = f"✅ {len(files)} imagem(s) baixada(s)"
                result.update(text)
            else:
                result.update("⚠️ Nenhuma imagem encontrada")
                
        except Exception as e:
            result.update(f"❌ Erro: {str(e)}")

    def action_back(self):
        self.app.pop_screen()

class InputScreen(Screen):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "confirm", "Confirm"),
    ]

    def __init__(self, prompt: str, current_value: str, callback):
        super().__init__()
        self.prompt = prompt
        self.current_value = current_value
        self.callback = callback

    def compose(self) -> ComposeResult:
        yield Static(self.prompt, classes="header")
        yield Input(value=self.current_value, id="input_field")
        yield Static("Enter: Confirmar | Escape: Cancelar", classes="help")

    def on_mount(self):
        self.query_one("#input_field", Input).focus()

    def action_confirm(self):
        value = self.query_one("#input_field", Input).value
        self.callback(value)
        self.app.pop_screen()

    def action_cancel(self):
        self.app.pop_screen()

class SelectScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑"),
        Binding("down,j", "cursor_down", "↓"),
        Binding("enter", "select", "Select"),
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, prompt: str, options: list, current_value: str, callback):
        super().__init__()
        self.prompt = prompt
        self.options = options
        self.current_value = current_value
        self.callback = callback

    def compose(self) -> ComposeResult:
        yield Static(self.prompt, classes="header")
        yield ListView(
            *[MenuListItem(label, f"Selecionar {label}", value) 
              for label, value in self.options],
            id="select_menu"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            self.callback(item.action)
            self.app.pop_screen()

    def action_cancel(self):
        self.app.pop_screen()

class StatusScreen(Screen):
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("📊 STATUS", classes="header")
        yield Static("", id="status_content")

    def on_mount(self) -> None:
        self.refresh_status()

    def refresh_status(self) -> None:
        try:
            from .utils import get_system_status
            status = get_system_status()
            
            content = "--- APIs ---\n"
            for api, status_info in status['apis'].items():
                icon = "✅" if status_info['status'] else "❌"
                content += f"{icon} {api}\n"
            
            content += "\n--- Workspace ---\n"
            ws = status['workspace']
            content += f"📁 {ws['path']}\n"
            for folder, info in ws['folders'].items():
                content += f"{folder}: {info['files']} arquivos, {info['size']}\n"
            content += f"TOTAL: {ws['total_files']} arquivos, {ws['total_size']}\n"
            
        except Exception as e:
            content = f"❌ Erro ao carregar status: {str(e)}"
        
        self.query_one("#status_content", Static).update(content)

    def action_back(self):
        self.app.pop_screen()

    def action_refresh(self):
        self.refresh_status()

class FigmaScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑"),
        Binding("down,j", "cursor_down", "↓"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "back", "Back"),
    ]

    def __init__(self):
        super().__init__()
        self.file_key = ""
        self.max_images = 3
        self.format = "png"
        self.mode = "all"
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Static("🎨 FIGMA", classes="header")
        yield ListView(
            MenuListItem("file_key", f"File Key: {self.file_key or '(vazio)'}", "file_key"),
            MenuListItem("max_images", f"Máximo: {self.max_images}", "max_images"),
            MenuListItem("format", f"Formato: {self.format}", "format"),
            MenuListItem("mode", f"Modo: {self.mode}", "mode"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar", "execute"),
            MenuListItem("back", "← Voltar", "back"),
            id="figma_menu"
        )
        yield Static("", id="result")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "file_key":
                self.app.push_screen(InputScreen("File Key:", self.file_key, self.set_file_key))
            elif item.action == "max_images":
                self.app.push_screen(InputScreen("Máximo:", str(self.max_images), self.set_max_images))
            elif item.action == "format":
                self.app.push_screen(SelectScreen("Formato:", 
                    [("PNG", "png"), ("WebP", "webp"), ("JPG", "jpg"), ("SVG", "svg")],
                    self.format, self.set_format))
            elif item.action == "mode":
                self.app.push_screen(SelectScreen("Modo:", 
                    [("Tudo", "all"), ("Componentes", "components"), ("CSS", "css")],
                    self.mode, self.set_mode))
            elif item.action == "output":
                self.app.push_screen(InputScreen("Output:", self.output, self.set_output))
            elif item.action == "execute":
                self.execute_figma()
            elif item.action == "back":
                self.app.pop_screen()

    def set_file_key(self, value: str):
        self.file_key = value
        self.refresh_menu()

    def set_max_images(self, value: str):
        try:
            self.max_images = int(value) if value else 3
        except ValueError:
            self.max_images = 3
        self.refresh_menu()

    def set_format(self, value: str):
        self.format = value
        self.refresh_menu()

    def set_mode(self, value: str):
        self.mode = value
        self.refresh_menu()

    def set_output(self, value: str):
        self.output = value
        self.refresh_menu()

    def refresh_menu(self):
        menu = self.query_one("#figma_menu", ListView)
        menu.clear()
        menu.extend([
            MenuListItem("file_key", f"File Key: {self.file_key or '(vazio)'}", "file_key"),
            MenuListItem("max_images", f"Máximo: {self.max_images}", "max_images"),
            MenuListItem("format", f"Formato: {self.format}", "format"),
            MenuListItem("mode", f"Modo: {self.mode}", "mode"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    async def execute_figma(self):
        if not self.file_key.strip():
            self.query_one("#result", Static).update("❌ Digite o File Key")
            return
        
        result = self.query_one("#result", Static)
        result.update("🔄 Extraindo...")
        
        try:
            from .apis import figma_download_files
            files = await asyncio.to_thread(
                figma_download_files,
                self.file_key,
                fmt=self.format,
                scale=1.0,
                output=self.output or None,
                nodes=None,
                max_images=self.max_images,
                mode=self.mode
            )
            
            if files:
                text = f"✅ {len(files)} arquivo(s) extraído(s)"
                result.update(text)
            else:
                result.update("⚠️ Nenhum arquivo extraído")
                
        except Exception as e:
            result.update(f"❌ Erro: {str(e)}")

    def action_back(self):
        self.app.pop_screen()

class RepoScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑"),
        Binding("down,j", "cursor_down", "↓"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "back", "Back"),
    ]

    def __init__(self):
        super().__init__()
        self.repo = ""
        self.query = ""
        self.no_ai = False
        self.all_clone = False
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Static("📦 REPOSITÓRIO", classes="header")
        yield ListView(
            MenuListItem("repo", f"Repo: {self.repo or '(vazio)'}", "repo"),
            MenuListItem("query", f"Query: {self.query or '(vazio)'}", "query"),
            MenuListItem("no_ai", f"Sem IA: {'sim' if self.no_ai else 'não'}", "no_ai"),
            MenuListItem("all_clone", f"Clone completo: {'sim' if self.all_clone else 'não'}", "all_clone"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar", "execute"),
            MenuListItem("back", "← Voltar", "back"),
            id="repo_menu"
        )
        yield Static("", id="result")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "repo":
                self.app.push_screen(InputScreen("usuario/repo:", self.repo, self.set_repo))
            elif item.action == "query":
                self.app.push_screen(InputScreen("Query IA:", self.query, self.set_query))
            elif item.action == "no_ai":
                self.no_ai = not self.no_ai
                self.refresh_menu()
            elif item.action == "all_clone":
                self.all_clone = not self.all_clone
                self.refresh_menu()
            elif item.action == "output":
                self.app.push_screen(InputScreen("Output:", self.output, self.set_output))
            elif item.action == "execute":
                self.execute_repo()
            elif item.action == "back":
                self.app.pop_screen()

    def set_repo(self, value: str):
        self.repo = value
        self.refresh_menu()

    def set_query(self, value: str):
        self.query = value
        self.refresh_menu()

    def set_output(self, value: str):
        self.output = value
        self.refresh_menu()

    def refresh_menu(self):
        menu = self.query_one("#repo_menu", ListView)
        menu.clear()
        menu.extend([
            MenuListItem("repo", f"Repo: {self.repo or '(vazio)'}", "repo"),
            MenuListItem("query", f"Query: {self.query or '(vazio)'}", "query"),
            MenuListItem("no_ai", f"Sem IA: {'sim' if self.no_ai else 'não'}", "no_ai"),
            MenuListItem("all_clone", f"Clone completo: {'sim' if self.all_clone else 'não'}", "all_clone"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    async def execute_repo(self):
        if not self.repo.strip() or "/" not in self.repo:
            self.query_one("#result", Static).update("❌ Digite usuario/repositorio")
            return
        
        result = self.query_one("#result", Static)
        result.update("🔄 Baixando...")
        
        try:
            from .apis import repo_download_auto
            files = await asyncio.to_thread(
                repo_download_auto,
                self.repo,
                query=self.query or None,
                no_ai=self.no_ai,
                all_files=self.all_clone,
                output=self.output or None
            )
            
            if files:
                text = f"✅ {len(files)} arquivo(s) baixado(s)"
                result.update(text)
            else:
                result.update("⚠️ Nenhum arquivo baixado")
                
        except Exception as e:
            result.update(f"❌ Erro: {str(e)}")

    def action_back(self):
        self.app.pop_screen()

class ConfigScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑"),
        Binding("down,j", "cursor_down", "↓"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "back", "Back"),
    ]

    def __init__(self):
        super().__init__()
        self.load_config()

    def load_config(self):
        try:
            from .config import get_api_key, get_workspace
            self.pexels_key = "●●●●●" if get_api_key('pexels') else ""
            self.figma_key = "●●●●●" if get_api_key('figma') else ""
            self.gemini_key = "●●●●●" if get_api_key('gemini') else ""
            self.workspace = get_workspace()
        except:
            self.pexels_key = ""
            self.figma_key = ""
            self.gemini_key = ""
            self.workspace = "materials"

    def compose(self) -> ComposeResult:
        yield Static("⚙️ CONFIG", classes="header")
        yield ListView(
            MenuListItem("pexels", f"Pexels: {self.pexels_key or '(não configurado)'}", "pexels"),
            MenuListItem("figma", f"Figma: {self.figma_key or '(não configurado)'}", "figma"),
            MenuListItem("gemini", f"Gemini: {self.gemini_key or '(não configurado)'}", "gemini"),
            MenuListItem("workspace", f"Workspace: {self.workspace}", "workspace"),
            MenuListItem("save", "💾 Salvar", "save"),
            MenuListItem("back", "← Voltar", "back"),
            id="config_menu"
        )
        yield Static("", id="result")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "pexels":
                self.app.push_screen(InputScreen("Chave Pexels:", "", self.set_pexels))
            elif item.action == "figma":
                self.app.push_screen(InputScreen("Token Figma:", "", self.set_figma))
            elif item.action == "gemini":
                self.app.push_screen(InputScreen("Chave Gemini:", "", self.set_gemini))
            elif item.action == "workspace":
                self.app.push_screen(InputScreen("Workspace:", self.workspace, self.set_workspace))
            elif item.action == "save":
                self.save_config()
            elif item.action == "back":
                self.app.pop_screen()

    def set_pexels(self, value: str):
        if value.strip():
            self.pexels_key = "●●●●●"
            self._temp_pexels = value
        self.refresh_menu()

    def set_figma(self, value: str):
        if value.strip():
            self.figma_key = "●●●●●"
            self._temp_figma = value
        self.refresh_menu()

    def set_gemini(self, value: str):
        if value.strip():
            self.gemini_key = "●●●●●"
            self._temp_gemini = value
        self.refresh_menu()

    def set_workspace(self, value: str):
        self.workspace = value
        self.refresh_menu()

    def refresh_menu(self):
        menu = self.query_one("#config_menu", ListView)
        menu.clear()
        menu.extend([
            MenuListItem("pexels", f"Pexels: {self.pexels_key or '(não configurado)'}", "pexels"),
            MenuListItem("figma", f"Figma: {self.figma_key or '(não configurado)'}", "figma"),
            MenuListItem("gemini", f"Gemini: {self.gemini_key or '(não configurado)'}", "gemini"),
            MenuListItem("workspace", f"Workspace: {self.workspace}", "workspace"),
            MenuListItem("save", "💾 Salvar", "save"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    def save_config(self):
        try:
            from .config import set_api_key, set_workspace
            
            if hasattr(self, '_temp_pexels'):
                set_api_key('pexels', self._temp_pexels)
            
            if hasattr(self, '_temp_figma'):
                set_api_key('figma', self._temp_figma)
            
            if hasattr(self, '_temp_gemini'):
                set_api_key('gemini', self._temp_gemini)
            
            set_workspace(self.workspace)
            
            self.query_one("#result", Static).update("✅ Salvo!")
            
        except Exception as e:
            self.query_one("#result", Static).update(f"❌ Erro: {str(e)}")

    def action_back(self):
        self.app.pop_screen()

class CLIToolsApp(App):
    CSS = """
    .header {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1 0;
    }
    
    .help {
        text-align: center;
        color: $text-muted;
        margin: 1 0;
    }
    
    ListView {
        height: 100%;
    }
    
    ListItem {
        height: 1;
        padding: 0 1;
    }
    
    ListItem:hover {
        background: $surface;
    }
    
    #result {
        margin: 1 0;
        padding: 1;
        border: solid $primary;
        min-height: 3;
    }
    
    #status_content {
        margin: 1 0;
        padding: 1;
        border: solid $accent;
        min-height: 10;
    }
    
    Input {
        margin: 1 0;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())

def interactive_menu():
    """Interface navegável por setas como Gemini CLI."""
    app = CLIToolsApp()
    app.run()

if __name__ == "__main__":
    interactive_menu()
