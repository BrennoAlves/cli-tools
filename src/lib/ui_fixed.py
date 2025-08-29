"""
Interface moderna com widgets nativos do Textual.
"""

from textual.app import App, ComposeResult
from textual.widgets import (
    Static, Input, Select, Button, Checkbox, 
    Header, Footer, Label, ProgressBar
)
from textual.containers import Vertical, Horizontal, Container
from textual.binding import Binding
from textual.validation import Number, Length
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

class MenuScreen(Screen):
    BINDINGS = [
        Binding("1", "search", "🔍 Buscar Imagens"),
        Binding("2", "figma", "🎨 Figma"),
        Binding("3", "repo", "📦 Repositório"),
        Binding("4", "status", "📊 Status"),
        Binding("5", "config", "⚙️ Config"),
        Binding("q", "quit", "Sair"),
        Binding("escape", "quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        yield HeaderWidget()
        yield Container(
            Label("Escolha uma opção:", classes="menu-label"),
            Button("🔍 Buscar Imagens", id="search", variant="primary"),
            Button("🎨 Extrair Figma", id="figma", variant="success"),
            Button("📦 Baixar Repositório", id="repo", variant="warning"),
            Button("📊 Status do Sistema", id="status"),
            Button("⚙️ Configurações", id="config"),
            Button("❌ Sair", id="quit", variant="error"),
            classes="menu-container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search":
            self.app.push_screen(SearchScreen())
        elif event.button.id == "figma":
            self.app.push_screen(FigmaScreen())
        elif event.button.id == "repo":
            self.app.push_screen(RepoScreen())
        elif event.button.id == "status":
            self.app.push_screen(StatusScreen())
        elif event.button.id == "config":
            self.app.push_screen(ConfigScreen())
        elif event.button.id == "quit":
            self.app.exit()

    def action_search(self) -> None:
        self.app.push_screen(SearchScreen())
    
    def action_figma(self) -> None:
        self.app.push_screen(FigmaScreen())
    
    def action_repo(self) -> None:
        self.app.push_screen(RepoScreen())
    
    def action_status(self) -> None:
        self.app.push_screen(StatusScreen())
    
    def action_config(self) -> None:
        self.app.push_screen(ConfigScreen())

class SearchScreen(Screen):
    BINDINGS = [
        Binding("escape", "back", "Voltar"),
        Binding("f1", "help", "Ajuda"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("🔍 Buscar Imagens", classes="form-title"),
            
            Label("Consulta de busca:"),
            Input(placeholder="Ex: office desk, nature, technology", 
                  validators=[Length(minimum=1)], id="query"),
            
            Label("Quantidade:"),
            Input(placeholder="1", value="1", 
                  validators=[Number(minimum=1, maximum=50)], id="count"),
            
            Label("Orientação:"),
            Select([("Qualquer", ""), ("Paisagem", "landscape"), 
                   ("Retrato", "portrait"), ("Quadrado", "square")], 
                   value="", id="orientation"),
            
            Label("Diretório de saída (opcional):"),
            Input(placeholder="materials/imagens", id="output"),
            
            Horizontal(
                Button("🚀 Executar", variant="primary", id="execute"),
                Button("🔙 Voltar", id="back"),
                classes="button-row"
            ),
            
            Static(id="result"),
            classes="form-container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "execute":
            self.execute_search()
        elif event.button.id == "back":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen("search"))

    async def execute_search(self) -> None:
        query = self.query_one("#query", Input).value
        count = self.query_one("#count", Input).value
        orientation = self.query_one("#orientation", Select).value
        output = self.query_one("#output", Input).value
        
        result_widget = self.query_one("#result", Static)
        
        if not query.strip():
            result_widget.update("❌ Digite uma consulta de busca")
            return
        
        try:
            count_int = int(count) if count else 1
        except ValueError:
            result_widget.update("❌ Quantidade deve ser um número")
            return
        
        result_widget.update("🔄 Buscando imagens...")
        
        try:
            from src.lib.apis import pexels_download_files
            files = await asyncio.to_thread(
                pexels_download_files, 
                query, 
                count=count_int, 
                orientation=orientation or None,
                output=output or None
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

class FigmaScreen(Screen):
    BINDINGS = [
        Binding("escape", "back", "Voltar"),
        Binding("f1", "help", "Ajuda"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("🎨 Extrair Figma", classes="form-title"),
            
            Label("File Key do Figma:"),
            Input(placeholder="Ex: AbCdEfGh123456", 
                  validators=[Length(minimum=8)], id="file_key"),
            
            Label("Máximo de imagens:"),
            Input(placeholder="3", value="3", 
                  validators=[Number(minimum=1, maximum=20)], id="max_images"),
            
            Label("Formato:"),
            Select([("PNG", "png"), ("WebP", "webp"), ("JPG", "jpg"), 
                   ("SVG", "svg"), ("PDF", "pdf")], 
                   value="png", id="format"),
            
            Label("Modo:"),
            Select([("Tudo", "all"), ("Componentes", "components"), 
                   ("CSS", "css")], 
                   value="all", id="mode"),
            
            Label("Diretório de saída (opcional):"),
            Input(placeholder="materials/figma", id="output"),
            
            Horizontal(
                Button("🚀 Executar", variant="primary", id="execute"),
                Button("🔙 Voltar", id="back"),
                classes="button-row"
            ),
            
            Static(id="result"),
            classes="form-container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "execute":
            self.execute_figma()
        elif event.button.id == "back":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen("figma"))

    async def execute_figma(self) -> None:
        file_key = self.query_one("#file_key", Input).value
        max_images = self.query_one("#max_images", Input).value
        fmt = self.query_one("#format", Select).value
        mode = self.query_one("#mode", Select).value
        output = self.query_one("#output", Input).value
        
        result_widget = self.query_one("#result", Static)
        
        if not file_key.strip():
            result_widget.update("❌ Digite o File Key do Figma")
            return
        
        try:
            max_int = int(max_images) if max_images else 3
        except ValueError:
            result_widget.update("❌ Máximo deve ser um número")
            return
        
        result_widget.update("🔄 Extraindo do Figma...")
        
        try:
            from src.lib.apis import figma_download_files
            files = await asyncio.to_thread(
                figma_download_files,
                file_key,
                fmt=fmt,
                scale=1.0,
                output=output or None,
                nodes=None,
                max_images=max_int,
                mode=mode
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

class RepoScreen(Screen):
    BINDINGS = [
        Binding("escape", "back", "Voltar"),
        Binding("f1", "help", "Ajuda"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("📦 Baixar Repositório", classes="form-title"),
            
            Label("Repositório (usuario/repo):"),
            Input(placeholder="Ex: tailwindlabs/tailwindcss", 
                  validators=[Length(minimum=3)], id="repo"),
            
            Label("Query para IA (opcional):"),
            Input(placeholder="Ex: components, frontend, docs", id="query"),
            
            Checkbox("Sem IA (baixar tudo)", id="no_ai"),
            Checkbox("Clone completo", id="all_clone"),
            
            Label("Diretório de saída (opcional):"),
            Input(placeholder="materials/repos", id="output"),
            
            Horizontal(
                Button("🚀 Executar", variant="primary", id="execute"),
                Button("🔙 Voltar", id="back"),
                classes="button-row"
            ),
            
            Static(id="result"),
            classes="form-container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "execute":
            self.execute_repo()
        elif event.button.id == "back":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen("repo"))

    async def execute_repo(self) -> None:
        repo = self.query_one("#repo", Input).value
        query = self.query_one("#query", Input).value
        no_ai = self.query_one("#no_ai", Checkbox).value
        all_clone = self.query_one("#all_clone", Checkbox).value
        output = self.query_one("#output", Input).value
        
        result_widget = self.query_one("#result", Static)
        
        if not repo.strip():
            result_widget.update("❌ Digite o repositório (usuario/repo)")
            return
        
        if "/" not in repo:
            result_widget.update("❌ Formato inválido. Use: usuario/repositorio")
            return
        
        result_widget.update("🔄 Baixando repositório...")
        
        try:
            from src.lib.apis import repo_download_auto
            files = await asyncio.to_thread(
                repo_download_auto,
                repo,
                query=query or None,
                no_ai=no_ai,
                all_files=all_clone,
                output=output or None
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

class StatusScreen(Screen):
    BINDINGS = [
        Binding("escape", "back", "Voltar"),
        Binding("r", "refresh", "Atualizar"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("📊 Status do Sistema", classes="form-title"),
            Static(id="status_content"),
            Button("🔙 Voltar", id="back"),
            classes="form-container"
        )
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_status()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_refresh(self) -> None:
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

class ConfigScreen(Screen):
    BINDINGS = [
        Binding("escape", "back", "Voltar"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("⚙️ Configurações", classes="form-title"),
            
            Label("Chave API Pexels:"),
            Input(placeholder="Digite sua chave Pexels", password=True, id="pexels_key"),
            
            Label("Token API Figma:"),
            Input(placeholder="Digite seu token Figma", password=True, id="figma_key"),
            
            Label("Chave API Gemini:"),
            Input(placeholder="Digite sua chave Gemini", password=True, id="gemini_key"),
            
            Label("Workspace:"),
            Input(placeholder="materials", id="workspace"),
            
            Horizontal(
                Button("💾 Salvar", variant="primary", id="save"),
                Button("🔙 Voltar", id="back"),
                classes="button-row"
            ),
            
            Static(id="result"),
            classes="form-container"
        )
        yield Footer()

    def on_mount(self) -> None:
        from src.lib.config import get_api_key, get_workspace
        
        # Carregar valores atuais (mascarados)
        pexels = get_api_key('pexels')
        if pexels:
            self.query_one("#pexels_key", Input).value = "●" * 20
        
        figma = get_api_key('figma')
        if figma:
            self.query_one("#figma_key", Input).value = "●" * 20
        
        gemini = get_api_key('gemini')
        if gemini:
            self.query_one("#gemini_key", Input).value = "●" * 20
        
        self.query_one("#workspace", Input).value = get_workspace()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.save_config()
        elif event.button.id == "back":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()

    def save_config(self) -> None:
        from src.lib.config import set_api_key, set_workspace
        
        pexels = self.query_one("#pexels_key", Input).value
        figma = self.query_one("#figma_key", Input).value
        gemini = self.query_one("#gemini_key", Input).value
        workspace = self.query_one("#workspace", Input).value
        
        result_widget = self.query_one("#result", Static)
        
        try:
            # Só salvar se não for máscara
            if pexels and not pexels.startswith("●"):
                set_api_key('pexels', pexels)
            
            if figma and not figma.startswith("●"):
                set_api_key('figma', figma)
            
            if gemini and not gemini.startswith("●"):
                set_api_key('gemini', gemini)
            
            if workspace:
                set_workspace(workspace)
            
            result_widget.update("✅ Configurações salvas com sucesso!")
            
        except Exception as e:
            result_widget.update(f"❌ Erro ao salvar: {str(e)}")

class HelpScreen(Screen):
    def __init__(self, topic: str = "general"):
        super().__init__()
        self.topic = topic

    BINDINGS = [
        Binding("escape", "back", "Voltar"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label(f"❓ Ajuda - {self.topic.title()}", classes="form-title"),
            Static(self.get_help_content(), id="help_content"),
            Button("🔙 Voltar", id="back"),
            classes="form-container"
        )
        yield Footer()

    def get_help_content(self) -> str:
        help_texts = {
            "search": """
🔍 Buscar Imagens

Busca e baixa imagens do Pexels.

Campos:
• Consulta: Termo de busca em inglês (ex: "office desk")
• Quantidade: Número de imagens (1-50)
• Orientação: Filtro por formato da imagem
• Output: Diretório personalizado (opcional)

Atalhos:
• F1: Esta ajuda
• Escape: Voltar
• Enter: Executar (quando em botão)
            """,
            "figma": """
🎨 Extrair Figma

Extrai designs e componentes do Figma.

Campos:
• File Key: ID do arquivo Figma (encontre na URL)
• Máximo: Número máximo de imagens (1-20)
• Formato: Tipo de arquivo (PNG, SVG, etc.)
• Modo: O que extrair (tudo, componentes, CSS)
• Output: Diretório personalizado (opcional)

Atalhos:
• F1: Esta ajuda
• Escape: Voltar
• Enter: Executar (quando em botão)
            """,
            "repo": """
📦 Baixar Repositório

Baixa repositórios do GitHub com IA.

Campos:
• Repositório: Formato usuario/repo
• Query: Filtro para IA (ex: "components")
• Sem IA: Baixa todos os arquivos
• Clone completo: Git clone tradicional
• Output: Diretório personalizado (opcional)

Atalhos:
• F1: Esta ajuda
• Escape: Voltar
• Enter: Executar (quando em botão)
            """
        }
        
        return help_texts.get(self.topic, "Ajuda não disponível para este tópico.")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()

class CLIToolsApp(App):
    CSS = """
    .menu-container {
        align: center middle;
        width: 60;
        height: auto;
        padding: 2;
    }
    
    .menu-label {
        text-align: center;
        margin: 1 0;
        color: $accent;
    }
    
    .form-container {
        align: center top;
        width: 80;
        height: auto;
        padding: 2;
        margin: 2;
    }
    
    .form-title {
        text-align: center;
        margin: 1 0;
        color: $accent;
        text-style: bold;
    }
    
    .button-row {
        align: center middle;
        height: auto;
        margin: 1 0;
    }
    
    Button {
        margin: 0 1;
        min-width: 16;
    }
    
    Input {
        margin: 0 0 1 0;
    }
    
    Select {
        margin: 0 0 1 0;
    }
    
    Label {
        margin: 1 0 0 0;
        color: $text;
    }
    
    #result {
        margin: 2 0;
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
    
    #help_content {
        margin: 1 0;
        padding: 1;
        border: solid $success;
        min-height: 15;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Sair"),
        Binding("ctrl+q", "quit", "Sair"),
    ]

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())

def interactive_menu():
    """Função principal para iniciar a interface."""
    app = CLIToolsApp()
    app.run()

if __name__ == "__main__":
    interactive_menu()
