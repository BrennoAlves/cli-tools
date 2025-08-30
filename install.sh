#!/bin/bash

# Cores Dracula
PURPLE='\033[38;2;189;147;249m'
GREEN='\033[38;2;80;250;123m'
CYAN='\033[38;2;139;233;253m'
YELLOW='\033[38;2;241;250;140m'
RED='\033[38;2;255;85;85m'
COMMENT='\033[38;2;98;114;164m'
RESET='\033[0m'

# ASCII Art
echo -e "${PURPLE}"
cat << "EOF"
 ██████╗██╗     ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██║     ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║     ██║     ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╗███████╗██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝╚══════╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
EOF
echo -e "${RESET}"

echo -e "${COMMENT}                    v0.1 - Instalação Interativa${RESET}"
echo ""

# Verificar Python
echo -e "${CYAN}🔍 Verificando requisitos...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado${RESET}"
    echo -e "${YELLOW}💡 Instale Python 3 primeiro e tente novamente${RESET}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 encontrado${RESET}"

# Criar venv
echo -e "${CYAN}📦 Preparando ambiente virtual...${RESET}"
python3 -m venv .venv
echo -e "${GREEN}✅ Ambiente criado${RESET}"

# Instalar dependências
echo -e "${CYAN}📥 Instalando dependências...${RESET}"
source .venv/bin/activate
pip install -e . > /dev/null 2>&1
echo -e "${GREEN}✅ Dependências instaladas${RESET}"

# Criar comandos
echo -e "${CYAN}🔗 Configurando comandos globais...${RESET}"
mkdir -p ~/.local/bin

# Comando cli-tools
cat > ~/.local/bin/cli-tools << 'EOF'
#!/bin/bash
cd /home/desk/cli-tools
source .venv/bin/activate
python -m src.main "$@"
EOF

# Comando ct (alias curto)
cat > ~/.local/bin/ct << 'EOF'
#!/bin/bash
cd /home/desk/cli-tools
source .venv/bin/activate
python -m src.main "$@"
EOF

chmod +x ~/.local/bin/cli-tools
chmod +x ~/.local/bin/ct
echo -e "${GREEN}✅ Comandos configurados: ${PURPLE}cli-tools${RESET} e ${PURPLE}ct${RESET}"

echo ""
echo -e "${PURPLE}🔑 CONFIGURAÇÃO DAS APIs${RESET}"
echo -e "${COMMENT}════════════════════════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "${YELLOW}💡 Configure suas chaves para usar todas as funcionalidades:${RESET}"
echo ""

# Pexels
echo -e "${CYAN}🖼️  PEXELS API${RESET} ${COMMENT}(para buscar imagens)${RESET}"
echo -e "${COMMENT}   📋 Obtenha em: https://www.pexels.com/api/${RESET}"
echo -e -n "${GREEN}   🔑 Digite sua chave Pexels (Enter para pular): ${RESET}"
read pexels_key

echo ""

# Figma
echo -e "${CYAN}🎨 FIGMA TOKEN${RESET} ${COMMENT}(para download de designs)${RESET}"
echo -e "${COMMENT}   📋 Obtenha em: https://www.figma.com/developers/api#access-tokens${RESET}"
echo -e -n "${GREEN}   🔑 Digite seu token Figma (Enter para pular): ${RESET}"
read figma_token

echo ""

# GitHub
echo -e "${CYAN}📦 GITHUB TOKEN${RESET} ${COMMENT}(opcional, para busca avançada)${RESET}"
echo -e "${COMMENT}   📋 Obtenha em: https://github.com/settings/tokens${RESET}"
echo -e -n "${GREEN}   🔑 Digite seu token GitHub (Enter para pular): ${RESET}"
read github_token

# Salvar configurações
echo ""
echo -e "${CYAN}💾 Salvando configurações...${RESET}"

cat > .env << EOF
# 🔑 Configuração das APIs - CLI Tools v0.1
# 📝 Edite este arquivo quando necessário

# 🖼️ Pexels API (para buscar imagens)
# 📋 Obtenha em: https://www.pexels.com/api/
PEXELS_API_KEY=${pexels_key}

# 🎨 Figma Token (para download de designs)  
# 📋 Obtenha em: https://www.figma.com/developers/api#access-tokens
FIGMA_TOKEN=${figma_token}

# 📦 GitHub Token (opcional, para busca avançada)
# 📋 Obtenha em: https://github.com/settings/tokens
GITHUB_TOKEN=${github_token}
EOF

echo -e "${GREEN}✅ Configurações salvas em .env${RESET}"

echo ""
echo -e "${GREEN}🎉 INSTALAÇÃO CONCLUÍDA!${RESET}"
echo -e "${COMMENT}════════════════════════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "${PURPLE}🚀 Como usar:${RESET}"
echo -e "${GREEN}   cli-tools${RESET}                     ${COMMENT}# Interface interativa${RESET}"
echo -e "${GREEN}   ct${RESET}                           ${COMMENT}# Interface interativa (comando curto)${RESET}"
echo -e "${GREEN}   cli-tools image 'office' -c 5${RESET}  ${COMMENT}# Buscar imagens${RESET}"
echo -e "${GREEN}   ct figclone AbCdEfGh123${RESET}       ${COMMENT}# Download Figma${RESET}"
echo -e "${GREEN}   cli-tools repo user/repo${RESET}      ${COMMENT}# Clonar repositório${RESET}"
echo -e "${GREEN}   ct status${RESET}                     ${COMMENT}# Verificar APIs${RESET}"
echo ""
echo -e "${YELLOW}📝 Para reconfigurar APIs: ${PURPLE}nano .env${RESET}"
echo ""
echo -e "${CYAN}🎯 Teste agora:${RESET}"
cli-tools
