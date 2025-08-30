#!/bin/bash

# CLI Tools v2.0 - Instalação Nativa Global
set -e

echo "🚀 CLI Tools v2.0 - Instalação Nativa"
echo "====================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale python3 primeiro."
    exit 1
fi

# Instalar pipx se não existir (recomendado para CLIs)
if ! command -v pipx &> /dev/null; then
    echo "📦 Instalando pipx (gerenciador de CLIs Python)..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y pipx
    elif command -v brew &> /dev/null; then
        brew install pipx
    else
        python3 -m pip install --user pipx
    fi
    pipx ensurepath
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "📦 Instalando CLI Tools com pipx..."
pipx install .

# Criar diretórios de dados no home do usuário
echo "📁 Criando estrutura de dados..."
mkdir -p ~/.local/share/cli-tools/{materials/{imagens,figma,repos},data/cache}

# Verificar instalação
echo "✅ Verificando instalação..."
if command -v cli-tools &> /dev/null; then
    echo "✅ Instalação concluída com sucesso!"
    echo ""
    echo "🎯 Para usar em qualquer lugar:"
    echo "   cli-tools ui"
    echo "   cli-tools search 'office desk' -c 1"
    echo "   cli-tools figma AbCdEfGh123 -f png"
    echo "   cli-tools repo user/repo -q 'components'"
    echo "   cli-tools status"
    echo ""
    echo "📋 Teste agora:"
    cli-tools --help
else
    echo "❌ Comando cli-tools não encontrado."
    echo "   Reinicie o terminal ou execute: source ~/.bashrc"
    exit 1
fi
