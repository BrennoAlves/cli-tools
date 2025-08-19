#!/bin/bash

# 🛠️ CLI Tools - Script de Instalação Automática
# Instala cli-tools em sistemas Linux de forma simples e rápida

set -e  # Parar em caso de erro

echo "🛠️ CLI Tools - Instalação Automática"
echo "======================================"
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "💡 Instale Python 3 primeiro:"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "   Arch:          sudo pacman -S python python-pip"
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip não encontrado!"
    echo "💡 Instale pip primeiro:"
    echo "   Ubuntu/Debian: sudo apt install python3-pip"
    exit 1
fi

# Usar pip3 se disponível, senão pip
PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

echo "✅ Python $(python3 --version) encontrado"
echo "✅ pip encontrado"
echo

# Verificar se já está instalado
if command -v cli-tools &> /dev/null; then
    echo "⚠️  cli-tools já está instalado!"
    echo "🔄 Atualizando para versão mais recente..."
    echo
fi

# Instalar dependências
echo "📦 Instalando dependências..."
$PIP_CMD install --user click requests rich

# Instalar cli-tools
echo "🚀 Instalando cli-tools..."
$PIP_CMD install --user -e .

# Verificar instalação
echo
echo "🧪 Testando instalação..."

# Verificar se o comando está no PATH
if ! command -v cli-tools &> /dev/null; then
    echo "⚠️  Comando cli-tools não encontrado no PATH"
    echo "💡 Adicione ~/.local/bin ao seu PATH:"
    echo "   echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.bashrc"
    echo "   source ~/.bashrc"
    echo
    echo "🔄 Ou execute diretamente:"
    echo "   ~/.local/bin/cli-tools --version"
else
    # Testar comando
    if cli-tools --version &> /dev/null; then
        echo "✅ Instalação concluída com sucesso!"
        echo
        echo "🎉 cli-tools está pronto para uso!"
        echo
        echo "📋 Próximos passos:"
        echo "   1. Configure suas APIs: cli-tools config"
        echo "   2. Execute setup inicial: cli-tools setup"
        echo "   3. Veja a ajuda: cli-tools help"
        echo
        echo "🚀 Exemplo de uso:"
        echo "   cli-tools search \"escritório\" --count 3"
    else
        echo "❌ Erro na instalação - comando não funciona"
        exit 1
    fi
fi
