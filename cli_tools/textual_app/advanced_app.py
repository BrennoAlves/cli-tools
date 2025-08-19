"""
CLI Tools - Aplicação Textual Avançada
Usando widgets avançados do framework Textual conforme estudado nos repositórios
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Button, DataTable, Header, Footer, Static, Tree, 
    ProgressBar, LoadingIndicator, TabbedContent, TabPane,
    Input, Select, Checkbox, RadioSet, RadioButton,
    ListView, ListItem, OptionList, SelectionList,
    Switch, Collapsible, DirectoryTree, Log, RichLog,
    Sparkline, Pretty, Markdown, TextArea
)
from textual.reactive import reactive, var
from textual.message import Message
from textual.screen import Screen, ModalScreen
from textual import on, work
from textual.worker import get_current_worker
from textual.validation import Function, Number, Length

import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import random

# Imports do CLI Tools
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.config import ConfigAPI, validar_chaves_api
    from core.controle_uso import controlador_uso
    from core.config_diretorios import ConfigDiretorios
except ImportError:
    # Fallback para modo demo
    class ConfigAPI:
        def __init__(self): pass
        @property
        def pexels_key(self): return "demo_key"
        @property
        def figma_token(self): return "demo_token"
        @property
        def gemini_key(self): return "demo_key"
    
    def validar_chaves_api(): return {}
    
    class MockControlador:
        def get_uso_hoje(self, api): return random.randint(0, 50)
        def get_limite(self, api): return {"pexels": 200, "figma": 1000, "gemini": 900}.get(api, 100)
    
    controlador_uso = MockControlador()
    
    class ConfigDiretorios:
        def obter_diretorio(self, tipo): return f"/demo/materials/{tipo}"


class SearchResultsModal(ModalScreen):
    """Modal para mostrar resultados de busca"""
    
    def __init__(self, results: List[Dict[str, Any]]):
        super().__init__()
        self.results = results
    
    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            yield Static("🔍 Resultados da Busca", id="modal-title")
            
            # Lista de resultados
            yield ListView(*[
                ListItem(Static(f"🖼️ {result['title']} - {result['size']}"), id=f"result-{i}")
                for i, result in enumerate(self.results)
            ], id="results-list")
            
            with Horizontal(id="modal-buttons"):
                yield Button("📥 Baixar Selecionados", id="download-btn", variant="success")
                yield Button("❌ Fechar", id="close-btn", variant="error")
    
    @on(Button.Pressed, "#download-btn")
    def download_selected(self) -> None:
        self.notify("📥 Download iniciado! (Demo)", severity="success")
        self.dismiss()
    
    @on(Button.Pressed, "#close-btn")
    def close_modal(self) -> None:
        self.dismiss()


class ConfigModal(ModalScreen):
    """Modal para configuração de APIs"""
    
    def compose(self) -> ComposeResult:
        with Container(id="config-modal"):
            yield Static("⚙️ Configuração de APIs", id="config-modal-title")
            
            with Vertical(id="config-form"):
                # Pexels
                yield Static("🖼️ Pexels API:")
                yield Input(
                    placeholder="Sua chave da API Pexels",
                    id="pexels-key",
                    password=True,
                    validators=[Length(minimum=10)]
                )
                
                # Figma
                yield Static("🎨 Figma Token:")
                yield Input(
                    placeholder="Seu token da API Figma", 
                    id="figma-token",
                    password=True,
                    validators=[Length(minimum=10)]
                )
                
                # Gemini
                yield Static("🤖 Gemini API:")
                yield Input(
                    placeholder="Sua chave da API Gemini",
                    id="gemini-key", 
                    password=True,
                    validators=[Length(minimum=10)]
                )
                
                # Opções avançadas
                with Collapsible(title="🔧 Opções Avançadas"):
                    yield Checkbox("Habilitar cache", id="enable-cache", value=True)
                    yield Checkbox("Logs detalhados", id="verbose-logs")
                    yield Switch("Modo desenvolvedor", id="dev-mode")
            
            with Horizontal(id="config-modal-buttons"):
                yield Button("💾 Salvar", id="save-config", variant="success")
                yield Button("🧪 Testar", id="test-config", variant="primary")
                yield Button("❌ Cancelar", id="cancel-config")
    
    @on(Button.Pressed, "#save-config")
    def save_config(self) -> None:
        self.notify("💾 Configurações salvas! (Demo)", severity="success")
        self.dismiss()
    
    @on(Button.Pressed, "#test-config")
    def test_config(self) -> None:
        self.notify("🧪 Testando APIs... (Demo)", severity="information")
    
    @on(Button.Pressed, "#cancel-config")
    def cancel_config(self) -> None:
        self.dismiss()


class DashboardTab(Static):
    """Tab do dashboard com métricas em tempo real"""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            # Métricas principais
            with Horizontal(id="metrics-row"):
                yield Static("📊 APIs Ativas: 3/3", id="apis-metric", classes="metric-card")
                yield Static("🔥 Requests Hoje: 47", id="requests-metric", classes="metric-card")
                yield Static("💾 Workspace: 584MB", id="storage-metric", classes="metric-card")
            
            # Gráfico de uso (simulado com Sparkline)
            yield Static("📈 Uso das APIs (últimos 7 dias):")
            yield Sparkline([10, 15, 8, 23, 17, 31, 47], id="usage-sparkline")
            
            # Tabela de status detalhado
            yield DataTable(id="detailed-status")
    
    def on_mount(self) -> None:
        """Configurar tabela detalhada"""
        table = self.query_one("#detailed-status", DataTable)
        table.add_columns("API", "Status", "Último Uso", "Quota", "Performance")
        
        table.add_row("🖼️ Pexels", "🟢 Online", "2 min atrás", "47/200", "⚡ Rápida")
        table.add_row("🎨 Figma", "🟢 Online", "15 min atrás", "12/1000", "⚡ Rápida")
        table.add_row("🤖 Gemini", "🟢 Online", "1 min atrás", "23/900", "⚡ Rápida")


class SearchTab(Static):
    """Tab de busca avançada com filtros"""
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            # Formulário de busca (esquerda)
            with Vertical(id="search-form", classes="form-panel"):
                yield Static("🔍 Busca de Imagens", classes="panel-title")
                
                yield Input(placeholder="Digite sua busca...", id="search-query")
                
                yield Static("Quantidade:")
                yield Select([
                    ("3 imagens", 3),
                    ("5 imagens", 5), 
                    ("10 imagens", 10),
                    ("20 imagens", 20),
                    ("50 imagens", 50)
                ], value=5, id="image-count")
                
                yield Static("Orientação:")
                yield RadioSet(
                    RadioButton("Qualquer", value=True, id="any-orientation"),
                    RadioButton("Landscape", id="landscape"),
                    RadioButton("Portrait", id="portrait"),
                    RadioButton("Square", id="square"),
                    id="orientation-set"
                )
                
                yield Static("Tamanho:")
                yield SelectionList(
                    ("Small (640px)", "small", False),
                    ("Medium (1280px)", "medium", True),
                    ("Large (1920px)", "large", False),
                    ("Original", "original", False),
                    id="size-selection"
                )
                
                with Collapsible(title="🎨 Filtros Avançados"):
                    yield Checkbox("Apenas fotos", id="photos-only", value=True)
                    yield Checkbox("Cores vibrantes", id="vibrant-colors")
                    yield Checkbox("Alta resolução", id="high-res")
                
                yield Button("🔍 Buscar", id="start-search", variant="primary")
            
            # Área de resultados (direita)
            with Vertical(id="results-panel", classes="results-panel"):
                yield Static("📋 Resultados", classes="panel-title")
                yield Static("Nenhuma busca realizada ainda.", id="results-status")
                yield ProgressBar(id="search-progress", show_eta=True)
    
    @on(Button.Pressed, "#start-search")
    def start_search(self) -> None:
        """Iniciar busca com animação"""
        query_input = self.query_one("#search-query", Input)
        if not query_input.value.strip():
            self.notify("Digite uma busca!", severity="error")
            return
        
        self.search_images(query_input.value.strip())
    
    @work(exclusive=True)
    async def search_images(self, query: str) -> None:
        """Simular busca de imagens"""
        progress = self.query_one("#search-progress", ProgressBar)
        status = self.query_one("#results-status", Static)
        
        progress.update(total=100)
        status.update("🔍 Buscando imagens...")
        
        # Simular progresso
        for i in range(0, 101, 5):
            progress.update(progress=i)
            await asyncio.sleep(0.1)
        
        # Simular resultados
        results = [
            {"title": f"Imagem {i+1} - {query}", "size": "1920x1080"}
            for i in range(5)
        ]
        
        status.update(f"✅ Encontradas {len(results)} imagens!")
        
        # Mostrar modal com resultados
        self.app.push_screen(SearchResultsModal(results))


class RepoTab(Static):
    """Tab de exploração de repositórios"""
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            # Árvore de diretórios (esquerda)
            with Vertical(id="repo-tree-panel", classes="tree-panel"):
                yield Static("📁 Explorador", classes="panel-title")
                yield DirectoryTree("/home/desk/materials/repos", id="repo-tree")
            
            # Preview de código (direita)
            with Vertical(id="code-preview-panel", classes="preview-panel"):
                yield Static("👁️ Preview", classes="panel-title")
                yield TextArea(
                    "# Selecione um arquivo na árvore para visualizar\n\n"
                    "def hello_world():\n"
                    "    print('Hello from CLI Tools!')\n"
                    "    return 'Textual Framework is awesome!'\n\n"
                    "if __name__ == '__main__':\n"
                    "    hello_world()",
                    language="python",
                    id="code-preview",
                    read_only=True
                )
    
    @on(DirectoryTree.FileSelected)
    def show_file_preview(self, event: DirectoryTree.FileSelected) -> None:
        """Mostrar preview do arquivo selecionado"""
        file_path = event.path
        preview = self.query_one("#code-preview", TextArea)
        
        try:
            if file_path.suffix in ['.py', '.js', '.ts', '.css', '.html', '.md']:
                content = file_path.read_text(encoding='utf-8')[:2000]  # Limitar tamanho
                preview.text = content
                self.notify(f"📄 Carregado: {file_path.name}", severity="success")
            else:
                preview.text = f"# Arquivo binário: {file_path.name}\n\nTipo: {file_path.suffix}\nTamanho: {file_path.stat().st_size} bytes"
        except Exception as e:
            preview.text = f"# Erro ao carregar arquivo\n\n{str(e)}"
            self.notify("Erro ao carregar arquivo", severity="error")


class LogsTab(Static):
    """Tab de logs do sistema"""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="logs-controls"):
                yield Button("🗑️ Limpar", id="clear-logs")
                yield Button("📥 Exportar", id="export-logs")
                yield Switch("Auto-scroll", id="auto-scroll", value=True)
            
            yield RichLog(id="system-logs", highlight=True, markup=True)
    
    def on_mount(self) -> None:
        """Adicionar logs de exemplo"""
        log = self.query_one("#system-logs", RichLog)
        
        log.write("[bold green]✅ Sistema iniciado[/bold green]")
        log.write("[blue]ℹ️ Carregando configurações...[/blue]")
        log.write("[yellow]⚠️ API Pexels: Quota em 23%[/yellow]")
        log.write("[green]✅ Workspace configurado: /home/desk/materials[/green]")
        log.write("[blue]ℹ️ Interface Textual carregada[/blue]")
        log.write("[cyan]🔍 Pronto para buscas![/cyan]")
    
    @on(Button.Pressed, "#clear-logs")
    def clear_logs(self) -> None:
        """Limpar logs"""
        self.query_one("#system-logs", RichLog).clear()
        self.notify("Logs limpos", severity="information")
    
    @on(Button.Pressed, "#export-logs")
    def export_logs(self) -> None:
        """Exportar logs"""
        self.notify("Logs exportados para logs.txt (Demo)", severity="success")


class MainScreen(Screen):
    """Tela principal com tabs"""
    
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("d", "toggle_dark", "Tema"),
        ("c", "open_config", "Config"),
        ("s", "screenshot", "Screenshot"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(id="main-container"):
            yield Static("🛠️ CLI Tools - Textual Framework", id="app-title")
            
            with TabbedContent(initial="dashboard"):
                with TabPane("📊 Dashboard", id="dashboard"):
                    yield DashboardTab()
                
                with TabPane("🔍 Search", id="search"):
                    yield SearchTab()
                
                with TabPane("📁 Repos", id="repos"):
                    yield RepoTab()
                
                with TabPane("📋 Logs", id="logs"):
                    yield LogsTab()
        
        yield Footer()
    
    def action_open_config(self) -> None:
        """Abrir modal de configuração"""
        self.app.push_screen(ConfigModal())
    
    def action_screenshot(self) -> None:
        """Tirar screenshot"""
        path = self.app.save_screenshot()
        self.notify(f"📸 Screenshot: {path}", severity="success")


class AdvancedCLIToolsApp(App):
    """Aplicação CLI Tools avançada usando Textual"""
    
    TITLE = "CLI Tools - Advanced Textual Interface"
    SUB_TITLE = "Framework Textual com widgets avançados"
    
    CSS = """
    /* Tema Dracula */
    Screen {
        background: #282a36;
        color: #f8f8f2;
    }
    
    #app-title {
        text-align: center;
        text-style: bold;
        color: #bd93f9;
        margin: 1;
    }
    
    /* Panels */
    .form-panel {
        width: 1fr;
        border: solid #6272a4;
        padding: 1;
        margin: 0 1 0 0;
    }
    
    .results-panel {
        width: 2fr;
        border: solid #6272a4;
        padding: 1;
    }
    
    .tree-panel {
        width: 1fr;
        border: solid #6272a4;
        padding: 1;
        margin: 0 1 0 0;
    }
    
    .preview-panel {
        width: 2fr;
        border: solid #6272a4;
        padding: 1;
    }
    
    .panel-title {
        text-style: bold;
        color: #8be9fd;
        margin: 0 0 1 0;
    }
    
    /* Métricas */
    #metrics-row {
        height: 5;
        margin: 0 0 1 0;
    }
    
    .metric-card {
        border: solid #50fa7b;
        padding: 1;
        margin: 0 1 0 0;
        text-align: center;
        text-style: bold;
        color: #50fa7b;
    }
    
    /* Widgets */
    Input {
        margin: 0 0 1 0;
        border: solid #6272a4;
    }
    
    Input:focus {
        border: solid #bd93f9;
    }
    
    Select {
        margin: 0 0 1 0;
    }
    
    RadioSet {
        layout: vertical;
        margin: 0 0 1 0;
    }
    
    SelectionList {
        height: 8;
        margin: 0 0 1 0;
    }
    
    DataTable {
        height: 10;
        margin: 1 0;
    }
    
    TextArea {
        height: 100%;
    }
    
    DirectoryTree {
        height: 100%;
    }
    
    RichLog {
        height: 100%;
        border: solid #6272a4;
    }
    
    ProgressBar {
        margin: 1 0;
    }
    
    Sparkline {
        height: 5;
        color: #50fa7b;
        margin: 0 0 1 0;
    }
    
    /* Botões */
    Button {
        margin: 0 1 1 0;
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
    
    /* Modals */
    #modal-container, #config-modal {
        background: #44475a;
        border: solid #bd93f9;
        padding: 2;
        width: 80;
        height: 70%;
    }
    
    #modal-title, #config-modal-title {
        text-align: center;
        text-style: bold;
        color: #bd93f9;
        margin: 0 0 1 0;
    }
    
    #results-list {
        height: 20;
        margin: 1 0;
    }
    
    #config-form {
        height: 80%;
        margin: 1 0;
    }
    
    #modal-buttons, #config-modal-buttons {
        layout: horizontal;
        align: center middle;
        margin: 1 0 0 0;
    }
    
    /* Logs */
    #logs-controls {
        height: 3;
        margin: 0 0 1 0;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("d", "toggle_dark", "Tema"),
        ("ctrl+c", "quit", "Sair"),
    ]
    
    def on_mount(self) -> None:
        """Executado quando a app é montada"""
        self.push_screen(MainScreen())
    
    def action_toggle_dark(self) -> None:
        """Alternar tema"""
        self.dark = not self.dark


if __name__ == "__main__":
    app = AdvancedCLIToolsApp()
    app.run()
