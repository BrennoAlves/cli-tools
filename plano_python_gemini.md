# 🐍 CLI Tools v2.0 - Gemini Style com Python

## 🎯 **ADAPTAÇÃO DOS PADRÕES GEMINI-CLI PARA PYTHON**

### **🏆 EQUIVALÊNCIAS PYTHON ↔ NODE.JS**

| Gemini-CLI (Node.js) | CLI Tools (Python) | Funcionalidade |
|---------------------|-------------------|----------------|
| React + Ink | **Textual + Rich** | TUI Framework |
| TypeScript | **Python + Type Hints** | Type Safety |
| Chalk | **Rich.console** | Cores e styling |
| Ink-gradient | **Rich.gradient** | Gradientes |
| String-width | **Rich.measure** | Medição de texto |
| Yargs | **Click** | Argument parsing |
| Vitest | **Pytest** | Testing framework |

---

## 🎨 **INTERFACE CONVERSACIONAL PYTHON**

### **Arquitetura Principal**
```python
# cli_tools/chat_app.py
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Input, Static, RichLog
from textual.reactive import reactive
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

class ChatApp(App):
    """Interface conversacional estilo gemini-cli"""
    
    CSS = """
    Screen {
        background: #282a36;
        color: #f8f8f2;
    }
    
    #chat-log {
        height: 1fr;
        border: solid #6272a4;
        margin: 1;
    }
    
    #input-area {
        height: 3;
        margin: 0 1 1 1;
    }
    
    Input {
        border: solid #bd93f9;
    }
    
    Input:focus {
        border: solid #50fa7b;
    }
    """
    
    def compose(self) -> ComposeResult:
        # ASCII Art Header
        yield Static(self.get_ascii_logo(), id="header")
        
        # Chat Log
        yield RichLog(id="chat-log", highlight=True, markup=True)
        
        # Input Area
        with Horizontal(id="input-area"):
            yield Static("💬", classes="prompt-icon")
            yield Input(
                placeholder="Como posso ajudar? (/help para comandos)",
                id="chat-input"
            )
    
    def get_ascii_logo(self) -> str:
        """ASCII art responsivo baseado no terminal"""
        return """
╔═══════════════════════════════════════╗
║  ██████╗██╗     ██╗    ████████╗ ██████╗ ║
║ ██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗║
║ ██║     ██║     ██║       ██║   ██║   ██║║
║ ██║     ██║     ██║       ██║   ██║   ██║║
║ ╚██████╗███████╗██║       ██║   ╚██████╔╝║
║  ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝ ║
║                                         ║
║ 🛠️ CLI Tools v2.0 - Developer Toolkit   ║
╚═══════════════════════════════════════╝
        """
    
    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Processar comando/mensagem do usuário"""
        user_input = message.value.strip()
        if not user_input:
            return
            
        # Limpar input
        self.query_one("#chat-input", Input).value = ""
        
        # Adicionar mensagem do usuário ao log
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.write(f"[bold cyan]> {user_input}[/bold cyan]")
        
        # Processar comando
        await self.process_command(user_input)
    
    async def process_command(self, command: str) -> None:
        """Processar comandos slash ou conversação"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        if command.startswith('/'):
            await self.handle_slash_command(command)
        else:
            await self.handle_conversation(command)
    
    async def handle_slash_command(self, command: str) -> None:
        """Processar comandos slash"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        parts = command.split()
        cmd = parts[0]
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
            await self.cmd_theme()
        elif cmd == '/help':
            await self.cmd_help()
        elif cmd == '/clear':
            chat_log.clear()
        else:
            chat_log.write(f"[red]❌ Comando desconhecido: {cmd}[/red]")
            chat_log.write("[yellow]💡 Digite /help para ver comandos disponíveis[/yellow]")
    
    async def cmd_search(self, args: list) -> None:
        """Comando /search"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        if not args:
            chat_log.write("[yellow]🔍 Uso: /search <termo de busca>[/yellow]")
            return
        
        query = " ".join(args)
        chat_log.write(f"[green]🔍 Buscando imagens: '{query}'[/green]")
        
        # Simular busca com progress
        with chat_log.capture_print():
            from rich.progress import Progress, SpinnerColumn, TextColumn
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=Console()
            ) as progress:
                task = progress.add_task("Buscando...", total=None)
                await asyncio.sleep(2)  # Simular API call
        
        chat_log.write("[green]✅ 5 imagens salvas em materials/imagens/[/green]")
    
    async def cmd_help(self) -> None:
        """Mostrar ajuda"""
        chat_log = self.query_one("#chat-log", RichLog)
        
        help_text = """
[bold cyan]🛠️ CLI Tools - Comandos Disponíveis[/bold cyan]

[bold yellow]Comandos Slash:[/bold yellow]
  [cyan]/search[/cyan] <termo>     - Buscar e baixar imagens
  [cyan]/figma[/cyan] <key>        - Extrair designs do Figma
  [cyan]/repo[/cyan] <url>         - Baixar repositório com IA
  [cyan]/config[/cyan]             - Configurar APIs
  [cyan]/status[/cyan]             - Status do sistema
  [cyan]/theme[/cyan]              - Alterar tema
  [cyan]/clear[/cyan]              - Limpar chat
  [cyan]/help[/cyan]               - Esta ajuda

[bold yellow]Conversação Natural:[/bold yellow]
  [green]"Preciso de imagens de escritório"[/green]
  [green]"Como configurar as APIs?"[/green]
  [green]"Baixar repo do tailwindcss"[/green]

[bold yellow]Atalhos:[/bold yellow]
  [magenta]Ctrl+C[/magenta]  - Sair
  [magenta]Tab[/magenta]     - Auto-complete
  [magenta]↑/↓[/magenta]     - Histórico
        """
        
        chat_log.write(help_text)
```

