"""
Continuação da interface navegável por setas - telas auxiliares.
"""

from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Input
from textual.containers import Vertical, Container
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
import asyncio

class InputScreen(Screen):
    BINDINGS = [
        Binding("escape", "cancel", "Cancelar"),
        Binding("enter", "confirm", "Confirmar"),
    ]

    def __init__(self, prompt: str, current_value: str, callback):
        super().__init__()
        self.prompt = prompt
        self.current_value = current_value
        self.callback = callback

    def compose(self) -> ComposeResult:
        yield Container(
            Label(self.prompt, classes="input-prompt"),
            Input(value=self.current_value, id="input_field"),
            Label("Enter: Confirmar | Escape: Cancelar", classes="input-help"),
            classes="input-container"
        )

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
        Binding("up,k", "cursor_up", "↑ Cima"),
        Binding("down,j", "cursor_down", "↓ Baixo"),
        Binding("enter", "select", "Selecionar"),
        Binding("escape", "cancel", "Cancelar"),
    ]

    def __init__(self, prompt: str, options: list, current_value: str, callback):
        super().__init__()
        self.prompt = prompt
        self.options = options
        self.current_value = current_value
        self.callback = callback

    def compose(self) -> ComposeResult:
        yield Label(self.prompt, classes="select-prompt")
        yield Container(
            ListView(
                *[MenuListItem(label, f"Selecionar {label}", value) 
                  for label, value in self.options],
                id="select_list"
            ),
            classes="select-container"
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
        Binding("escape", "back", "← Voltar"),
        Binding("r", "refresh", "Atualizar"),
    ]

    def compose(self) -> ComposeResult:
        yield Label("📊 Status do Sistema", classes="screen-title")
        yield Container(
            Static(id="status_content"),
            classes="status-container"
        )

    def on_mount(self) -> None:
        self.refresh_status()

    def refresh_status(self) -> None:
        from src.lib.utils import get_system_status
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
        
        self.query_one("#status_content", Static).update(content)

    def action_back(self):
        self.app.pop_screen()

    def action_refresh(self):
        self.refresh_status()

# Importar MenuListItem da primeira parte
from .ui_arrows import MenuListItem

class FigmaMenuScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑ Cima"),
        Binding("down,j", "cursor_down", "↓ Baixo"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "back", "← Voltar"),
    ]

    def __init__(self):
        super().__init__()
        self.file_key = ""
        self.max_images = 3
        self.format = "png"
        self.mode = "all"
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Label("🎨 Extrair Figma", classes="screen-title")
        yield Container(
            ListView(
                MenuListItem("file_key", f"File Key: {self.file_key or '(vazio)'}", "file_key"),
                MenuListItem("max_images", f"Máximo: {self.max_images}", "max_images"),
                MenuListItem("format", f"Formato: {self.format}", "format"),
                MenuListItem("mode", f"Modo: {self.mode}", "mode"),
                MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
                MenuListItem("execute", "🚀 Executar extração", "execute"),
                MenuListItem("back", "← Voltar", "back"),
                id="figma_list"
            ),
            Static(id="result"),
            classes="form-container"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "file_key":
                self.app.push_screen(InputScreen("Digite o File Key:", self.file_key, self.set_file_key))
            elif item.action == "max_images":
                self.app.push_screen(InputScreen("Digite o máximo:", str(self.max_images), self.set_max_images))
            elif item.action == "format":
                self.app.push_screen(SelectScreen("Formato:", 
                    [("PNG", "png"), ("WebP", "webp"), ("JPG", "jpg"), ("SVG", "svg"), ("PDF", "pdf")],
                    self.format, self.set_format))
            elif item.action == "mode":
                self.app.push_screen(SelectScreen("Modo:", 
                    [("Tudo", "all"), ("Componentes", "components"), ("CSS", "css")],
                    self.mode, self.set_mode))
            elif item.action == "output":
                self.app.push_screen(InputScreen("Digite o diretório:", self.output, self.set_output))
            elif item.action == "execute":
                self.execute_figma()
            elif item.action == "back":
                self.app.pop_screen()

    def set_file_key(self, value: str):
        self.file_key = value
        self.refresh_list()

    def set_max_images(self, value: str):
        try:
            self.max_images = int(value) if value else 3
        except ValueError:
            self.max_images = 3
        self.refresh_list()

    def set_format(self, value: str):
        self.format = value
        self.refresh_list()

    def set_mode(self, value: str):
        self.mode = value
        self.refresh_list()

    def set_output(self, value: str):
        self.output = value
        self.refresh_list()

    def refresh_list(self):
        list_view = self.query_one("#figma_list", ListView)
        list_view.clear()
        list_view.extend([
            MenuListItem("file_key", f"File Key: {self.file_key or '(vazio)'}", "file_key"),
            MenuListItem("max_images", f"Máximo: {self.max_images}", "max_images"),
            MenuListItem("format", f"Formato: {self.format}", "format"),
            MenuListItem("mode", f"Modo: {self.mode}", "mode"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar extração", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    async def execute_figma(self):
        if not self.file_key.strip():
            self.query_one("#result", Static).update("❌ Digite o File Key do Figma")
            return
        
        result_widget = self.query_one("#result", Static)
        result_widget.update("🔄 Extraindo do Figma...")
        
        try:
            from src.lib.apis import figma_download_files
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
                text = f"✅ {len(files)} arquivo(s) extraído(s):\n"
                for f in files:
                    text += f"📁 {f['nome']} ({f['tamanho']})\n"
                result_widget.update(text)
            else:
                result_widget.update("⚠️ Nenhum arquivo extraído")
                
        except Exception as e:
            result_widget.update(f"❌ Erro: {str(e)}")

    def action_back(self):
        self.app.pop_screen()

class RepoMenuScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑ Cima"),
        Binding("down,j", "cursor_down", "↓ Baixo"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "back", "← Voltar"),
    ]

    def __init__(self):
        super().__init__()
        self.repo = ""
        self.query = ""
        self.no_ai = False
        self.all_clone = False
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Label("📦 Baixar Repositório", classes="screen-title")
        yield Container(
            ListView(
                MenuListItem("repo", f"Repositório: {self.repo or '(vazio)'}", "repo"),
                MenuListItem("query", f"Query IA: {self.query or '(vazio)'}", "query"),
                MenuListItem("no_ai", f"Sem IA: {'sim' if self.no_ai else 'não'}", "no_ai"),
                MenuListItem("all_clone", f"Clone completo: {'sim' if self.all_clone else 'não'}", "all_clone"),
                MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
                MenuListItem("execute", "🚀 Executar download", "execute"),
                MenuListItem("back", "← Voltar", "back"),
                id="repo_list"
            ),
            Static(id="result"),
            classes="form-container"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "repo":
                self.app.push_screen(InputScreen("Digite usuario/repo:", self.repo, self.set_repo))
            elif item.action == "query":
                self.app.push_screen(InputScreen("Digite a query:", self.query, self.set_query))
            elif item.action == "no_ai":
                self.no_ai = not self.no_ai
                self.refresh_list()
            elif item.action == "all_clone":
                self.all_clone = not self.all_clone
                self.refresh_list()
            elif item.action == "output":
                self.app.push_screen(InputScreen("Digite o diretório:", self.output, self.set_output))
            elif item.action == "execute":
                self.execute_repo()
            elif item.action == "back":
                self.app.pop_screen()

    def set_repo(self, value: str):
        self.repo = value
        self.refresh_list()

    def set_query(self, value: str):
        self.query = value
        self.refresh_list()

    def set_output(self, value: str):
        self.output = value
        self.refresh_list()

    def refresh_list(self):
        list_view = self.query_one("#repo_list", ListView)
        list_view.clear()
        list_view.extend([
            MenuListItem("repo", f"Repositório: {self.repo or '(vazio)'}", "repo"),
            MenuListItem("query", f"Query IA: {self.query or '(vazio)'}", "query"),
            MenuListItem("no_ai", f"Sem IA: {'sim' if self.no_ai else 'não'}", "no_ai"),
            MenuListItem("all_clone", f"Clone completo: {'sim' if self.all_clone else 'não'}", "all_clone"),
            MenuListItem("output", f"Output: {self.output or 'padrão'}", "output"),
            MenuListItem("execute", "🚀 Executar download", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    async def execute_repo(self):
        if not self.repo.strip():
            self.query_one("#result", Static).update("❌ Digite o repositório (usuario/repo)")
            return
        
        if "/" not in self.repo:
            self.query_one("#result", Static).update("❌ Formato inválido. Use: usuario/repositorio")
            return
        
        result_widget = self.query_one("#result", Static)
        result_widget.update("🔄 Baixando repositório...")
        
        try:
            from src.lib.apis import repo_download_auto
            files = await asyncio.to_thread(
                repo_download_auto,
                self.repo,
                query=self.query or None,
                no_ai=self.no_ai,
                all_files=self.all_clone,
                output=self.output or None
            )
            
            if files:
                text = f"✅ {len(files)} arquivo(s) baixado(s):\n"
                for f in files[:10]:  # Mostrar apenas os primeiros 10
                    text += f"📁 {f['nome']}\n"
                if len(files) > 10:
                    text += f"... e mais {len(files) - 10} arquivos\n"
                result_widget.update(text)
            else:
                result_widget.update("⚠️ Nenhum arquivo baixado")
                
        except Exception as e:
            result_widget.update(f"❌ Erro: {str(e)}")

    def action_back(self):
        self.app.pop_screen()

class ConfigMenuScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑ Cima"),
        Binding("down,j", "cursor_down", "↓ Baixo"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "back", "← Voltar"),
    ]

    def __init__(self):
        super().__init__()
        self.load_config()

    def load_config(self):
        from src.lib.config import get_api_key, get_workspace
        self.pexels_key = "●●●●●" if get_api_key('pexels') else ""
        self.figma_key = "●●●●●" if get_api_key('figma') else ""
        self.gemini_key = "●●●●●" if get_api_key('gemini') else ""
        self.workspace = get_workspace()

    def compose(self) -> ComposeResult:
        yield Label("⚙️ Configurações", classes="screen-title")
        yield Container(
            ListView(
                MenuListItem("pexels", f"Pexels API: {self.pexels_key or '(não configurado)'}", "pexels"),
                MenuListItem("figma", f"Figma API: {self.figma_key or '(não configurado)'}", "figma"),
                MenuListItem("gemini", f"Gemini API: {self.gemini_key or '(não configurado)'}", "gemini"),
                MenuListItem("workspace", f"Workspace: {self.workspace}", "workspace"),
                MenuListItem("save", "💾 Salvar configurações", "save"),
                MenuListItem("back", "← Voltar", "back"),
                id="config_list"
            ),
            Static(id="result"),
            classes="form-container"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "pexels":
                self.app.push_screen(InputScreen("Digite a chave Pexels:", "", self.set_pexels))
            elif item.action == "figma":
                self.app.push_screen(InputScreen("Digite o token Figma:", "", self.set_figma))
            elif item.action == "gemini":
                self.app.push_screen(InputScreen("Digite a chave Gemini:", "", self.set_gemini))
            elif item.action == "workspace":
                self.app.push_screen(InputScreen("Digite o workspace:", self.workspace, self.set_workspace))
            elif item.action == "save":
                self.save_config()
            elif item.action == "back":
                self.app.pop_screen()

    def set_pexels(self, value: str):
        if value.strip():
            self.pexels_key = "●●●●●"
            self._temp_pexels = value
        self.refresh_list()

    def set_figma(self, value: str):
        if value.strip():
            self.figma_key = "●●●●●"
            self._temp_figma = value
        self.refresh_list()

    def set_gemini(self, value: str):
        if value.strip():
            self.gemini_key = "●●●●●"
            self._temp_gemini = value
        self.refresh_list()

    def set_workspace(self, value: str):
        self.workspace = value
        self.refresh_list()

    def refresh_list(self):
        list_view = self.query_one("#config_list", ListView)
        list_view.clear()
        list_view.extend([
            MenuListItem("pexels", f"Pexels API: {self.pexels_key or '(não configurado)'}", "pexels"),
            MenuListItem("figma", f"Figma API: {self.figma_key or '(não configurado)'}", "figma"),
            MenuListItem("gemini", f"Gemini API: {self.gemini_key or '(não configurado)'}", "gemini"),
            MenuListItem("workspace", f"Workspace: {self.workspace}", "workspace"),
            MenuListItem("save", "💾 Salvar configurações", "save"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    def save_config(self):
        from src.lib.config import set_api_key, set_workspace
        
        result_widget = self.query_one("#result", Static)
        
        try:
            if hasattr(self, '_temp_pexels'):
                set_api_key('pexels', self._temp_pexels)
            
            if hasattr(self, '_temp_figma'):
                set_api_key('figma', self._temp_figma)
            
            if hasattr(self, '_temp_gemini'):
                set_api_key('gemini', self._temp_gemini)
            
            set_workspace(self.workspace)
            
            result_widget.update("✅ Configurações salvas com sucesso!")
            
        except Exception as e:
            result_widget.update(f"❌ Erro ao salvar: {str(e)}")

    def action_back(self):
        self.app.pop_screen()

class CLIToolsApp(App):
    CSS = """
    .menu-container {
        height: 100%;
        padding: 1;
    }
    
    .form-container {
        height: 100%;
        padding: 1;
    }
    
    .screen-title {
        text-align: center;
        margin: 1 0;
        color: $accent;
        text-style: bold;
    }
    
    .input-container {
        align: center middle;
        width: 60;
        height: auto;
        padding: 2;
    }
    
    .input-prompt {
        text-align: center;
        margin: 1 0;
        color: $accent;
    }
    
    .input-help {
        text-align: center;
        margin: 1 0;
        color: $text-muted;
    }
    
    .select-container {
        height: 100%;
        padding: 1;
    }
    
    .select-prompt {
        text-align: center;
        margin: 1 0;
        color: $accent;
        text-style: bold;
    }
    
    .status-container {
        height: 100%;
        padding: 1;
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
        min-height: 5;
    }
    
    #status_content {
        margin: 1 0;
        padding: 1;
        border: solid $accent;
        min-height: 10;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Sair"),
        Binding("ctrl+q", "quit", "Sair"),
    ]

    def on_mount(self) -> None:
        from .ui_arrows import MainMenuScreen
        self.push_screen(MainMenuScreen())

def interactive_menu():
    """Função principal para iniciar a interface."""
    app = CLIToolsApp()
    app.run()

if __name__ == "__main__":
    interactive_menu()
