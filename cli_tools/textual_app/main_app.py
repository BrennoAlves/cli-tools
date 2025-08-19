"""
CLI Tools - Aplicação Textual Principal
Implementação usando o framework Textual para interfaces TUI interativas
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Button, DataTable, Header, Footer, Static, Tree, 
    ProgressBar, LoadingIndicator, TabbedContent, TabPane,
    Input, Select, Checkbox, RadioSet, RadioButton
)
from textual.reactive import reactive
from textual.message import Message
from textual.screen import Screen
from textual import on, work
from textual.worker import get_current_worker

import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Imports do CLI Tools
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import ConfigAPI, validar_chaves_api
from core.controle_uso import controlador_uso
from core.config_diretorios import ConfigDiretorios


class StatusScreen(Screen):
    """Tela de status das APIs e workspace"""
    
    BINDINGS = [
        ("escape", "app.pop_screen", "Voltar"),
        ("r", "refresh", "Atualizar"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compor a tela de status"""
        yield Header()
        
        with Container(id="status-container"):
            yield Static("📊 Status do Sistema", id="status-title")
            
            # Tabela de APIs
            yield DataTable(id="apis-table")
            
            # Tabela de Workspace
            yield DataTable(id="workspace-table")
            
            # Botões de ação
            with Horizontal(id="status-buttons"):
                yield Button("🔄 Atualizar", id="refresh-btn", variant="primary")
                yield Button("⚙️ Configurar", id="config-btn", variant="success")
                yield Button("📈 Detalhes", id="details-btn")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Executado quando a tela é montada"""
        self.load_status_data()
    
    def load_status_data(self) -> None:
        """Carrega dados de status nas tabelas"""
        # Configurar tabela de APIs
        apis_table = self.query_one("#apis-table", DataTable)
        apis_table.add_columns("API", "Status", "Uso Hoje", "Limite", "Descrição")
        
        # Obter status das APIs
        problemas = validar_chaves_api()
        apis_data = [
            {
                'name': '🖼️ Pexels',
                'status': '✅ Ativo' if 'pexels' not in problemas else '❌ Inativo',
                'usage': controlador_uso.get_uso_hoje('pexels'),
                'limit': controlador_uso.get_limite('pexels'),
                'desc': 'Busca de imagens' if 'pexels' not in problemas else problemas['pexels']
            },
            {
                'name': '🎨 Figma',
                'status': '✅ Ativo' if 'figma' not in problemas else '❌ Inativo',
                'usage': controlador_uso.get_uso_hoje('figma'),
                'limit': controlador_uso.get_limite('figma'),
                'desc': 'Extração de designs' if 'figma' not in problemas else problemas['figma']
            },
            {
                'name': '🤖 Gemini',
                'status': '✅ Ativo' if 'gemini' not in problemas else '❌ Inativo',
                'usage': controlador_uso.get_uso_hoje('gemini'),
                'limit': controlador_uso.get_limite('gemini'),
                'desc': 'IA para análise' if 'gemini' not in problemas else problemas['gemini']
            }
        ]
        
        for api in apis_data:
            apis_table.add_row(
                api['name'],
                api['status'],
                str(api['usage']),
                str(api['limit']),
                api['desc'][:40] + "..." if len(api['desc']) > 40 else api['desc']
            )
        
        # Configurar tabela de workspace
        workspace_table = self.query_one("#workspace-table", DataTable)
        workspace_table.add_columns("Diretório", "Arquivos", "Tamanho (MB)", "Caminho")
        
        try:
            config_dirs = ConfigDiretorios()
            for tipo in ['imagens', 'figma', 'repos']:
                dir_path = Path(config_dirs.obter_diretorio(tipo))
                if dir_path.exists():
                    files = list(dir_path.rglob('*'))
                    file_count = len([f for f in files if f.is_file()])
                    size_mb = sum(f.stat().st_size for f in files if f.is_file() and f.exists()) / (1024*1024)
                else:
                    file_count = 0
                    size_mb = 0.0
                
                workspace_table.add_row(
                    f"📂 {tipo.title()}",
                    str(file_count),
                    f"{size_mb:.1f}",
                    str(dir_path)
                )
        except Exception as e:
            workspace_table.add_row("❌ Erro", "0", "0.0", f"Erro: {str(e)}")
    
    @on(Button.Pressed, "#refresh-btn")
    def refresh_status(self) -> None:
        """Atualizar dados de status"""
        # Limpar tabelas
        self.query_one("#apis-table", DataTable).clear()
        self.query_one("#workspace-table", DataTable).clear()
        
        # Recarregar dados
        self.load_status_data()
        
        self.notify("Status atualizado!", severity="information")
    
    @on(Button.Pressed, "#config-btn")
    def open_config(self) -> None:
        """Abrir tela de configuração"""
        self.app.push_screen(ConfigScreen())
    
    @on(Button.Pressed, "#details-btn")
    def show_details(self) -> None:
        """Mostrar detalhes avançados"""
        self.notify("Funcionalidade em desenvolvimento", severity="warning")
    
    def action_refresh(self) -> None:
        """Ação de atualizar via tecla R"""
        self.refresh_status()


class SearchScreen(Screen):
    """Tela de busca de imagens"""
    
    BINDINGS = [
        ("escape", "app.pop_screen", "Voltar"),
        ("ctrl+s", "start_search", "Buscar"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compor a tela de busca"""
        yield Header()
        
        with Container(id="search-container"):
            yield Static("🔍 Busca de Imagens", id="search-title")
            
            # Formulário de busca
            with Vertical(id="search-form"):
                yield Input(placeholder="Digite sua busca...", id="search-input")
                
                with Horizontal():
                    yield Static("Quantidade:", classes="label")
                    yield Select([("3", 3), ("5", 5), ("10", 10), ("20", 20)], value=5, id="count-select")
                
                with Horizontal():
                    yield Static("Orientação:", classes="label")
                    yield RadioSet(
                        RadioButton("Qualquer", value=True, id="any-radio"),
                        RadioButton("Landscape", id="landscape-radio"),
                        RadioButton("Portrait", id="portrait-radio"),
                        RadioButton("Square", id="square-radio"),
                        id="orientation-radio"
                    )
                
                with Horizontal(id="search-buttons"):
                    yield Button("🔍 Buscar", id="search-btn", variant="primary")
                    yield Button("🗂️ Abrir Pasta", id="open-folder-btn")
            
            # Área de resultados
            yield Container(id="results-container")
            
            # Progress bar (inicialmente oculta)
            yield ProgressBar(id="search-progress", show_eta=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Executado quando a tela é montada"""
        # Ocultar progress bar inicialmente
        self.query_one("#search-progress").display = False
        
        # Focar no input
        self.query_one("#search-input").focus()
    
    @on(Button.Pressed, "#search-btn")
    def start_search(self) -> None:
        """Iniciar busca de imagens"""
        search_input = self.query_one("#search-input", Input)
        count_select = self.query_one("#count-select", Select)
        
        query = search_input.value.strip()
        if not query:
            self.notify("Digite uma busca!", severity="error")
            return
        
        count = count_select.value
        
        # Mostrar progress bar
        progress = self.query_one("#search-progress", ProgressBar)
        progress.display = True
        progress.update(total=100)
        
        # Iniciar busca assíncrona
        self.run_search(query, count)
    
    @work(exclusive=True)
    async def run_search(self, query: str, count: int) -> None:
        """Executar busca de imagens de forma assíncrona"""
        progress = self.query_one("#search-progress", ProgressBar)
        results_container = self.query_one("#results-container")
        
        try:
            # Simular progresso da busca
            for i in range(0, 101, 10):
                progress.update(progress=i)
                await asyncio.sleep(0.1)
            
            # Aqui integraria com o comando search real
            # Por enquanto, simular resultados
            results_container.mount(
                Static(f"✅ Busca concluída!\n\n🔍 Query: {query}\n📊 Quantidade: {count}\n📁 Salvo em: materials/imagens/")
            )
            
            self.notify(f"Busca '{query}' concluída com sucesso!", severity="success")
            
        except Exception as e:
            results_container.mount(Static(f"❌ Erro na busca: {str(e)}"))
            self.notify("Erro na busca!", severity="error")
        
        finally:
            # Ocultar progress bar
            progress.display = False
    
    @on(Button.Pressed, "#open-folder-btn")
    def open_folder(self) -> None:
        """Abrir pasta de imagens"""
        try:
            config_dirs = ConfigDiretorios()
            images_path = config_dirs.obter_diretorio('imagens')
            self.notify(f"Pasta: {images_path}", severity="information")
        except Exception as e:
            self.notify(f"Erro: {str(e)}", severity="error")
    
    def action_start_search(self) -> None:
        """Ação de buscar via Ctrl+S"""
        self.start_search()


class ConfigScreen(Screen):
    """Tela de configuração de APIs"""
    
    BINDINGS = [
        ("escape", "app.pop_screen", "Voltar"),
        ("ctrl+s", "save_config", "Salvar"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compor a tela de configuração"""
        yield Header()
        
        with Container(id="config-container"):
            yield Static("⚙️ Configuração de APIs", id="config-title")
            
            with Vertical(id="config-form"):
                # Pexels API
                yield Static("🖼️ Pexels API Key:", classes="config-label")
                yield Input(placeholder="Sua chave da API Pexels", id="pexels-input", password=True)
                
                # Figma API
                yield Static("🎨 Figma API Token:", classes="config-label")
                yield Input(placeholder="Seu token da API Figma", id="figma-input", password=True)
                
                # Gemini API
                yield Static("🤖 Google Gemini API Key:", classes="config-label")
                yield Input(placeholder="Sua chave da API Gemini", id="gemini-input", password=True)
                
                # Botões
                with Horizontal(id="config-buttons"):
                    yield Button("💾 Salvar", id="save-btn", variant="success")
                    yield Button("🧪 Testar", id="test-btn", variant="primary")
                    yield Button("❌ Cancelar", id="cancel-btn")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Executado quando a tela é montada"""
        # Carregar configurações existentes
        self.load_current_config()
    
    def load_current_config(self) -> None:
        """Carregar configurações atuais"""
        config = ConfigAPI()
        
        if config.pexels_key:
            self.query_one("#pexels-input", Input).value = "●" * 20  # Mascarar chave
        
        if config.figma_token:
            self.query_one("#figma-input", Input).value = "●" * 20  # Mascarar token
        
        if config.gemini_key:
            self.query_one("#gemini-input", Input).value = "●" * 20  # Mascarar chave
    
    @on(Button.Pressed, "#save-btn")
    def save_config(self) -> None:
        """Salvar configurações"""
        self.notify("Configurações salvas! (Funcionalidade em desenvolvimento)", severity="success")
    
    @on(Button.Pressed, "#test-btn")
    def test_apis(self) -> None:
        """Testar APIs"""
        self.notify("Testando APIs... (Funcionalidade em desenvolvimento)", severity="information")
    
    @on(Button.Pressed, "#cancel-btn")
    def cancel_config(self) -> None:
        """Cancelar configuração"""
        self.app.pop_screen()
    
    def action_save_config(self) -> None:
        """Ação de salvar via Ctrl+S"""
        self.save_config()


class MainScreen(Screen):
    """Tela principal com menu de navegação"""
    
    def compose(self) -> ComposeResult:
        """Compor a tela principal"""
        yield Header()
        
        with Container(id="main-container"):
            yield Static("🛠️ CLI Tools - Interface Textual", id="main-title")
            
            with Vertical(id="menu-container"):
                yield Button("📊 Status do Sistema", id="status-menu", variant="primary")
                yield Button("🔍 Buscar Imagens", id="search-menu", variant="success")
                yield Button("🎨 Extrair Figma", id="figma-menu", variant="warning")
                yield Button("📁 Baixar Repositório", id="repo-menu")
                yield Button("⚙️ Configurações", id="config-menu")
                yield Button("❌ Sair", id="exit-menu", variant="error")
        
        yield Footer()
    
    @on(Button.Pressed, "#status-menu")
    def open_status(self) -> None:
        """Abrir tela de status"""
        self.app.push_screen(StatusScreen())
    
    @on(Button.Pressed, "#search-menu")
    def open_search(self) -> None:
        """Abrir tela de busca"""
        self.app.push_screen(SearchScreen())
    
    @on(Button.Pressed, "#figma-menu")
    def open_figma(self) -> None:
        """Abrir tela do Figma"""
        self.notify("Tela Figma em desenvolvimento", severity="warning")
    
    @on(Button.Pressed, "#repo-menu")
    def open_repo(self) -> None:
        """Abrir tela de repositório"""
        self.notify("Tela Repositório em desenvolvimento", severity="warning")
    
    @on(Button.Pressed, "#config-menu")
    def open_config(self) -> None:
        """Abrir tela de configuração"""
        self.app.push_screen(ConfigScreen())
    
    @on(Button.Pressed, "#exit-menu")
    def exit_app(self) -> None:
        """Sair da aplicação"""
        self.app.exit()


class CLIToolsApp(App):
    """Aplicação principal do CLI Tools usando Textual"""
    
    TITLE = "CLI Tools - Textual Interface"
    SUB_TITLE = "Ferramentas para desenvolvedores com IA integrada"
    
    CSS_PATH = "styles.tcss"
    
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("d", "toggle_dark", "Tema"),
        ("s", "screenshot", "Screenshot"),
    ]
    
    def on_mount(self) -> None:
        """Executado quando a app é montada"""
        self.push_screen(MainScreen())
    
    def action_toggle_dark(self) -> None:
        """Alternar tema escuro/claro"""
        self.dark = not self.dark
    
    def action_screenshot(self) -> None:
        """Tirar screenshot da aplicação"""
        path = self.save_screenshot()
        self.notify(f"Screenshot salvo: {path}", severity="success")


if __name__ == "__main__":
    app = CLIToolsApp()
    app.run()
