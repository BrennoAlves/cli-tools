#!/bin/bash

# 🛠️ CLI Tools - Instalação Interativa v1.1.0
# Script único de instalação completa e interativa

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para print colorido
print_color() {
    printf "${1}${2}${NC}\n"
}

# Header
clear
print_color $CYAN "🛠️  CLI TOOLS v1.1.0 - INSTALAÇÃO INTERATIVA"
print_color $CYAN "================================================"
echo ""
print_color $BLUE "Kit de ferramentas para desenvolvedores com IA integrada"
echo ""

# Verificar Python
print_color $YELLOW "🔍 Verificando requisitos..."
if ! command -v python3 &> /dev/null; then
    print_color $RED "❌ Python 3 não encontrado. Instale Python 3.7+ primeiro."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_color $GREEN "✅ Python $PYTHON_VERSION encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    print_color $RED "❌ pip3 não encontrado. Instale pip primeiro."
    exit 1
fi
print_color $GREEN "✅ pip3 encontrado"

# Instalar dependências
print_color $YELLOW "📦 Instalando dependências..."
pip3 install -r requirements.txt --quiet --user
if [ $? -eq 0 ]; then
    print_color $GREEN "✅ Dependências instaladas"
else
    print_color $RED "❌ Erro ao instalar dependências"
    exit 1
fi

# Configurar comando global
print_color $YELLOW "🔧 Configurando comando global..."

# Criar script wrapper
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

# Copiar arquivos (excluindo .git)
SHARE_DIR="$HOME/.local/share/cli-tools"
mkdir -p "$SHARE_DIR"

# Copiar apenas arquivos necessários
cp -r cli_tools "$SHARE_DIR/"
cp requirements.txt "$SHARE_DIR/"
cp setup.py "$SHARE_DIR/"
cp .env.example "$SHARE_DIR/"
cp README.md "$SHARE_DIR/"

print_color $GREEN "✅ Comando 'cli-tools' instalado em $INSTALL_DIR"

# Verificar PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    print_color $YELLOW "⚠️  Adicione $HOME/.local/bin ao seu PATH:"
    print_color $CYAN "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    print_color $CYAN "   # Adicione essa linha ao seu ~/.bashrc ou ~/.zshrc"
    echo ""
fi

# Configuração das APIs
print_color $YELLOW "🔑 Configuração das APIs"
echo ""
print_color $BLUE "Para usar todas as funcionalidades, você precisa configurar as chaves de API:"
echo ""
print_color $CYAN "1. 🖼️  Pexels API (busca de imagens)"
print_color $CYAN "   • Gratuita: https://www.pexels.com/api/"
print_color $CYAN "   • 200 requests/hora"
echo ""
print_color $CYAN "2. 🎨 Figma API (extração de designs)"
print_color $CYAN "   • Gratuita: https://www.figma.com/developers/api"
print_color $CYAN "   • Para seus próprios arquivos"
echo ""
print_color $CYAN "3. 🤖 Google Gemini (IA para seleção)"
print_color $CYAN "   • Gratuita: https://makersuite.google.com/app/apikey"
print_color $CYAN "   • 15 requests/minuto"
echo ""

read -p "Deseja configurar as APIs agora? [S/n]: " config_apis
config_apis=${config_apis:-S}