### **Sistema de Slash Commands**
```python
# cli_tools/commands/slash_processor.py
from typing import Dict, Callable, List
from dataclasses import dataclass
import asyncio

@dataclass
class SlashCommand:
    name: str
    description: str
    handler: Callable
    aliases: List[str] = None

class SlashCommandProcessor:
    """Processador de comandos slash estilo gemini-cli"""
    
    def __init__(self):
        self.commands: Dict[str, SlashCommand] = {}
        self.register_builtin_commands()
    
    def register_builtin_commands(self):
        """Registrar comandos built-in"""
        commands = [
            SlashCommand("search", "Buscar imagens", self.search_handler, ["s", "img"]),
            SlashCommand("figma", "Extrair designs", self.figma_handler, ["f", "design"]),
            SlashCommand("repo", "Baixar repositório", self.repo_handler, ["r", "git"]),
            SlashCommand("config", "Configurar APIs", self.config_handler, ["cfg"]),
            SlashCommand("status", "Status do sistema", self.status_handler, ["st"]),
            SlashCommand("theme", "Alterar tema", self.theme_handler, ["t"]),
            SlashCommand("help", "Mostrar ajuda", self.help_handler, ["h", "?"]),
            SlashCommand("clear", "Limpar tela", self.clear_handler, ["cls"]),
        ]
        
        for cmd in commands:
            self.register_command(cmd)
    
    def register_command(self, command: SlashCommand):
        """Registrar comando"""
        self.commands[command.name] = command
        
        # Registrar aliases
        if command.aliases:
            for alias in command.aliases:
                self.commands[alias] = command
    
    async def process(self, command_line: str) -> str:
        """Processar linha de comando"""
        if not command_line.startswith('/'):
            return await self.handle_natural_language(command_line)
        
        parts = command_line[1:].split()
        if not parts:
            return "❌ Comando vazio"
        
        cmd_name = parts[0]
        args = parts[1:]
        
        if cmd_name not in self.commands:
            return f"❌ Comando desconhecido: /{cmd_name}\n💡 Digite /help para ver comandos"
        
        command = self.commands[cmd_name]
        return await command.handler(args)
    
    async def search_handler(self, args: List[str]) -> str:
        """Handler para /search"""
        if not args:
            return "🔍 Uso: /search <termo de busca>"
        
        query = " ".join(args)
        # Integrar com sistema existente
        from ..core.pexels_api import buscar_imagens
        
        try:
            resultados = await buscar_imagens(query, 5)
            return f"✅ {len(resultados)} imagens de '{query}' salvas!"
        except Exception as e:
            return f"❌ Erro na busca: {str(e)}"
    
    async def handle_natural_language(self, text: str) -> str:
        """Processar linguagem natural com IA"""
        # Integrar com Gemini para interpretar intenção
        intent = await self.detect_intent(text)
        
        if "imagem" in text.lower() or "foto" in text.lower():
            # Extrair termo de busca
            query = self.extract_search_term(text)
            return await self.search_handler([query])
        elif "figma" in text.lower():
            return "🎨 Para extrair do Figma, use: /figma <chave_do_arquivo>"
        elif "repo" in text.lower() or "repositório" in text.lower():
            return "📦 Para baixar repositório, use: /repo <url_do_repo>"
        else:
            return "💡 Não entendi. Digite /help para ver comandos disponíveis."
```

