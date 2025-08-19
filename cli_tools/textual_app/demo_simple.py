"""
Demo simples da aplicação Textual CLI Tools
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Static, Header, Footer, DataTable
from textual.screen import Screen
from textual import on


class DemoScreen(Screen):
    """Tela de demonstração simples"""
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield Static("🛠️ CLI Tools - Demo Textual Framework", id="title")
            yield Static("✅ Framework Textual funcionando corretamente!", id="status")
            
            # Tabela de demonstração
            yield DataTable(id="demo-table")
            
            # Botões de demonstração
            with Horizontal():
                yield Button("📊 Status", id="status-btn", variant="primary")
                yield Button("🔍 Search", id="search-btn", variant="success")
                yield Button("⚙️ Config", id="config-btn", variant="warning")
                yield Button("❌ Sair", id="exit-btn", variant="error")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Configurar tabela de demo"""
        table = self.query_one("#demo-table", DataTable)
        table.add_columns("Componente", "Status", "Framework")
        
        table.add_row("🖼️ Rich", "✅ Ativo", "Renderização")
        table.add_row("🖥️ Textual", "✅ Ativo", "TUI Framework")
        table.add_row("🎯 Widgets", "✅ Funcionando", "Interativos")
        table.add_row("🎨 CSS", "✅ Aplicado", "Estilização")
    
    @on(Button.Pressed, "#status-btn")
    def show_status(self) -> None:
        self.notify("📊 Status: Todos os sistemas operacionais!", severity="success")
    
    @on(Button.Pressed, "#search-btn")
    def show_search(self) -> None:
        self.notify("🔍 Search: Interface de busca disponível!", severity="information")
    
    @on(Button.Pressed, "#config-btn")
    def show_config(self) -> None:
        self.notify("⚙️ Config: Configurações funcionais!", severity="warning")
    
    @on(Button.Pressed, "#exit-btn")
    def exit_demo(self) -> None:
        self.app.exit()


class DemoApp(App):
    """Aplicação de demonstração"""
    
    TITLE = "CLI Tools - Textual Demo"
    
    CSS = """
    Screen {
        background: #282a36;
        color: #f8f8f2;
    }
    
    #title {
        text-align: center;
        text-style: bold;
        color: #bd93f9;
        margin: 1;
    }
    
    #status {
        text-align: center;
        color: #50fa7b;
        margin: 1;
    }
    
    DataTable {
        margin: 1;
        height: 8;
    }
    
    Button {
        margin: 0 1;
    }
    
    Button.-primary {
        background: #bd93f9;
        color: #282a36;
    }
    
    Button.-success {
        background: #50fa7b;
        color: #282a36;
    }
    
    Button.-warning {
        background: #ffb86c;
        color: #282a36;
    }
    
    Button.-error {
        background: #ff5555;
        color: #f8f8f2;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("d", "toggle_dark", "Tema"),
    ]
    
    def on_mount(self) -> None:
        self.push_screen(DemoScreen())


if __name__ == "__main__":
    app = DemoApp()
    app.run()
