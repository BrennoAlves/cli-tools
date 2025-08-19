# 🤖👥 CLI Tools v2.0 - Arquitetura Híbrida

## 🎯 **DUAL MODE: HUMANOS + AGENTS**

### **🧠 DETECÇÃO AUTOMÁTICA DE CONTEXTO**

```python
# cli_tools/main.py
import sys
import os
from typing import Optional

def detect_usage_context() -> str:
    """Detectar se está sendo usado por humano ou agent"""
    
    # 1. Verificar se há argumentos (agent mode)
    if len(sys.argv) > 1:
        return "agent"
    
    # 2. Verificar variáveis de ambiente
    if os.getenv('CLI_TOOLS_AGENT_MODE'):
        return "agent"
    
    # 3. Verificar se está em TTY (terminal interativo)
    if not sys.stdin.isatty():
        return "agent"
    
    # 4. Verificar se está sendo chamado por script
    if os.getenv('_') and 'python' in os.getenv('_'):
        return "agent"
    
    # Default: modo humano
    return "human"

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """🛠️ CLI Tools - Dual Mode: Humanos + Agents"""
    
    usage_mode = detect_usage_context()
    
    if ctx.invoked_subcommand is None:
        if usage_mode == "human":
            # Modo conversacional para humanos
            launch_chat_interface()
        else:
            # Mostrar help para agents
            click.echo(ctx.get_help())
    
def launch_chat_interface():
    """Lançar interface conversacional"""
    from .chat_app import ChatApp
    app = ChatApp()
    app.run()
```

---

## 🤖 **MODO AGENT: COMANDOS ÚNICOS**

### **Mantém Compatibilidade Total**
```bash
# Agents continuam usando comandos diretos
cli-tools search "escritório moderno" -n 5
cli-tools figma "abc123def" -n 3 --format png  
cli-tools repo "tailwindcss/tailwindcss" -q "componentes"
cli-tools status
cli-tools config --pexels-key "xxx"

# Modo não-interativo para scripts
echo "escritório moderno" | cli-tools search --stdin -n 10
cli-tools search "natureza" --json | jq '.urls[]'
```

### **API Programática**
```python
# Para agents Python
from cli_tools import CLITools

client = CLITools()
results = await client.search("escritório moderno", count=5)
designs = await client.figma("abc123def", format="png")
repo = await client.repo("tailwindcss/tailwindcss", query="componentes")
```

---

## 👥 **MODO HUMAN: INTERFACE CONVERSACIONAL**

### **Entrada Única Intuitiva**
```bash
# Humanos usam entrada única
cli-tools

# Abre interface chat
╔═══════════════════════════════════════╗
║ 🛠️ CLI Tools v2.0 - Developer Toolkit ║
╚═══════════════════════════════════════╝

💬 Como posso ajudar? Digite sua mensagem ou use comandos:

> /search escritório moderno
> Preciso de imagens de natureza
> /figma abc123def
> Como configurar as APIs?
> _
```

### **Processamento Inteligente**
```python
# cli_tools/chat_processor.py
class ChatProcessor:
    """Processador híbrido de comandos"""
    
    async def process_input(self, user_input: str) -> str:
        """Processar entrada do usuário"""
        
        # 1. Comandos slash diretos
        if user_input.startswith('/'):
            return await self.handle_slash_command(user_input)
        
        # 2. Linguagem natural com IA
        intent = await self.detect_intent(user_input)
        return await self.handle_natural_language(user_input, intent)
    
    async def detect_intent(self, text: str) -> dict:
        """Detectar intenção usando IA"""
        prompts = {
            "search": ["imagem", "foto", "buscar", "encontrar", "picture"],
            "figma": ["figma", "design", "ui", "interface"],
            "repo": ["repositório", "repo", "código", "github", "baixar"],
            "config": ["configurar", "api", "chave", "token", "setup"],
            "status": ["status", "estado", "saúde", "health", "info"]
        }
        
        text_lower = text.lower()
        
        for intent, keywords in prompts.items():
            if any(keyword in text_lower for keyword in keywords):
                return {
                    "intent": intent,
                    "confidence": 0.8,
                    "extracted_params": self.extract_params(text, intent)
                }
        
        return {"intent": "unknown", "confidence": 0.0}
    
    def extract_params(self, text: str, intent: str) -> dict:
        """Extrair parâmetros da linguagem natural"""
        if intent == "search":
            # Extrair termo de busca
            patterns = [
                r"imagens? de (.+)",
                r"fotos? de (.+)", 
                r"buscar (.+)",
                r"encontrar (.+)"
            ]
            
            import re
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return {"query": match.group(1).strip()}
        
        return {}
```