### **Auto-Complete Inteligente**
```python
# cli_tools/ui/autocomplete.py
from textual.widgets import Input
from typing import List, Optional
import os

class SmartInput(Input):
    """Input com auto-complete inteligente"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.suggestions: List[str] = []
        self.current_suggestion = 0
    
    def get_suggestions(self, text: str) -> List[str]:
        """Obter sugestões baseadas no contexto"""
        suggestions = []
        
        if text.startswith('/'):
            # Sugestões de comandos slash
            commands = [
                "/search", "/figma", "/repo", "/config", 
                "/status", "/theme", "/help", "/clear"
            ]
            suggestions = [cmd for cmd in commands if cmd.startswith(text)]
        
        elif text.startswith('/search '):
            # Sugestões de termos de busca populares
            popular_terms = [
                "escritório moderno", "natureza", "tecnologia",
                "design minimalista", "workspace", "ui design"
            ]
            query = text[8:]  # Remove "/search "
            suggestions = [f"/search {term}" for term in popular_terms 
                          if term.startswith(query)]
        
        elif text.startswith('/repo '):
            # Sugestões de repositórios populares
            popular_repos = [
                "tailwindcss/tailwindcss", "facebook/react",
                "microsoft/vscode", "vercel/next.js"
            ]
            repo = text[6:]  # Remove "/repo "
            suggestions = [f"/repo {r}" for r in popular_repos 
                          if r.startswith(repo)]
        
        return suggestions[:5]  # Máximo 5 sugestões
```

### **Tema Dracula Nativo**
```python
# cli_tools/themes/dracula.py
from rich.theme import Theme
from rich.style import Style

DRACULA_THEME = Theme({
    "background": Style(bgcolor="#282a36"),
    "foreground": Style(color="#f8f8f2"),
    "purple": Style(color="#bd93f9", bold=True),
    "cyan": Style(color="#8be9fd"),
    "green": Style(color="#50fa7b"),
    "orange": Style(color="#ffb86c"),
    "red": Style(color="#ff5555"),
    "yellow": Style(color="#f1fa8c"),
    "comment": Style(color="#6272a4"),
    "user_input": Style(color="#8be9fd", bold=True),
    "system_response": Style(color="#50fa7b"),
    "error": Style(color="#ff5555", bold=True),
    "warning": Style(color="#ffb86c"),
    "success": Style(color="#50fa7b", bold=True),
    "info": Style(color="#8be9fd"),
})

DRACULA_CSS = """
Screen {
    background: #282a36;
    color: #f8f8f2;
}

Input {
    background: #44475a;
    color: #f8f8f2;
    border: solid #6272a4;
}

Input:focus {
    border: solid #bd93f9;
}

RichLog {
    background: #282a36;
    color: #f8f8f2;
    border: solid #6272a4;
}

Static {
    color: #f8f8f2;
}

.user-message {
    color: #8be9fd;
}

.system-message {
    color: #50fa7b;
}

.error-message {
    color: #ff5555;
}

.warning-message {
    color: #ffb86c;
}
"""
```

---

## 🚀 **IMPLEMENTAÇÃO FASEADA**

### **FASE 1: CORE CONVERSACIONAL** 💬
- [ ] Interface chat com Textual + Rich
- [ ] Processador de slash commands
- [ ] ASCII art responsivo
- [ ] Tema Dracula nativo
- [ ] Input inteligente com histórico

### **FASE 2: COMANDOS MODERNOS** ⚡
- [ ] /search com interface rica
- [ ] /figma com preview
- [ ] /repo com seleção IA
- [ ] /config com dialogs
- [ ] /status com métricas live

### **FASE 3: IA CONVERSACIONAL** 🤖
- [ ] Interpretação de linguagem natural
- [ ] Auto-complete contextual
- [ ] Sugestões inteligentes
- [ ] Histórico com busca
- [ ] Context awareness

### **FASE 4: POLISH & FEATURES** ✨
- [ ] Animações suaves
- [ ] Progress indicators
- [ ] Error handling gracioso
- [ ] Plugin system
- [ ] Update notifications

---

## 🎯 **VANTAGENS DA STACK PYTHON**

### **✅ Mantém Familiaridade**
- **Click** já dominado
- **Rich/Textual** já estudado
- **Python** ecosystem conhecido
- **Async/await** nativo

### **✅ Bibliotecas Poderosas**
- **Rich**: Styling e formatação
- **Textual**: TUI framework moderno
- **Asyncio**: Operações assíncronas
- **Pydantic**: Validação de dados
- **Httpx**: HTTP client moderno

### **✅ Performance Adequada**
- **Startup rápido** com imports lazy
- **Memory efficient** com generators
- **Async I/O** para APIs
- **Caching** inteligente

---

## 🎉 **RESULTADO ESPERADO**

**CLI Tools v2.0 Python** terá:

✨ **Interface conversacional** como gemini-cli  
🐍 **Stack Python** familiar e poderosa  
🎨 **Tema Dracula** nativo e elegante  
💬 **Slash commands** intuitivos  
🤖 **IA conversacional** integrada  
⚡ **Performance** excelente  
🔧 **Extensibilidade** total  

**"O melhor dos dois mundos: UX do gemini-cli + Power do Python!"** 🚀
