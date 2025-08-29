# 🛠️ CLI Tools v2.0

Kit de ferramentas para desenvolvedores com IA integrada e interface moderna.

![CLI Tools](https://img.shields.io/badge/CLI%20Tools-v2.0-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ⚡ Instalação Rápida

```bash
curl -sSL https://raw.githubusercontent.com/cli-tools/cli-tools/main/install.sh | bash
```

## 🎯 Funcionalidades

### 🔍 **Busca de Imagens**
```bash
cli-tools search "escritório moderno" -n 5
```
- Busca no Pexels com IA
- Download automático
- Organização inteligente

### 🎨 **Extração Figma**
```bash
cli-tools figma abc123def --format png
```
- Extrai designs e assets
- Múltiplos formatos (PNG, SVG, JPG)
- Metadados preservados

### 📦 **Download de Repositórios**
```bash
cli-tools repo tailwindcss/tailwindcss -q "componentes"
```
- Seleção inteligente com IA
- Filtros personalizados
- Análise de relevância

### 🖥️ **Interface Interativa**
```bash
cli-tools ui
```
- Menu com navegação por setas
- Cores vibrantes (tema Dracula)
- Feedback visual em tempo real

Temas:
- `CLI_THEME=transparent` (padrão, usa fundo do seu terminal)
- `CLI_THEME=dracula` (fundo Dracula dentro da UI)

Exemplos:
```bash
CLI_THEME=dracula cli-tools
CLI_THEME=transparent cli-tools
```

Atalho:
- Dentro da UI, pressione `T` para alternar entre os temas.

## 📊 Status e Monitoramento

```bash
cli-tools status              # Status geral
cli-tools status --dashboard  # Dashboard visual
cli-tools usage              # Uso das APIs
```

## ⚙️ Configuração

### 🔑 **APIs Necessárias**

Crie um arquivo `.env` na raiz:

```bash
# Pexels (gratuito: 200 req/hora)
PEXELS_API_KEY=sua_chave_aqui

# Figma (gratuito: sem limite)
FIGMA_API_TOKEN=seu_token_aqui

# Google Gemini (gratuito: 15 req/min)
GEMINI_API_KEY=sua_chave_aqui
```

### 🌐 **Obter Chaves**

- **Pexels**: https://www.pexels.com/api/
- **Figma**: https://www.figma.com/developers/api
- **Gemini**: https://makersuite.google.com/app/apikey

### 🔧 **Configuração Interativa**

```bash
cli-tools config --interactive
```

## 📁 Workspace Automático

O CLI Tools organiza automaticamente seus arquivos:

```
materials/
├── imagens/          # Imagens do Pexels
├── figma/            # Designs do Figma
└── repos/            # Repositórios clonados
```

- **Em projetos (.git)**: `./materials`
- **Fora de projetos**: `~/materials`
- **Configurável**: `cli-tools config --workspace /caminho`

## 🎮 Interface Interativa

A interface menu oferece navegação intuitiva:

- **↑↓**: Navegar opções
- **Enter**: Selecionar
- **Q/Esc**: Sair
- **R**: Atualizar

### Funcionalidades:
- 🔍 Busca de imagens com filtros
- 🎨 Extração de designs Figma
- 📦 Download inteligente de repos
- 📊 Dashboard de status em tempo real
- ⚙️ Configuração visual de APIs
- 🛠️ Ferramentas auxiliares

## 🚀 Exemplos de Uso

### **Workflow Completo**
```bash
# 1. Configurar APIs
cli-tools config --interactive

# 2. Verificar status
cli-tools status

# 3. Buscar recursos
cli-tools search "interface moderna" -n 10
cli-tools figma design-key-123 --format svg
cli-tools repo microsoft/vscode -q "themes"

# 4. Interface visual
cli-tools ui
```

### **Automação**
```bash
# Script para baixar assets de projeto
#!/bin/bash
cli-tools search "logo startup" -n 3 --orientation square
cli-tools figma $FIGMA_KEY --format png
cli-tools repo tailwindcss/tailwindcss -q "components"
```

### **Integração com Pipelines**
```bash
# Output JSON para processamento
cli-tools search "background" --json | jq '.urls[]'
cli-tools status --json | jq '.apis.pexels.status'
```

## 🏗️ Arquitetura

```
cli-tools/                  # 📁 Repositório principal
├── src/                    # 🐍 Código fonte Python
│   ├── __init__.py        # 📦 Inicialização do pacote
│   ├── main.py            # 🚀 Entry point principal
│   ├── menu_app/          # 🎮 Interface TUI interativa
│   │   └── interactive_menu.py
│   ├── core/              # ⚙️ Lógica de negócio e APIs
│   │   ├── config.py      # ⚙️ Configuração geral
│   │   ├── config_ia.py   # 🤖 Configuração IA/Gemini
│   │   ├── config_diretorios.py # 📁 Gestão de diretórios
│   │   ├── controle_uso.py # 📊 Controle de uso das APIs
│   │   ├── interface.py   # 🖥️ Interface base
│   │   ├── navegacao_cli.py # 🧭 Navegação CLI
│   │   ├── rich_dashboards.py # 📊 Dashboards Rich completos
│   │   └── rich_dashboards_simple.py # 📊 Dashboards simplificados
│   └── tools/             # 🛠️ Ferramentas específicas
│       ├── buscar-imagens.py # 🔍 Busca de imagens (Pexels)
│       ├── extrator-figma.py # 🎨 Extração Figma
│       └── baixar-repo.py    # 📦 Download de repositórios
├── materials/             # 📁 Workspace de arquivos
│   ├── imagens/          # 🖼️ Imagens baixadas
│   ├── figma/            # 🎨 Designs do Figma
│   └── repos/            # 📦 Repositórios clonados
├── .amazonq/docs/         # 📚 Documentação de desenvolvimento
├── .env                   # 🔑 Configuração local
├── README.md             # 📖 Documentação pública
├── requirements.txt      # 📦 Dependências Python
└── install.sh            # 🚀 Script de instalação
```

## 🔧 Desenvolvimento

### **Instalação Local**
```bash
git clone https://github.com/cli-tools/cli-tools.git
cd cli-tools
pip install -r requirements.txt
python -m src.main --help
```

### **Estrutura do Código**
- **`src/main.py`**: CLI principal e detecção de modo
- **`src/menu_app/`**: Interface TUI com Textual
- **`src/core/`**: Integrações de API e lógica de negócio
- **`src/tools/`**: Utilitários e ferramentas auxiliares