---

## 🔄 **IMPLEMENTAÇÃO DUAL**

### **Estrutura Modular**
```
cli_tools/
├── main.py              # Entry point com detecção de modo
├── commands/            # Comandos tradicionais (agents)
│   ├── search.py
│   ├── figma.py
│   ├── repo.py
│   └── status.py
├── chat/                # Interface conversacional (humanos)
│   ├── app.py
│   ├── processor.py
│   ├── slash_commands.py
│   └── ai_interpreter.py
├── core/                # Lógica compartilhada
│   ├── pexels_api.py
│   ├── figma_api.py
│   └── gemini_api.py
└── themes/              # Temas visuais
    └── dracula.py
```

### **Comando Principal Híbrido**
```python
# cli_tools/main.py
@click.group(invoke_without_command=True)
@click.option('--chat', is_flag=True, help='Forçar modo chat')
@click.option('--agent', is_flag=True, help='Forçar modo agent')
@click.pass_context
def cli(ctx, chat, agent):
    """🛠️ CLI Tools - Dual Mode Interface"""
    
    # Forçar modo específico se solicitado
    if chat:
        launch_chat_interface()
        return
    
    if agent or ctx.invoked_subcommand:
        # Modo agent - continuar com subcomandos
        return
    
    # Auto-detectar modo
    usage_mode = detect_usage_context()
    
    if usage_mode == "human":
        launch_chat_interface()
    else:
        click.echo(ctx.get_help())

# Manter comandos existentes para agents
@cli.command()
@click.argument('consulta')
@click.option('--count', '-c', '-n', default=3)
@click.option('--orientation', type=click.Choice(['landscape', 'portrait', 'square']))
def search(consulta, count, orientation):
    """🖼️ Buscar e baixar imagens (Agent Mode)"""
    # Implementação existente mantida
    pass

@cli.command()
@click.argument('chave_arquivo')
@click.option('--max', '-n', default=3)
@click.option('--format', type=click.Choice(['png', 'jpg', 'svg']))
def figma(chave_arquivo, max, format):
    """🎨 Extrair designs do Figma (Agent Mode)"""
    # Implementação existente mantida
    pass

# ... outros comandos mantidos
```

