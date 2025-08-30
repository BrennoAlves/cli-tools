#!/bin/bash

# CLI Tools v2.0 - Update
set -e

echo "🔄 CLI Tools - Update"
echo "===================="

# Verificar se pipx está instalado
if ! command -v pipx &> /dev/null; then
    echo "❌ pipx não encontrado. Use ./install.sh primeiro."
    exit 1
fi

# Verificar se cli-tools está instalado
if ! command -v cli-tools &> /dev/null; then
    echo "❌ cli-tools não instalado. Use ./install.sh primeiro."
    exit 1
fi

echo "📦 Atualizando CLI Tools..."
pipx upgrade cli-tools

echo "✅ Update concluído!"
echo ""
echo "📋 Versão atual:"
cli-tools --version 2>/dev/null || echo "Comando --version não implementado"
