"""
Aplicação Chat CLI Tools v2.0
Interface conversacional moderna e responsiva
"""

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Input, RichLog, Static
from textual.reactive import reactive
from textual.binding import Binding
from rich.console import Console
from rich.text import Text
import shutil
import os
import sys

# Adicionar path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from chat.ascii_art import get_header_with_subtitle, GRADIENT_COLORS
    from chat.messages import (
        get_welcome_message, 
        get_input_placeholder, 
        get_help_text,
        STATUS_MESSAGES,
        NATURAL_RESPONSES,
        ERROR_MESSAGES,
        TIPS
    )
except ImportError:
    # Fallback para teste direto
    def get_header_with_subtitle(width, version="2.0"):
        if width >= 60:
            return f"""
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝

v{version} - Kit de ferramentas para desenvolvedores"""
        else:
            return f"CLI-TOOLS v{version}"
    
    def get_welcome_message(width):
        return """[dim]💡 Como usar:[/dim]
[dim]  • Digite comandos: /search, /figma, /repo[/dim]
[dim]  • Ou fale naturalmente: "Preciso de imagens"[/dim]"""
    
    def get_input_placeholder(width):
        return "Como posso ajudar? Digite comandos ou fale naturalmente..."
    
    def get_help_text(width, command=None):
        return """[bold cyan]🛠️ CLI Tools - Comandos[/bold cyan]

[purple]/search[/purple] <termo>  - Buscar imagens
[purple]/figma[/purple] <chave>   - Extrair designs  
[purple]/repo[/purple] <url>      - Baixar repositório
[purple]/config[/purple]          - Configurar APIs
[purple]/status[/purple]          - Ver status
[purple]/help[/purple]            - Esta ajuda"""
    
    STATUS_MESSAGES = {
        "searching": "🔍 Buscando imagens...",
        "processing": "⚙️ Processando...",
        "success": "✅ Concluído!",
        "configuring": "🔧 Configurando...",
        "analyzing": "🤖 Analisando com IA..."
    }
    
    NATURAL_RESPONSES = {
        "search_detected": "🔍 Entendi! Vou buscar imagens para você.",
        "figma_detected": "🎨 Vou extrair os designs do Figma.",
        "repo_detected": "📦 Vou baixar o repositório.",
        "unknown_intent": "🤔 Não entendi. Tente /help para ver comandos."
    }
    
    ERROR_MESSAGES = {
        "network_error": "🌐 Erro de conexão"
    }
    
    TIPS = {
        "no_config": "💡 Configure as APIs com /config para começar",
        "first_time": "💡 Primeira vez? Tente: /search natureza",
        "empty_search": "💡 Exemplo: /search escritório moderno",
        "figma_help": "💡 Cole a URL do Figma ou apenas a chave",
        "repo_help": "💡 Use owner/repo ou URL completa",
        "shortcuts": "💡 Atalhos: Ctrl+L (limpar), Ctrl+H (ajuda)"
    }


