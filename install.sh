#!/bin/bash

# 🛠️ CLI Tools - Instalação Simples v1.1.0

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_color() {
    printf "${1}${2}${NC}\n"
}

# Header
clear
print_color $BLUE "🛠️ CLI TOOLS v1.1.0 - INSTALAÇÃO SIMPLES"
print_color $BLUE "=========================================="
echo ""

# Verificar Python
print_color $YELLOW "🔍 Verificando requisitos..."
if ! command -v python3 &> /dev/null; then
    print_color $RED "❌ Python 3 não encontrado. Instale Python 3.7+ primeiro."
    exit 1
fi
print_color $GREEN "✅ Python encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    print_color $RED "❌ pip3 não encontrado. Instale pip primeiro."
    exit 1
fi
print_color $GREEN "✅ pip3 encontrado"

# Instalar dependências
print_color $YELLOW "📦 Instalando dependências..."
pip3 install -r requirements.txt --quiet --user
print_color $GREEN "✅ Dependências instaladas"

# Configurar comando global
print_color $YELLOW "🔧 Configurando comando global..."
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

CLI_SCRIPT="$INSTALL_DIR/cli-tools"
cat > "$CLI_SCRIPT" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
CLI_TOOLS_DIR="$SCRIPT_DIR/../share/cli-tools"

cd "$CLI_TOOLS_DIR"
export PYTHONPATH="$CLI_TOOLS_DIR:$PYTHONPATH"
python3 -m cli_tools.main "$@"
EOF

chmod +x "$CLI_SCRIPT"

# Copiar arquivos
SHARE_DIR="$HOME/.local/share/cli-tools"
mkdir -p "$SHARE_DIR"
cp -r . "$SHARE_DIR/"

print_color $GREEN "✅ Comando 'cli-tools' instalado"

# Verificar PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    print_color $YELLOW "⚠️  Adicione ao seu PATH:"
    print_color $BLUE "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

# Teste
print_color $YELLOW "🧪 Testando instalação..."
cd "$SHARE_DIR"
if python3 -m cli_tools.main --version &> /dev/null; then
    print_color $GREEN "✅ Instalação concluída!"
else
    print_color $RED "❌ Erro na instalação"
    exit 1
fi

echo ""
print_color $GREEN "🎉 PRONTO PARA USAR!"
print_color $BLUE "Comandos:"
print_color $BLUE "  cli-tools status"
print_color $BLUE "  cli-tools search \"query\" -n 3"
print_color $BLUE "  cli-tools config  # Para configurar APIs"
echo ""
