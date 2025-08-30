# 🛠️ CLI Tools v0.1

Kit de ferramentas para desenvolvedores com interface moderna e tema Dracula.

## ✨ Funcionalidades

### 🖼️ **Image** - Buscar imagens no Pexels
- Busca com filtros (orientação, tamanho, cor)
- Download em alta qualidade
- Free tier: 200 requests/hora

### 🎨 **FigClone** - Download de designs do Figma
- Export em PNG, JPG, SVG, PDF
- Escalas customizadas (1x-4x)
- Componentes específicos
- Free tier: 30 requests/minuto

### 📦 **Repo** - Clonar repositórios do GitHub
- Clone com profundidade customizada
- Busca em arquivos
- Informações detalhadas do repositório
- Free tier: 60 requests/hora (5000 com token)

### 📊 **Status** - Verificar APIs e sistema
- Status das APIs em tempo real
- Informações do sistema
- Verificação de dependências

## 🚀 Instalação

```bash
git clone https://github.com/BrennoAlves/cli-tools.git
cd cli-tools
./install.sh
```

O instalador é **interativo** e vai:
- ✅ Criar ambiente virtual automaticamente
- ✅ Instalar todas as dependências
- ✅ Configurar comandos globais (`cli-tools` e `ct`)
- ✅ Solicitar chaves das APIs (opcional)
- ✅ Criar arquivo `.env` com suas configurações

## 🎯 Como usar

### Interface Interativa (Recomendado)
```bash
cli-tools    # ou ct (comando curto)
```

**Navegação:**
- ↑↓ setas para navegar
- Enter para selecionar
- q para sair

### Comandos Diretos
```bash
# Buscar imagens
cli-tools image "office desk" --count 5 --orientation landscape

# Download do Figma
cli-tools figclone AbCdEfGh123 --format png --scale 2

# Clonar repositório
cli-tools repo microsoft/vscode --query "components"

# Status do sistema
cli-tools status
```

## 🔑 Configuração das APIs

As chaves são configuradas durante a instalação, mas você pode editá-las depois:

```bash
nano .env
```

### Onde obter as chaves:

- **Pexels**: https://www.pexels.com/api/
- **Figma**: https://www.figma.com/developers/api#access-tokens  
- **GitHub**: https://github.com/settings/tokens (opcional)

## 🎨 Interface

- **Tema Dracula** completo
- **ASCII art** no menu principal
- **Navegação por setas** intuitiva
- **Panels informativos** com cores
- **Validação em tempo real**
- **Mensagens de erro amigáveis**

## 📋 Requisitos

- Python 3.8+
- Git (para clone de repositórios)
- Linux/macOS (Windows via WSL)

## 🏗️ Estrutura

```
cli-tools/
├── src/
│   ├── main.py              # Entry point com menu
│   └── tools/               # Ferramentas
│       ├── image.py         # Busca de imagens
│       ├── figclone.py      # Download Figma
│       ├── repo.py          # Clone de repositórios
│       └── status.py        # Status do sistema
├── install.sh               # Instalação interativa
├── pyproject.toml           # Dependências
└── README.md                # Este arquivo
```

## 🎉 Primeira versão

Esta é a primeira versão oficial do CLI Tools, criada do zero com foco em:

- **Simplicidade**: Instalação em 1 comando
- **Usabilidade**: Interface intuitiva e amigável  
- **Profissionalismo**: Código limpo e bem estruturado
- **Funcionalidade**: Ferramentas úteis para desenvolvedores

---

**Desenvolvido com ❤️ usando Python, Rich e Textual**
