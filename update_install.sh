#!/bin/bash
# Script para atualizar instalação do CLI Tools

echo "🔄 Atualizando instalação do CLI Tools..."

# Diretório de instalação
INSTALL_DIR="$HOME/.local/share/cli-tools"

# Copiar arquivos atualizados
echo "📁 Copiando arquivos..."
cp -r cli_tools/* "$INSTALL_DIR/cli_tools/"

# Copiar requirements se necessário
if [ -f "requirements.txt" ]; then
    cp requirements.txt "$INSTALL_DIR/"
fi

echo "✅ Instalação atualizada com sucesso!"
echo ""
echo "🚀 Comandos disponíveis:"
echo "  cli-tools ui          # Interface Textual"
echo "  cli-tools ui --demo   # Modo demo"
echo "  cli-tools status      # Dashboard Rich"
echo "  cli-tools search      # Buscar imagens"
echo ""
echo "🎯 Teste a interface Textual:"
echo "  cli-tools ui --demo"