class ChatApp(App):
    """Interface conversacional CLI Tools"""
    
    TITLE = "CLI Tools v2.0"
    SUB_TITLE = "Kit de ferramentas para desenvolvedores"
    
    CSS = """
    /* Tema Dracula */
    Screen {
        background: #282a36;
        color: #f8f8f2;
    }
    
    #header {
        height: auto;
        content-align: center middle;
        text-style: bold;
        color: #bd93f9;
        margin: 1 0;
    }
    
    #chat-container {
        height: 1fr;
        margin: 0 1;
    }
    
    #chat-log {
        height: 1fr;
        border: solid #6272a4;
        padding: 1;
        margin: 0 0 1 0;
    }
    
    #input-container {
        height: 3;
        margin: 0;
    }
    
    #prompt-icon {
        width: 3;
        content-align: center middle;
        color: #8be9fd;
        text-style: bold;
    }
    
    Input {
        border: solid #6272a4;
        background: #44475a;
        color: #f8f8f2;
    }
    
    Input:focus {
        border: solid #bd93f9;
    }
    
    Input > .input--placeholder {
        color: #6272a4;
        text-style: italic;
    }
    
    #footer {
        height: 1;
        background: #44475a;
        color: #6272a4;
        content-align: center middle;
    }
    
    /* Responsividade */
    .compact #header {
        margin: 0;
    }
    
    .compact #chat-container {
        margin: 0;
    }
    
    .minimal #input-container {
        height: 2;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Sair", priority=True),
        Binding("ctrl+l", "clear_chat", "Limpar", show=True),
        Binding("ctrl+h", "show_help", "Ajuda", show=True),
        Binding("escape", "focus_input", "Focar Input"),
    ]
    
    # Estado reativo
    terminal_width = reactive(80)
    terminal_height = reactive(24)
    
    def __init__(self):
        super().__init__()
        self.console = Console()
        self.command_history = []
        self.history_index = -1
    
    def compose(self) -> ComposeResult:
        """Compor interface"""
        # Header responsivo
        yield Static("", id="header")
        
        # Container principal
        with Container(id="chat-container"):
            # Log do chat
            yield RichLog(
                id="chat-log",
                highlight=True,
                markup=True,
                auto_scroll=True,
                wrap=True
            )
            
            # Área de input
            with Horizontal(id="input-container"):
                yield Static("💬", id="prompt-icon")
                yield Input(
                    placeholder="Carregando...",
                    id="chat-input"
                )
        
        # Footer com atalhos
        yield Static("", id="footer")
    
    def on_mount(self) -> None:
        """Inicialização da aplicação"""
        self.update_terminal_size()
        self.update_responsive_elements()
        self.show_welcome_message()
        
        # Focar no input
        self.query_one("#chat-input", Input).focus()
    
    def update_terminal_size(self) -> None:
        """Atualizar tamanho do terminal"""
        size = shutil.get_terminal_size()
        self.terminal_width = size.columns
        self.terminal_height = size.lines
    
    def update_responsive_elements(self) -> None:
        """Atualizar elementos baseados no tamanho do terminal"""
        width = self.terminal_width
        
        # Atualizar header
        header_text = get_header_with_subtitle(width)
        self.query_one("#header", Static).update(header_text)
        
        # Atualizar placeholder do input
        placeholder = get_input_placeholder(width)
        self.query_one("#chat-input", Input).placeholder = placeholder
        
        # Atualizar footer
        if width >= 60:
            footer_text = "Ctrl+C: Sair • Ctrl+L: Limpar • Ctrl+H: Ajuda • /help: Comandos"
        elif width >= 40:
            footer_text = "Ctrl+C: Sair • Ctrl+L: Limpar • /help: Comandos"
        else:
            footer_text = "Ctrl+C: Sair • /help"
        
        self.query_one("#footer", Static).update(footer_text)
        
        # Aplicar classes CSS responsivas
        if width < 40:
            self.add_class("minimal")
        elif width < 60:
            self.add_class("compact")
    
    def show_welcome_message(self) -> None:
        """Mostrar mensagem de boas-vindas"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        welcome = get_welcome_message(self.terminal_width)
        chat_log.write(welcome)
        chat_log.write("")
        
        # Dica contextual
        if not self.has_api_config():
            chat_log.write(f"[yellow]{TIPS['no_config']}[/yellow]")
        else:
            chat_log.write(f"[dim]{TIPS['first_time']}[/dim]")
        
        chat_log.write("")
    
    def has_api_config(self) -> bool:
        """Verificar se APIs estão configuradas"""
        # Verificar se existe arquivo .env com chaves
        env_file = os.path.join(os.path.expanduser("~"), ".cli-tools", ".env")
        return os.path.exists(env_file)
    
    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Processar entrada do usuário"""
        user_input = message.value.strip()
        if not user_input:
            return
        
        # Adicionar ao histórico
        self.command_history.append(user_input)
        self.history_index = len(self.command_history)
        
        # Limpar input
        input_widget = self.query_one("#chat-input", Input)
        input_widget.value = ""
        
        # Mostrar mensagem do usuário
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.write(f"[bold cyan]> {user_input}[/bold cyan]")
        
        # Processar comando
        try:
            await self.process_user_input(user_input)
        except Exception as e:
            chat_log.write(f"[red]{ERROR_MESSAGES['network_error']}: {str(e)}[/red]")
        
        chat_log.write("")  # Linha em branco
    
    async def process_user_input(self, user_input: str) -> None:
        """Processar entrada do usuário"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        # Comandos slash
        if user_input.startswith('/'):
            await self.handle_slash_command(user_input)
        else:
            # Linguagem natural
            await self.handle_natural_language(user_input)
    
    async def handle_slash_command(self, command: str) -> None:
        """Processar comandos slash"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == '/search':
            await self.cmd_search(args)
        elif cmd == '/figma':
            await self.cmd_figma(args)
        elif cmd == '/repo':
            await self.cmd_repo(args)
        elif cmd == '/config':
            await self.cmd_config()
        elif cmd == '/status':
            await self.cmd_status()
        elif cmd == '/theme':
            await self.cmd_theme(args)
        elif cmd == '/clear':
            self.action_clear_chat()
        elif cmd == '/help':
            self.show_help(args[0] if args else None)
        else:
            chat_log.write(f"[red]❌ Comando desconhecido: {cmd}[/red]")
            chat_log.write(f"[yellow]{TIPS['shortcuts']}[/yellow]")
    
    async def handle_natural_language(self, text: str) -> None:
        """Processar linguagem natural"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        text_lower = text.lower()
        
        # Detectar intenções
        if any(word in text_lower for word in ["imagem", "foto", "picture", "buscar"]):
            chat_log.write(f"[green]{NATURAL_RESPONSES['search_detected']}[/green]")
            # Extrair termo de busca
            query = self.extract_search_term(text)
            if query:
                await self.cmd_search([query])
            else:
                chat_log.write(f"[yellow]{TIPS['empty_search']}[/yellow]")
        
        elif "figma" in text_lower:
            chat_log.write(f"[green]{NATURAL_RESPONSES['figma_detected']}[/green]")
            chat_log.write(f"[yellow]{TIPS['figma_help']}[/yellow]")
        
        elif any(word in text_lower for word in ["repo", "repositório", "github"]):
            chat_log.write(f"[green]{NATURAL_RESPONSES['repo_detected']}[/green]")
            chat_log.write(f"[yellow]{TIPS['repo_help']}[/yellow]")
        
        elif any(word in text_lower for word in ["config", "configurar", "api"]):
            await self.cmd_config()
        
        elif any(word in text_lower for word in ["status", "estado", "saúde"]):
            await self.cmd_status()
        
        else:
            chat_log.write(f"[yellow]{NATURAL_RESPONSES['unknown_intent']}[/yellow]")
            chat_log.write(f"[dim]{TIPS['shortcuts']}[/dim]")
    
    def extract_search_term(self, text: str) -> str:
        """Extrair termo de busca da linguagem natural"""
        import re
        
        patterns = [
            r"imagens? (?:de |do |da )?(.+)",
            r"fotos? (?:de |do |da )?(.+)",
            r"buscar (.+)",
            r"encontrar (.+)",
            r"preciso (?:de )?(.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    async def cmd_search(self, args: list) -> None:
        """Comando /search"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        if not args:
            chat_log.write(f"[yellow]🔍 Uso: /search <termo de busca>[/yellow]")
            chat_log.write(f"[dim]Exemplo: /search escritório moderno[/dim]")
            return
        
        query = " ".join(args)
        chat_log.write(f"[green]{STATUS_MESSAGES['searching']}[/green]")
        chat_log.write(f"[dim]Termo: '{query}'[/dim]")
        
        # Simular busca (integrar com API real depois)
        import asyncio
        await asyncio.sleep(1)
        
        chat_log.write(f"[green]{STATUS_MESSAGES['success']} 5 imagens salvas em materials/imagens/[/green]")
    
    async def cmd_figma(self, args: list) -> None:
        """Comando /figma"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        if not args:
            chat_log.write(f"[yellow]🎨 Uso: /figma <chave_do_arquivo>[/yellow]")
            chat_log.write(f"[dim]Exemplo: /figma abc123def[/dim]")
            return
        
        key = args[0]
        chat_log.write(f"[green]{STATUS_MESSAGES['processing']}[/green]")
        chat_log.write(f"[dim]Chave: {key}[/dim]")
        
        # Simular extração
        import asyncio
        await asyncio.sleep(1.5)
        
        chat_log.write(f"[green]{STATUS_MESSAGES['success']} Designs extraídos para materials/figma/[/green]")
    
    async def cmd_repo(self, args: list) -> None:
        """Comando /repo"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        if not args:
            chat_log.write(f"[yellow]📦 Uso: /repo <url_ou_owner/repo>[/yellow]")
            chat_log.write(f"[dim]Exemplo: /repo tailwindcss/tailwindcss[/dim]")
            return
        
        repo = args[0]
        chat_log.write(f"[green]{STATUS_MESSAGES['analyzing']}[/green]")
        chat_log.write(f"[dim]Repositório: {repo}[/dim]")
        
        # Simular análise
        import asyncio
        await asyncio.sleep(2)
        
        chat_log.write(f"[green]{STATUS_MESSAGES['success']} Repositório baixado para materials/repos/[/green]")
    
    async def cmd_config(self) -> None:
        """Comando /config"""
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.write(f"[blue]{STATUS_MESSAGES['configuring']}[/blue]")
        chat_log.write("[dim]Abrindo configuração de APIs...[/dim]")
        
        # TODO: Implementar dialog de configuração
        import asyncio
        await asyncio.sleep(0.5)
        
        chat_log.write("[green]💡 Use o comando tradicional: cli-tools config[/green]")
    
    async def cmd_status(self) -> None:
        """Comando /status"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        status_text = """[bold cyan]📊 Status do Sistema[/bold cyan]

[bold yellow]APIs:[/bold yellow]
  🖼️ Pexels:  [green]✅ Ativo[/green] (47/200 requests)
  🎨 Figma:   [green]✅ Ativo[/green] (12/1000 requests)  
  🤖 Gemini:  [green]✅ Ativo[/green] (23/900 requests)

[bold yellow]Workspace:[/bold yellow]
  📁 Imagens: 127 arquivos (584 MB)
  🎨 Figma:   23 designs (156 MB)
  📦 Repos:   8 repositórios (2.1 GB)

[bold yellow]Sistema:[/bold yellow]
  💾 Espaço livre: 45.2 GB
  🌐 Conexão: [green]Online[/green]
  ⚡ Performance: [green]Ótima[/green]"""
        
        chat_log.write(status_text)
    
    async def cmd_theme(self, args: list) -> None:
        """Comando /theme"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        if not args:
            chat_log.write("[cyan]🎨 Temas disponíveis: dracula (atual), light, auto[/cyan]")
            return
        
        theme = args[0].lower()
        if theme in ["dracula", "light", "auto"]:
            chat_log.write(f"[green]🎨 Tema alterado para: {theme}[/green]")
        else:
            chat_log.write(f"[red]❌ Tema desconhecido: {theme}[/red]")
    
    def show_help(self, command: str = None) -> None:
        """Mostrar ajuda"""
        chat_log = self.query_one("#chat-log", RichLog)
        help_text = get_help_text(self.terminal_width, command)
        chat_log.write(help_text)
    
    def action_clear_chat(self) -> None:
        """Limpar chat"""
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.clear()
        self.show_welcome_message()
    
    def action_show_help(self) -> None:
        """Mostrar ajuda via atalho"""
        self.show_help()
    
    def action_focus_input(self) -> None:
        """Focar no input"""
        self.query_one("#chat-input", Input).focus()
    
    def on_resize(self, event) -> None:
        """Reagir a mudanças de tamanho do terminal"""
        self.update_terminal_size()
        self.update_responsive_elements()


if __name__ == "__main__":
    app = ChatApp()
    app.run()
