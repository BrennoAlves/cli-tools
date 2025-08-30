"""
Interface interativa do terminal.
"""

from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Input, ProgressBar
from textual.containers import Vertical, Container
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
from rich.align import Align
def validate_query(value):
    """Validador para consulta de busca."""
    if not value.strip():
        return False, "Consulta não pode estar vazia"
    if len(value.strip()) < 2:
        return False, "Consulta deve ter pelo menos 2 caracteres"
    return True, ""

def validate_count(value):
    """Validador para quantidade."""
    try:
        num = int(value)
        if num < 1:
            return False, "Deve ser maior que 0"
        if num > 80:
            return False, "Máximo 80 imagens"
        return True, ""
    except ValueError:
        return False, "Deve ser um número"

def validate_figma_key(value):
    """Validador para Figma file key."""
    if not value.strip():
        return False, "File key não pode estar vazio"
    if len(value.strip()) < 10:
        return False, "File key muito curto"
    return True, ""

def validate_repo(value):
    """Validador para repositório."""
    if not value.strip():
        return False, "Repositório não pode estar vazio"
    if "/" not in value:
        return False, "Formato: usuario/repositorio"
    parts = value.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return False, "Formato: usuario/repositorio"
    return True, ""

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
        self.orientation = "landscape"
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Static("🔍 BUSCAR IMAGENS", classes="header")
        yield ListView(
            MenuListItem("query", f"Consulta: {self.query or '(vazio)'}", "query"),
            MenuListItem("count", f"Quantidade: {self.count}", "count"),
            MenuListItem("orientation", f"Orientação: {self.orientation}", "orientation"),
            MenuListItem("output", f"Pasta: {self.output or '(padrão)'}", "output"),
            MenuListItem("execute", "🚀 Executar busca", "execute"),
            MenuListItem("back", "← Voltar", "back"),
            id="search_menu"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "query":
                def callback(value):
                    self.query = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen(
                    "Digite a consulta:", 
                    self.query, 
                    callback,
                    validator=validate_query,
                    help_text="💡 Use termos em inglês para melhores resultados (ex: 'office desk', 'mountain landscape')"
                ))
            elif item.action == "count":
                def callback(value):
                    try:
                        self.count = int(value)
                        self.refresh_menu()
                    except ValueError:
                        pass
                self.app.push_screen(InputScreen(
                    "Quantidade de imagens:", 
                    str(self.count), 
                    callback,
                    validator=validate_count,
                    help_text="💡 Máximo 80 imagens por busca. Recomendado: 1-10 para testes."
                ))
            elif item.action == "orientation":
                def callback(value):
                    self.orientation = value
                    self.refresh_menu()
                options = [("landscape", "Paisagem"), ("portrait", "Retrato"), ("square", "Quadrado")]
                self.app.push_screen(SelectScreen("Selecione orientação:", options, callback))
            elif item.action == "output":
                def callback(value):
                    self.output = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen("Pasta de destino:", self.output, callback))
            elif item.action == "execute":
                self.execute_search()
            elif item.action == "back":
                self.app.pop_screen()

    def refresh_menu(self):
        menu = self.query_one("#search_menu")
        menu.clear()
        menu.extend([
            MenuListItem("query", f"Consulta: {self.query or '(vazio)'}", "query"),
            MenuListItem("count", f"Quantidade: {self.count}", "count"),
            MenuListItem("orientation", f"Orientação: {self.orientation}", "orientation"),
            MenuListItem("output", f"Pasta: {self.output or '(padrão)'}", "output"),
            MenuListItem("execute", "🚀 Executar busca", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    def execute_search(self):
        if not self.query:
            return
        
        def operation():
            from src.lib.apis import pexels_download_files
            files = pexels_download_files(
                self.query, 
                count=self.count, 
                orientation=self.orientation, 
                output=self.output if self.output else None
            )
            
            if files:
                result = f"✅ {len(files)} imagem(ns) baixada(s):\n\n"
                for f in files:
                    result += f"📁 {f['nome']} ({f['tamanho']})\n"
                return result
            else:
                return "⚠️ Nenhuma imagem encontrada."
        
        self.app.push_screen(ProgressScreen("Buscando Imagens", operation))

    def show_result(self, message):
        self.app.push_screen(ResultScreen("Resultado da Busca", message))

    def action_back(self):
        self.app.pop_screen()

class InputScreen(Screen):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("f1", "help", "Help"),
    ]

    def __init__(self, prompt: str, current_value: str, callback, validator=None, help_text=""):
        super().__init__()
        self.prompt = prompt
        self.current_value = current_value
        self.callback = callback
        self.validator = validator
        self.help_text = help_text

    def compose(self) -> ComposeResult:
        yield Static(self.prompt, classes="header")
        yield Input(value=self.current_value, id="input_field")
        yield Static("", id="validation_msg", classes="validation")
        yield Static("Enter: Confirmar | Escape: Cancelar | F1: Ajuda", classes="help")
        if self.help_text:
            yield Static(self.help_text, id="help_content", classes="help_hidden")

    def on_mount(self):
        self.query_one("#input_field").focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        if self.validator:
            is_valid, msg = self.validator(event.value)
            validation_widget = self.query_one("#validation_msg")
            if is_valid:
                validation_widget.update("✅ Válido")
                validation_widget.add_class("valid")
                validation_widget.remove_class("invalid")
            else:
                validation_widget.update(f"❌ {msg}")
                validation_widget.add_class("invalid")
                validation_widget.remove_class("valid")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.value.strip()
        if self.validator:
            is_valid, msg = self.validator(value)
            if not is_valid:
                return  # Não submete se inválido
        self.callback(value)
        self.app.pop_screen()

    def action_cancel(self):
        self.app.pop_screen()

    def action_help(self):
        help_widget = self.query_one("#help_content")
        if help_widget.has_class("help_hidden"):
            help_widget.remove_class("help_hidden")
            help_widget.add_class("help_visible")
        else:
            help_widget.add_class("help_hidden")
            help_widget.remove_class("help_visible")

class SelectScreen(Screen):
    BINDINGS = [
        Binding("up,k", "cursor_up", "↑"),
        Binding("down,j", "cursor_down", "↓"),
        Binding("enter", "select", "Enter"),
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, prompt: str, options: list, callback):
        super().__init__()
        self.prompt = prompt
        self.options = options
        self.callback = callback

    def compose(self) -> ComposeResult:
        yield Static(self.prompt, classes="header")
        yield ListView(
            *[MenuListItem(label, f"Selecionar {label}", value) 
              for value, label in self.options],
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
    ]

    def compose(self) -> ComposeResult:
        yield Static("📊 STATUS", classes="header")
        yield Static("", id="status_content")

    def on_mount(self):
        self.refresh_status()

    def refresh_status(self):
        try:
            from src.lib.utils import get_system_status
            status_data = get_system_status()
            
            content = []
            content.append("🔧 Sistema:")
            content.append(f"  Workspace: {status_data.get('workspace', 'N/A')}")
            content.append(f"  Tema: {status_data.get('theme', 'N/A')}")
            content.append("")
            content.append("🔑 APIs:")
            apis = status_data.get('apis', {})
            for api, status in apis.items():
                icon = "✅" if status else "❌"
                content.append(f"  {api}: {icon}")
            
            self.query_one("#status_content").update("\n".join(content))
        except Exception as e:
            self.query_one("#status_content").update(f"Erro ao carregar status: {e}")

    def action_back(self):
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
        self.mode = "all"
        self.format = "png"
        self.max_images = 10
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Static("🎨 FIGMA", classes="header")
        yield ListView(
            MenuListItem("file_key", f"File Key: {self.file_key or '(vazio)'}", "file_key"),
            MenuListItem("mode", f"Modo: {self.mode}", "mode"),
            MenuListItem("format", f"Formato: {self.format}", "format"),
            MenuListItem("max_images", f"Máximo: {self.max_images}", "max_images"),
            MenuListItem("output", f"Pasta: {self.output or '(padrão)'}", "output"),
            MenuListItem("execute", "🚀 Executar extração", "execute"),
            MenuListItem("back", "← Voltar", "back"),
            id="figma_menu"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "file_key":
                def callback(value):
                    self.file_key = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen(
                    "Digite o File Key do Figma:", 
                    self.file_key, 
                    callback,
                    validator=validate_figma_key,
                    help_text="💡 Encontre o File Key na URL do Figma: figma.com/file/[FILE_KEY]/nome-do-projeto"
                ))
            elif item.action == "mode":
                def callback(value):
                    self.mode = value
                    self.refresh_menu()
                options = [("all", "Tudo"), ("components", "Componentes"), ("css", "CSS")]
                self.app.push_screen(SelectScreen("Selecione o modo:", options, callback))
            elif item.action == "format":
                def callback(value):
                    self.format = value
                    self.refresh_menu()
                options = [("png", "PNG"), ("jpg", "JPG"), ("svg", "SVG")]
                self.app.push_screen(SelectScreen("Selecione o formato:", options, callback))
            elif item.action == "max_images":
                def callback(value):
                    try:
                        self.max_images = int(value)
                        self.refresh_menu()
                    except ValueError:
                        pass
                self.app.push_screen(InputScreen("Máximo de imagens:", str(self.max_images), callback))
            elif item.action == "output":
                def callback(value):
                    self.output = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen("Pasta de destino:", self.output, callback))
            elif item.action == "execute":
                self.execute_figma()
            elif item.action == "back":
                self.app.pop_screen()

    def refresh_menu(self):
        menu = self.query_one("#figma_menu")
        menu.clear()
        menu.extend([
            MenuListItem("file_key", f"File Key: {self.file_key or '(vazio)'}", "file_key"),
            MenuListItem("mode", f"Modo: {self.mode}", "mode"),
            MenuListItem("format", f"Formato: {self.format}", "format"),
            MenuListItem("max_images", f"Máximo: {self.max_images}", "max_images"),
            MenuListItem("output", f"Pasta: {self.output or '(padrão)'}", "output"),
            MenuListItem("execute", "🚀 Executar extração", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    def execute_figma(self):
        if not self.file_key:
            return
        
        try:
            from src.lib.apis import figma_download_files
            files = figma_download_files(
                self.file_key,
                fmt=self.format,
                scale=1.0,
                output=self.output if self.output else None,
                nodes=None,
                max_images=self.max_images,
                mode=self.mode
            )
            
            if files:
                result = f"✅ {len(files)} arquivo(s) extraído(s):\n\n"
                for f in files:
                    result += f"📁 {f['nome']} ({f['tamanho']})\n"
            else:
                result = "⚠️ Nenhum arquivo gerado."
                
            self.show_result(result)
        except Exception as e:
            self.show_result(f"❌ Erro: {e}")

    def show_result(self, message):
        self.app.push_screen(ResultScreen("Resultado Figma", message))

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
        self.all_files = False
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Static("📦 REPOSITÓRIO", classes="header")
        yield ListView(
            MenuListItem("repo", f"Repo: {self.repo or '(vazio)'}", "repo"),
            MenuListItem("query", f"Query: {self.query or '(vazio)'}", "query"),
            MenuListItem("no_ai", f"Sem IA: {'Sim' if self.no_ai else 'Não'}", "no_ai"),
            MenuListItem("all_files", f"Todos arquivos: {'Sim' if self.all_files else 'Não'}", "all_files"),
            MenuListItem("output", f"Pasta: {self.output or '(padrão)'}", "output"),
            MenuListItem("execute", "🚀 Executar download", "execute"),
            MenuListItem("back", "← Voltar", "back"),
            id="repo_menu"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "repo":
                def callback(value):
                    self.repo = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen(
                    "Digite o repositório (user/repo):", 
                    self.repo, 
                    callback,
                    validator=validate_repo,
                    help_text="💡 Formato: usuario/repositorio (ex: 'facebook/react', 'microsoft/vscode')"
                ))
            elif item.action == "query":
                def callback(value):
                    self.query = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen("Query para IA (opcional):", self.query, callback))
            elif item.action == "no_ai":
                self.no_ai = not self.no_ai
                self.refresh_menu()
            elif item.action == "all_files":
                self.all_files = not self.all_files
                self.refresh_menu()
            elif item.action == "output":
                def callback(value):
                    self.output = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen("Pasta de destino:", self.output, callback))
            elif item.action == "execute":
                self.execute_repo()
            elif item.action == "back":
                self.app.pop_screen()

    def refresh_menu(self):
        menu = self.query_one("#repo_menu")
        menu.clear()
        menu.extend([
            MenuListItem("repo", f"Repo: {self.repo or '(vazio)'}", "repo"),
            MenuListItem("query", f"Query: {self.query or '(vazio)'}", "query"),
            MenuListItem("no_ai", f"Sem IA: {'Sim' if self.no_ai else 'Não'}", "no_ai"),
            MenuListItem("all_files", f"Todos arquivos: {'Sim' if self.all_files else 'Não'}", "all_files"),
            MenuListItem("output", f"Pasta: {self.output or '(padrão)'}", "output"),
            MenuListItem("execute", "🚀 Executar download", "execute"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    def execute_repo(self):
        if not self.repo:
            return
        
        try:
            from src.lib.apis import repo_download_auto
            path = repo_download_auto(
                self.repo,
                query=self.query if self.query else None,
                output=self.output if self.output else None,
                no_ai=self.no_ai,
                all_clone=self.all_files,
                explain=None,
                dry_run=False,
                interactive=False
            )
            
            result = f"✅ Repositório baixado:\n\n📦 {path}"
            self.show_result(result)
        except Exception as e:
            self.show_result(f"❌ Erro: {e}")

    def show_result(self, message):
        self.app.push_screen(ResultScreen("Resultado Repo", message))

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
            from src.lib.config import get_config
            config = get_config()
            self.pexels_key = config.get('apis', {}).get('pexels', '')
            self.figma_key = config.get('apis', {}).get('figma', '')
            self.gemini_key = config.get('apis', {}).get('gemini', '')
            self.workspace = config.get('workspace', '')
            self.theme = config.get('theme', 'transparent')
        except:
            self.pexels_key = ""
            self.figma_key = ""
            self.gemini_key = ""
            self.workspace = ""
            self.theme = "transparent"

    def compose(self) -> ComposeResult:
        yield Static("⚙️ CONFIG", classes="header")
        yield ListView(
            MenuListItem("pexels", f"Pexels: {self.pexels_key or '(não configurado)'}", "pexels"),
            MenuListItem("figma", f"Figma: {self.figma_key or '(não configurado)'}", "figma"),
            MenuListItem("gemini", f"Gemini: {self.gemini_key or '(não configurado)'}", "gemini"),
            MenuListItem("workspace", f"Workspace: {self.workspace or '(padrão)'}", "workspace"),
            MenuListItem("theme", f"Tema: {self.theme}", "theme"),
            MenuListItem("save", "💾 Salvar configurações", "save"),
            MenuListItem("back", "← Voltar", "back"),
            id="config_menu"
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, 'action'):
            if item.action == "pexels":
                def callback(value):
                    self.pexels_key = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen("Pexels API Key:", self.pexels_key, callback))
            elif item.action == "figma":
                def callback(value):
                    self.figma_key = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen("Figma API Token:", self.figma_key, callback))
            elif item.action == "gemini":
                def callback(value):
                    self.gemini_key = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen("Gemini API Key:", self.gemini_key, callback))
            elif item.action == "workspace":
                def callback(value):
                    self.workspace = value
                    self.refresh_menu()
                self.app.push_screen(InputScreen("Workspace path:", self.workspace, callback))
            elif item.action == "theme":
                def callback(value):
                    self.theme = value
                    self.refresh_menu()
                options = [("transparent", "Transparente"), ("dracula", "Dracula")]
                self.app.push_screen(SelectScreen("Selecione o tema:", options, callback))
            elif item.action == "save":
                self.save_config()
            elif item.action == "back":
                self.app.pop_screen()

    def refresh_menu(self):
        menu = self.query_one("#config_menu")
        menu.clear()
        menu.extend([
            MenuListItem("pexels", f"Pexels: {self.pexels_key or '(não configurado)'}", "pexels"),
            MenuListItem("figma", f"Figma: {self.figma_key or '(não configurado)'}", "figma"),
            MenuListItem("gemini", f"Gemini: {self.gemini_key or '(não configurado)'}", "gemini"),
            MenuListItem("workspace", f"Workspace: {self.workspace or '(padrão)'}", "workspace"),
            MenuListItem("theme", f"Tema: {self.theme}", "theme"),
            MenuListItem("save", "💾 Salvar configurações", "save"),
            MenuListItem("back", "← Voltar", "back"),
        ])

    def save_config(self):
        try:
            from src.lib.config import save_config
            config = {
                'apis': {
                    'pexels': self.pexels_key,
                    'figma': self.figma_key,
                    'gemini': self.gemini_key
                },
                'workspace': self.workspace,
                'theme': self.theme
            }
            save_config(config)
            self.show_result("Configurações salvas com sucesso!")
        except Exception as e:
            self.show_result(f"Erro ao salvar: {e}")

    def show_result(self, message):
        self.app.push_screen(ResultScreen("Config", message))

    def action_back(self):
        self.app.pop_screen()

class ProgressScreen(Screen):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, title: str, operation_func, *args, **kwargs):
        super().__init__()
        self.title = title
        self.operation_func = operation_func
        self.args = args
        self.kwargs = kwargs

    def compose(self) -> ComposeResult:
        yield Static(f"⏳ {self.title}", classes="header")
        yield ProgressBar(id="progress_bar")
        yield Static("Executando operação...", id="status_text")
        yield Static("Escape: Cancelar", classes="help")

    async def on_mount(self):
        progress_bar = self.query_one("#progress_bar")
        status_text = self.query_one("#status_text")
        
        try:
            progress_bar.update(progress=30)
            status_text.update("Conectando com API...")
            
            # Executar operação
            result = await self.run_operation()
            
            progress_bar.update(progress=100)
            status_text.update("✅ Concluído!")
            
            # Mostrar resultado após breve pausa
            await asyncio.sleep(1)
            self.app.pop_screen()
            self.app.push_screen(ResultScreen(self.title, result))
            
        except Exception as e:
            progress_bar.update(progress=100)
            status_text.update(f"❌ Erro: {e}")
            await asyncio.sleep(2)
            self.app.pop_screen()

    async def run_operation(self):
        # Simular operação assíncrona
        import asyncio
        await asyncio.sleep(0.5)  # Simular delay de rede
        
        # Executar função real
        return self.operation_func(*self.args, **self.kwargs)

    def action_cancel(self):
        self.app.pop_screen()

class ResultScreen(Screen):
    BINDINGS = [
        Binding("escape,enter,q", "back", "Back"),
    ]

    def __init__(self, title: str, message: str):
        super().__init__()
        self.title = title
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static(f"📋 {self.title}", classes="header")
        yield Static(self.message, id="result_content")
        yield Static("Enter/Escape: Voltar", classes="help")

    def action_back(self):
        self.app.pop_screen()

class CLIToolsApp(App):
    CSS = """
    .header {
        background: #bd93f9;
        color: #282a36;
        text-align: center;
        padding: 1;
        margin-bottom: 1;
    }
    
    .help {
        background: #44475a;
        color: #f8f8f2;
        text-align: center;
        padding: 1;
        margin-top: 1;
    }
    
    .validation {
        text-align: center;
        padding: 0 1;
        margin: 0;
    }
    
    .validation.valid {
        background: #50fa7b;
        color: #282a36;
    }
    
    .validation.invalid {
        background: #ff5555;
        color: #f8f8f2;
    }
    
    .help_hidden {
        display: none;
    }
    
    .help_visible {
        background: #6272a4;
        color: #f8f8f2;
        padding: 1;
        margin: 1 0;
    }
    
    ListView {
        background: #282a36;
        color: #f8f8f2;
    }
    
    ListItem {
        background: #282a36;
        color: #f8f8f2;
    }
    
    ListItem:hover {
        background: #44475a;
    }
    
    Input {
        background: #44475a;
        color: #f8f8f2;
    }
    
    Static {
        background: #282a36;
        color: #f8f8f2;
    }
    
    #result_content {
        background: #44475a;
        color: #f8f8f2;
        padding: 1;
        margin: 1;
    }
    """

    def on_mount(self):
        self.push_screen(MainMenuScreen())

def run():
    """Executar interface interativa do terminal."""
    app = CLIToolsApp()
    app.run()
