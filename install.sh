#!/bin/bash

# 🛠️ CLI Tools - Instalador Simples v2.0
# Instalador funcional sem interfaces complexas

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_color() {
    printf "${1}${2}${NC}\n"
}

print_color $CYAN "🛠️  CLI TOOLS - INSTALADOR SIMPLES"
print_color $CYAN "=================================="
echo ""

# 1. Verificar Python
print_color $YELLOW "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_color $RED "❌ Python 3 não encontrado"
    exit 1
fi
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_color $GREEN "✅ Python $PYTHON_VERSION"

# 2. Verificar pip
if ! command -v pip3 &> /dev/null; then
    print_color $RED "❌ pip3 não encontrado"
    exit 1
fi
print_color $GREEN "✅ pip3 encontrado"

# 3. Instalar dependências
print_color $YELLOW "📦 Instalando dependências..."
pip3 install click requests rich --user --quiet
print_color $GREEN "✅ Dependências instaladas"

# 4. Criar diretórios
print_color $YELLOW "📁 Criando estrutura..."
INSTALL_DIR="$HOME/.local/bin"
SHARE_DIR="$HOME/.local/share/cli-tools"
mkdir -p "$INSTALL_DIR"
mkdir -p "$SHARE_DIR"
print_color $GREEN "✅ Diretórios criados"

# 5. Copiar arquivos
print_color $YELLOW "📋 Copiando arquivos..."
cp -r cli_tools "$SHARE_DIR/"
cp requirements.txt "$SHARE_DIR/"
cp .env.example "$SHARE_DIR/"
cp README.md "$SHARE_DIR/" 2>/dev/null || true
print_color $GREEN "✅ Arquivos copiados"

# 6. Criar comando executável
print_color $YELLOW "🔧 Criando comando..."
cat > "$INSTALL_DIR/cli-tools" << 'EOF'
#!/bin/bash
# CLI Tools - Comando Principal

# Preservar diretório atual
USER_PWD="$(pwd)"
export USER_PWD

# Diretório de instalação
CLI_TOOLS_DIR="$HOME/.local/share/cli-tools"

# Executar
cd "$CLI_TOOLS_DIR"
export PYTHONPATH="$CLI_TOOLS_DIR:$PYTHONPATH"
python3 -m cli_tools.main "$@"
EOF

chmod +x "$INSTALL_DIR/cli-tools"
print_color $GREEN "✅ Comando criado"

# 7. Configurar PATH
print_color $YELLOW "🛤️  Configurando PATH..."
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    # Detectar shell
    if [ -n "$ZSH_VERSION" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        print_color $BLUE "📝 Adicionado ao ~/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        print_color $BLUE "📝 Adicionado ao ~/.bashrc"
    fi
    export PATH="$HOME/.local/bin:$PATH"
fi
print_color $GREEN "✅ PATH configurado"

# 8. Criar configuração básica
print_color $YELLOW "⚙️  Criando configuração..."
cat > "$SHARE_DIR/.env" << 'EOF'
# 🔑 CLI Tools - Configuração
# Configure suas chaves de API aqui

# APIs (configure conforme necessário)
PEXELS_API_KEY=
FIGMA_ACCESS_TOKEN=
GEMINI_API_KEY=

# Configurações
CLI_TOOLS_VERSION=1.1.0
DEFAULT_TIMEOUT=30
DOWNLOAD_TIMEOUT=120
MAX_RETRIES=3
AI_VERBOSITY=basic
EOF
print_color $GREEN "✅ Configuração criada"

# 9. Testar instalação
print_color $YELLOW "🧪 Testando..."
if "$INSTALL_DIR/cli-tools" --version &> /dev/null; then
    print_color $GREEN "✅ Teste passou!"
else
    print_color $RED "❌ Teste falhou"
    exit 1
fi

# 10. Finalização
echo ""
print_color $GREEN "🎉 INSTALAÇÃO CONCLUÍDA!"
print_color $CYAN "========================"
echo ""
print_color $BLUE "Comando instalado: cli-tools"
print_color $BLUE "Localização: $INSTALL_DIR/cli-tools"
print_color $BLUE "Configuração: $SHARE_DIR/.env"
echo ""
print_color $YELLOW "📋 Próximos passos:"
print_color $CYAN "1. Reinicie o terminal ou execute: source ~/.bashrc"
print_color $CYAN "2. Configure APIs em: $SHARE_DIR/.env"
print_color $CYAN "3. Teste: cli-tools --help"
echo ""
print_color $GREEN "✨ Pronto para usar!"
