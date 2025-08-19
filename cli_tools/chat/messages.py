"""
Textos informativos e curtos para CLI Tools
Inspirado no gemini-cli em português
"""

# Mensagens de boas-vindas
WELCOME_MESSAGES = {
    "full": """[dim]💡 Como usar:[/dim]
[dim]  • Digite comandos: /search, /figma, /repo[/dim]
[dim]  • Ou fale naturalmente: "Preciso de imagens de escritório"[/dim]
[dim]  • Ctrl+C para sair, /help para ajuda completa[/dim]""",
    
    "compact": """[dim]💡 Digite comandos ou fale naturalmente[/dim]
[dim]  • /search, /figma, /repo ou Ctrl+C para sair[/dim]""",
    
    "minimal": """[dim]💡 Digite /help para comandos[/dim]"""
}

# Placeholders para input
INPUT_PLACEHOLDERS = {
    "full": "Como posso ajudar? Digite comandos ou fale naturalmente...",
    "compact": "Digite comandos ou pergunte algo...",
    "minimal": "Digite aqui..."
}

# Comandos slash com descrições curtas
SLASH_COMMANDS = {
    "/search": {
        "desc": "Buscar imagens",
        "usage": "/search <termo>",
        "example": "/search escritório moderno",
        "help": "Busca e baixa imagens do Pexels"
    },
    "/figma": {
        "desc": "Extrair designs",
        "usage": "/figma <chave>", 
        "example": "/figma abc123def",
        "help": "Extrai designs e assets do Figma"
    },
    "/repo": {
        "desc": "Baixar repositório",
        "usage": "/repo <url>",
        "example": "/repo tailwindcss/tailwindcss", 
        "help": "Baixa repositório com seleção inteligente"
    },
    "/config": {
        "desc": "Configurar APIs",
        "usage": "/config",
        "example": "/config",
        "help": "Configura chaves das APIs"
    },
    "/status": {
        "desc": "Status do sistema", 
        "usage": "/status",
        "example": "/status",
        "help": "Mostra saúde das APIs e workspace"
    },
    "/theme": {
        "desc": "Alterar tema",
        "usage": "/theme [nome]",
        "example": "/theme dracula",
        "help": "Altera tema visual (dracula, light, auto)"
    },
    "/clear": {
        "desc": "Limpar chat",
        "usage": "/clear", 
        "example": "/clear",
        "help": "Limpa histórico do chat"
    },
    "/help": {
        "desc": "Mostrar ajuda",
        "usage": "/help [comando]",
        "example": "/help search",
        "help": "Mostra ajuda geral ou de comando específico"
    }
}

# Mensagens de status
STATUS_MESSAGES = {
    "searching": "🔍 Buscando imagens...",
    "downloading": "📥 Baixando arquivos...",
    "processing": "⚙️ Processando...",
    "configuring": "🔧 Configurando...",
    "analyzing": "🤖 Analisando com IA...",
    "extracting": "🎨 Extraindo designs...",
    "cloning": "📦 Clonando repositório...",
    "success": "✅ Concluído!",
    "error": "❌ Erro:",
    "warning": "⚠️ Atenção:",
    "info": "ℹ️ Info:"
}

# Respostas para linguagem natural
NATURAL_RESPONSES = {
    "search_detected": "🔍 Entendi! Vou buscar imagens para você.",
    "figma_detected": "🎨 Vou extrair os designs do Figma.",
    "repo_detected": "📦 Vou baixar o repositório.",
    "config_needed": "⚙️ Primeiro preciso configurar as APIs. Use /config",
    "unknown_intent": "🤔 Não entendi. Tente /help para ver comandos.",
    "missing_params": "📝 Preciso de mais informações. Exemplo:",
    "api_error": "🔌 Problema com a API. Verifique /status",
    "no_results": "🔍 Nenhum resultado encontrado.",
    "quota_exceeded": "📊 Limite de API atingido. Tente mais tarde."
}

# Mensagens de erro amigáveis
ERROR_MESSAGES = {
    "no_api_key": "🔑 API não configurada. Use /config para configurar",
    "invalid_figma_key": "🎨 Chave do Figma inválida. Verifique o formato",
    "invalid_repo_url": "📦 URL do repositório inválida",
    "network_error": "🌐 Erro de conexão. Verifique sua internet",
    "file_error": "📁 Erro ao salvar arquivo",
    "permission_error": "🔒 Sem permissão para escrever no diretório",
    "quota_error": "📊 Limite de API excedido",
    "timeout_error": "⏱️ Operação demorou muito. Tente novamente"
}

