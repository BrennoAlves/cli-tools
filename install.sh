#!/bin/bash

# CLI Tools v2.0 - Instalação Automática
set -e

echo "🚀 CLI Tools v2.0 - Instalação"
echo "================================"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale python3 primeiro."
    exit 1
fi

# Criar .venv se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativar .venv
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Instalar CLI Tools
echo "⚙️ Instalando CLI Tools..."
pip install -e .

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p materials/{imagens,figma,repos}
mkdir -p data/cache

# Verificar instalação
echo "✅ Verificando instalação..."
if .venv/bin/python -m src.main --version &> /dev/null; then
    echo "✅ CLI Tools instalado com sucesso!"
    echo ""
    echo "🎯 Para usar:"
    echo "   source .venv/bin/activate"
    echo "   cli-tools ui"
    echo ""
    echo "   ou diretamente:"
    echo "   .venv/bin/python -m src.main ui"
else
    echo "❌ Erro na instalação. Verifique os logs acima."
    exit 1
fi
