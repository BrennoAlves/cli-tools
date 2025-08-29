#!/bin/bash
# CLI Tools - Script de Instalação Automática
# Versão 2.0 - Estrutura reorganizada

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_color() {
    printf "${1}${2}${NC}\n"
}

# Header
print_color $PURPLE "
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗  ║
║ ██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝  ║
║ ██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗  ║
║ ╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║  ║
║  ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝  ║
║                                                                      ║
║                    🚀 Instalação Automática v2.0 🚀                  ║
╚══════════════════════════════════════════════════════════════════════╝
"

print_color $CYAN "🔧 Iniciando instalação do CLI Tools..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    print_color $RED "❌ Python 3 não encontrado. Instale Python 3.8+ primeiro."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_color $GREEN "✅ Python $PYTHON_VERSION encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    print_color $RED "❌ pip3 não encontrado. Instale pip primeiro."
    exit 1
fi

# Diretório de instalação
INSTALL_DIR="$HOME/.local/share/cli-tools"
BIN_DIR="$HOME/.local/bin"

print_color $BLUE "📁 Diretório de instalação: $INSTALL_DIR"

# Criar diretórios
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copiar arquivos
print_color $YELLOW "📦 Copiando arquivos..."
cp -r src "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"
cp README.md "$INSTALL_DIR/"

# Criar ambiente virtual
print_color $YELLOW "🐍 Criando ambiente virtual..."
cd "$INSTALL_DIR"
python3 -m venv venv

# Ativar ambiente virtual e instalar dependências
print_color $YELLOW "📚 Instalando dependências..."
source venv/bin/activate
pip install -r requirements.txt

# Criar wrapper executável
print_color $YELLOW "🔗 Criando comando cli-tools..."
cat > "$BIN_DIR/cli-tools" << 'EOF'
#!/bin/bash
# CLI Tools - Comando Principal

# Preservar diretório atual
USER_PWD="$(pwd)"
export USER_PWD

# Diretório de instalação
CLI_TOOLS_DIR="$HOME/.local/share/cli-tools"

# Ativar ambiente virtual e executar
cd "$CLI_TOOLS_DIR"
source venv/bin/activate
export PYTHONPATH="$CLI_TOOLS_DIR:$PYTHONPATH"
python3 -m src.main "$@"
EOF

chmod +x "$BIN_DIR/cli-tools"

# Verificar se ~/.local/bin está no PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    print_color $YELLOW "⚠️  Adicionando ~/.local/bin ao PATH..."
    
    # Detectar shell
    if [[ $SHELL == *"zsh"* ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ $SHELL == *"fish"* ]]; then
        SHELL_RC="$HOME/.config/fish/config.fish"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
    
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    export PATH="$HOME/.local/bin:$PATH"
    
    print_color $GREEN "✅ PATH atualizado em $SHELL_RC"
fi

# Criar diretório de configuração
CONFIG_DIR="$HOME/.cli-tools"
mkdir -p "$CONFIG_DIR"

# Testar instalação
print_color $YELLOW "🧪 Testando instalação..."
if "$BIN_DIR/cli-tools" --version &> /dev/null; then
    print_color $GREEN "✅ CLI Tools instalado com sucesso!"
else
    print_color $RED "❌ Erro na instalação. Verifique os logs acima."
    exit 1
fi

# Sucesso
print_color $GREEN "
🎉 Instalação concluída com sucesso!

📋 Próximos passos:
1. Reinicie seu terminal ou execute: source ~/.bashrc
2. Configure suas APIs: cli-tools config --interactive
3. Teste o sistema: cli-tools status
4. Veja a ajuda: cli-tools --help

🚀 Comandos disponíveis:
  cli-tools search \"natureza\" -n 5    # Buscar imagens
  cli-tools figma abc123def            # Extrair Figma
  cli-tools repo owner/repo            # Baixar repositório
  cli-tools ui                         # Interface interativa
  cli-tools status                     # Status do sistema

📚 Documentação completa em: ~/.local/share/cli-tools/README.md
"

print_color $PURPLE "Obrigado por usar CLI Tools! 🛠️"