# Dicas contextuais
TIPS = {
    "first_time": "💡 Primeira vez? Tente: /search natureza",
    "no_config": "💡 Configure as APIs com /config para começar",
    "empty_search": "💡 Exemplo: /search escritório moderno",
    "figma_help": "💡 Cole a URL do Figma ou apenas a chave do arquivo",
    "repo_help": "💡 Use owner/repo ou URL completa do GitHub",
    "shortcuts": "💡 Atalhos: Ctrl+L (limpar), Ctrl+H (ajuda)"
}

def get_welcome_message(terminal_width: int) -> str:
    """Retorna mensagem de boas-vindas baseada no tamanho do terminal"""
    if terminal_width >= 80:
        return WELCOME_MESSAGES["full"]
    elif terminal_width >= 50:
        return WELCOME_MESSAGES["compact"] 
    else:
        return WELCOME_MESSAGES["minimal"]

def get_input_placeholder(terminal_width: int) -> str:
    """Retorna placeholder do input baseado no tamanho do terminal"""
    if terminal_width >= 80:
        return INPUT_PLACEHOLDERS["full"]
    elif terminal_width >= 50:
        return INPUT_PLACEHOLDERS["compact"]
    else:
        return INPUT_PLACEHOLDERS["minimal"]

def get_help_text(terminal_width: int, command: str = None) -> str:
    """Gera texto de ajuda responsivo"""
    
    if command and command.startswith('/'):
        # Ajuda específica de comando
        if command in SLASH_COMMANDS:
            cmd_info = SLASH_COMMANDS[command]
            return f"""[bold yellow]{command}[/bold yellow] - {cmd_info['desc']}

[bold]Uso:[/bold] {cmd_info['usage']}
[bold]Exemplo:[/bold] {cmd_info['example']}

{cmd_info['help']}"""
        else:
            return f"❌ Comando {command} não encontrado"
    
    # Ajuda geral
    if terminal_width >= 80:
        return get_full_help()
    elif terminal_width >= 50:
        return get_compact_help()
    else:
        return get_minimal_help()

def get_full_help() -> str:
    """Ajuda completa para terminais grandes"""
    return """[bold cyan]🛠️ CLI Tools - Comandos Disponíveis[/bold cyan]

[bold yellow]Comandos Slash:[/bold yellow]
  [purple]/search[/purple] <termo>     - Buscar e baixar imagens
  [purple]/figma[/purple] <chave>      - Extrair designs do Figma
  [purple]/repo[/purple] <url>         - Baixar repositório com IA
  [purple]/config[/purple]             - Configurar APIs
  [purple]/status[/purple]             - Status do sistema
  [purple]/theme[/purple] [nome]       - Alterar tema visual
  [purple]/clear[/purple]              - Limpar chat
  [purple]/help[/purple] [comando]     - Ajuda específica

[bold yellow]Linguagem Natural:[/bold yellow]
  [green]"Preciso de imagens de escritório moderno"[/green]
  [green]"Como configurar as APIs?"[/green]
  [green]"Baixar repositório do tailwindcss"[/green]
  [green]"Qual o status do sistema?"[/green]

[bold yellow]Atalhos de Teclado:[/bold yellow]
  [cyan]Ctrl+C[/cyan]  - Sair do programa
  [cyan]Ctrl+L[/cyan]  - Limpar chat
  [cyan]Ctrl+H[/cyan]  - Mostrar esta ajuda
  [cyan]↑/↓[/cyan]     - Navegar histórico
  [cyan]Tab[/cyan]     - Auto-completar

[bold yellow]Exemplos Rápidos:[/bold yellow]
  [dim]/search "escritório moderno" → Busca 5 imagens[/dim]
  [dim]/figma abc123def → Extrai designs[/dim]
  [dim]/repo tailwindcss/tailwindcss → Baixa repo[/dim]"""

def get_compact_help() -> str:
    """Ajuda compacta para terminais médios"""
    return """[bold cyan]🛠️ CLI Tools - Comandos[/bold cyan]

[bold yellow]Comandos:[/bold yellow]
  [purple]/search[/purple] <termo>  - Buscar imagens
  [purple]/figma[/purple] <chave>   - Extrair designs
  [purple]/repo[/purple] <url>      - Baixar repositório
  [purple]/config[/purple]          - Configurar APIs
  [purple]/status[/purple]          - Ver status
  [purple]/help[/purple]            - Esta ajuda

[bold yellow]Linguagem Natural:[/bold yellow]
  [green]"Preciso de imagens de natureza"[/green]
  [green]"Configurar APIs"[/green]

[bold yellow]Atalhos:[/bold yellow] Ctrl+C (sair), Ctrl+L (limpar)"""

def get_minimal_help() -> str:
    """Ajuda mínima para terminais pequenos"""
    return """[bold cyan]CLI Tools[/bold cyan]

[purple]/search[/purple] <termo>
[purple]/figma[/purple] <chave>
[purple]/repo[/purple] <url>
[purple]/config[/purple]
[purple]/status[/purple]

Ctrl+C para sair"""
