#!/bin/bash

# 🔧 CLI Tools - Configuração Rápida
# Configura as APIs de forma interativa

echo "🔧 CLI Tools - Configuração Rápida"
echo "=================================="
echo

# Verificar se cli-tools está instalado
if ! command -v cli-tools &> /dev/null; then
    echo "❌ cli-tools não está instalado!"
    echo "💡 Execute primeiro: ./install.sh"
    exit 1
fi

# Verificar se .env já existe
if [ -f ".env" ]; then
    echo "⚠️  Arquivo .env já existe!"
    read -p "🤔 Deseja sobrescrever? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Configuração cancelada"
        exit 0
    fi
fi

# Copiar template
if [ ! -f ".env.example" ]; then
    echo "❌ Arquivo .env.example não encontrado!"
    exit 1
fi

cp .env.example .env
echo "✅ Arquivo .env criado"
echo

echo "🔑 Configure suas chaves de API:"
echo

# Pexels API
echo "📸 PEXELS API (busca de imagens)"
echo "   Obtenha em: https://www.pexels.com/api/"
read -p "   Sua chave Pexels (Enter para pular): " PEXELS_KEY
if [ ! -z "$PEXELS_KEY" ]; then
    sed -i "s/sua_chave_pexels_aqui/$PEXELS_KEY/" .env
    echo "   ✅ Pexels configurado"
else
    echo "   ⏭️  Pexels pulado"
fi
echo

# Figma API
echo "🎨 FIGMA API (extração de designs)"
echo "   Obtenha em: https://www.figma.com/developers/api"
read -p "   Seu token Figma (Enter para pular): " FIGMA_TOKEN
if [ ! -z "$FIGMA_TOKEN" ]; then
    sed -i "s/seu_token_figma_aqui/$FIGMA_TOKEN/" .env
    echo "   ✅ Figma configurado"
else
    echo "   ⏭️  Figma pulado"
fi
echo

# Gemini API
echo "🤖 GEMINI API (IA para seleção)"
echo "   Obtenha em: https://makersuite.google.com/app/apikey"
read -p "   Sua chave Gemini (Enter para pular): " GEMINI_KEY
if [ ! -z "$GEMINI_KEY" ]; then
    sed -i "s/sua_chave_gemini_aqui/$GEMINI_KEY/" .env
    echo "   ✅ Gemini configurado"
else
    echo "   ⏭️  Gemini pulado"
fi
echo

echo "🚀 Executando setup inicial..."
cli-tools setup

echo
echo "✅ Configuração concluída!"
echo
echo "📋 Comandos úteis:"
echo "   cli-tools status  # Ver status"
echo "   cli-tools help    # Ver ajuda"
echo "   cli-tools config  # Ver configurações"
echo
echo "🎉 cli-tools está pronto para uso!"