if [[ $config_apis =~ ^[Ss]$ ]]; then
    print_color $YELLOW "📝 Configurando APIs..."
    
    # Criar arquivo .env
    ENV_FILE="$SHARE_DIR/.env"
    cp "$SHARE_DIR/.env.example" "$ENV_FILE" 2>/dev/null || true
    
    echo "# 🔑 Configuração das Ferramentas CLI" > "$ENV_FILE"
    echo "# Configurado via instalação interativa" >> "$ENV_FILE"
    echo "" >> "$ENV_FILE"
    
    # Pexels
    echo ""
    print_color $BLUE "🖼️  Configurando Pexels API:"
    read -p "Cole sua chave da API Pexels (ou Enter para pular): " pexels_key
    if [ -n "$pexels_key" ]; then
        echo "PEXELS_API_KEY=$pexels_key" >> "$ENV_FILE"
        print_color $GREEN "✅ Pexels configurado"
    else
        echo "PEXELS_API_KEY=" >> "$ENV_FILE"
        print_color $YELLOW "⚠️  Pexels pulado"
    fi
    
    # Figma
    echo ""
    print_color $BLUE "🎨 Configurando Figma API:"
    read -p "Cole seu token da API Figma (ou Enter para pular): " figma_token
    if [ -n "$figma_token" ]; then
        echo "FIGMA_API_TOKEN=$figma_token" >> "$ENV_FILE"
        print_color $GREEN "✅ Figma configurado"
    else
        echo "FIGMA_API_TOKEN=" >> "$ENV_FILE"
        print_color $YELLOW "⚠️  Figma pulado"
    fi
    
    # Gemini
    echo ""
    print_color $BLUE "🤖 Configurando Google Gemini:"
    read -p "Cole sua chave da API Gemini (ou Enter para pular): " gemini_key
    if [ -n "$gemini_key" ]; then
        echo "GEMINI_API_KEY=$gemini_key" >> "$ENV_FILE"
        print_color $GREEN "✅ Gemini configurado"
    else
        echo "GEMINI_API_KEY=" >> "$ENV_FILE"
        print_color $YELLOW "⚠️  Gemini pulado"
    fi
    
    # Configurações opcionais
    echo "" >> "$ENV_FILE"
    echo "# Configuração Opcional" >> "$ENV_FILE"
    echo "CLI_TOOLS_VERSION=1.1.0" >> "$ENV_FILE"
    echo "DEFAULT_TIMEOUT=30" >> "$ENV_FILE"
    echo "DOWNLOAD_TIMEOUT=120" >> "$ENV_FILE"
    echo "MAX_RETRIES=3" >> "$ENV_FILE"
    
    print_color $GREEN "✅ Arquivo .env criado em $ENV_FILE"
fi

# Configuração da IA
echo ""
print_color $YELLOW "🤖 Configuração da IA"
echo ""
print_color $BLUE "A IA pode explicar suas decisões em diferentes níveis:"
print_color $CYAN "• Silencioso - Só mostrar resultado"
print_color $CYAN "• Básico - Resultado + resumo (recomendado)"
print_color $CYAN "• Detalhado - Mostrar processo completo"
print_color $CYAN "• Debug - Tudo + informações técnicas"
echo ""
print_color $PURPLE "💡 Interface moderna com navegação por setas (↑↓) disponível!"
echo ""

read -p "Deseja configurar o comportamento da IA agora? [S/n]: " config_ia
config_ia=${config_ia:-S}

if [[ $config_ia =~ ^[Ss]$ ]]; then
    cd "$SHARE_DIR"
    python3 -m cli_tools.main ai-config --interactive
fi

# Teste final
echo ""
print_color $YELLOW "🧪 Testando instalação..."
cd "$SHARE_DIR"

if python3 -m cli_tools.main --version &> /dev/null; then
    print_color $GREEN "✅ CLI Tools instalado com sucesso!"
else
    print_color $RED "❌ Erro na instalação"
    exit 1
fi

# Finalização
echo ""
print_color $GREEN "🎉 INSTALAÇÃO CONCLUÍDA!"
print_color $CYAN "================================================"
echo ""
print_color $BLUE "Comandos disponíveis:"
print_color $CYAN "  cli-tools --help           # Ver todos os comandos"
print_color $CYAN "  cli-tools status           # Status do sistema"
print_color $CYAN "  cli-tools search \"logo\" -n 3  # Buscar imagens"
print_color $CYAN "  cli-tools repo user/repo -q \"CSS\"  # Baixar repo com IA"
print_color $CYAN "  cli-tools ai-config --show # Ver config da IA"
echo ""
print_color $BLUE "Exemplos práticos:"
print_color $CYAN "  cli-tools search \"escritório moderno\" --number 5"
print_color $CYAN "  cli-tools repo \"tailwindcss/tailwindcss\" -q \"componentes\""
print_color $CYAN "  cli-tools figma \"abc123\" -n 3 --format png"
echo ""
print_color $PURPLE "📚 Documentação: https://github.com/BrennoAlves/cli-tools"
print_color $PURPLE "🐛 Issues: https://github.com/BrennoAlves/cli-tools/issues"
echo ""
print_color $GREEN "Divirta-se desenvolvendo! 🚀"