### **Interface Chat Moderna**
```python
# cli_tools/chat/app.py
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Input, RichLog, Static
from rich.console import Console
from rich.panel import Panel

class ChatApp(App):
    """Interface conversacional moderna"""
    
    CSS = """
    Screen {
        background: #282a36;
        color: #f8f8f2;
    }
    
    #header {
        height: 8;
        content-align: center middle;
        text-style: bold;
    }
    
    #chat-log {
        height: 1fr;
        border: solid #6272a4;
        margin: 1;
        padding: 1;
    }
    
    #input-container {
        height: 3;
        margin: 0 1 1 1;
    }
    
    Input {
        border: solid #bd93f9;
        background: #44475a;
        color: #f8f8f2;
    }
    
    Input:focus {
        border: solid #50fa7b;
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
    """
    
    BINDINGS = [
        ("ctrl+c", "quit", "Sair"),
        ("ctrl+l", "clear_chat", "Limpar"),
        ("ctrl+h", "show_help", "Ajuda"),
    ]
    
    def compose(self) -> ComposeResult:
        # Header com ASCII art
        yield Static(self.get_header(), id="header")
        
        # Chat log
        yield RichLog(
            id="chat-log",
            highlight=True,
            markup=True,
            auto_scroll=True
        )
        
        # Input area
        with Horizontal(id="input-container"):
            yield Static("💬 ", classes="prompt-icon")
            yield Input(
                placeholder="Como posso ajudar? (/help para comandos)",
                id="chat-input"
            )
    
    def get_header(self) -> str:
        """Header com ASCII art responsivo"""
        return """
[bold purple]╔═══════════════════════════════════════╗[/bold purple]
[bold purple]║[/bold purple] [bold cyan]🛠️ CLI Tools v2.0 - Developer Toolkit[/bold cyan] [bold purple]║[/bold purple]
[bold purple]╚═══════════════════════════════════════╝[/bold purple]

[dim]Modo Conversacional - Digite comandos ou fale naturalmente[/dim]
        """
    
    def on_mount(self) -> None:
        """Inicialização"""
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.write("[dim]💡 Dicas:[/dim]")
        chat_log.write("[dim]  • Use /search, /figma, /repo para comandos diretos[/dim]")
        chat_log.write("[dim]  • Ou fale naturalmente: 'Preciso de imagens de escritório'[/dim]")
        chat_log.write("[dim]  • Ctrl+C para sair, Ctrl+L para limpar[/dim]")
        chat_log.write("")
        
        # Focar no input
        self.query_one("#chat-input", Input).focus()
    
    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Processar entrada do usuário"""
        user_input = message.value.strip()
        if not user_input:
            return
        
        # Limpar input
        input_widget = self.query_one("#chat-input", Input)
        input_widget.value = ""
        
        # Adicionar mensagem do usuário
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.write(f"[bold cyan]> {user_input}[/bold cyan]")
        
        # Processar comando
        from .processor import ChatProcessor
        processor = ChatProcessor()
        
        try:
            response = await processor.process_input(user_input)
            chat_log.write(f"[green]{response}[/green]")
        except Exception as e:
            chat_log.write(f"[red]❌ Erro: {str(e)}[/red]")
        
        chat_log.write("")  # Linha em branco
    
    def action_clear_chat(self) -> None:
        """Limpar chat"""
        self.query_one("#chat-log", RichLog).clear()
        self.on_mount()  # Reexibir dicas
    
    def action_show_help(self) -> None:
        """Mostrar ajuda"""
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.write("""
[bold yellow]🛠️ CLI Tools - Comandos Disponíveis[/bold yellow]

[bold cyan]Comandos Slash:[/bold cyan]
  [purple]/search[/purple] <termo>     - Buscar e baixar imagens
  [purple]/figma[/purple] <key>        - Extrair designs do Figma  
  [purple]/repo[/purple] <url>         - Baixar repositório com IA
  [purple]/config[/purple]             - Configurar APIs
  [purple]/status[/purple]             - Status do sistema
  [purple]/clear[/purple]              - Limpar chat
  [purple]/help[/purple]               - Esta ajuda

[bold cyan]Linguagem Natural:[/bold cyan]
  [green]"Preciso de imagens de escritório moderno"[/green]
  [green]"Como configurar as APIs?"[/green]
  [green]"Baixar repositório do tailwindcss"[/green]
  [green]"Qual o status do sistema?"[/green]

[bold cyan]Atalhos:[/bold cyan]
  [yellow]Ctrl+C[/yellow]  - Sair
  [yellow]Ctrl+L[/yellow]  - Limpar chat
  [yellow]Ctrl+H[/yellow]  - Esta ajuda
        """)
```

---

## 🎯 **VANTAGENS DA ARQUITETURA HÍBRIDA**

### **✅ Para Agents:**
- **Comandos únicos** mantidos
- **API programática** disponível
- **Saída JSON** para parsing
- **Modo não-interativo** para scripts
- **Compatibilidade total** com versão atual

### **✅ Para Humanos:**
- **Interface conversacional** moderna
- **Linguagem natural** com IA
- **Slash commands** intuitivos
- **Auto-complete** contextual
- **Tema Dracula** nativo

### **✅ Para Ambos:**
- **Detecção automática** de contexto
- **Core compartilhado** (sem duplicação)
- **Performance otimizada** para cada uso
- **Manutenção simplificada**

---

## 🚀 **IMPLEMENTAÇÃO**

**Posso prosseguir implementando esta arquitetura híbrida que atende perfeitamente tanto humanos quanto agents? ✅/❌**

A solução mantém **100% de compatibilidade** para agents enquanto oferece uma **experiência moderna** para humanos! 🤖👥
