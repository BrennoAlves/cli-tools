# 🛠️ CLI Tools

Kit de ferramentas para desenvolvedores com IA integrada para buscar imagens, extrair designs do Figma e baixar repositórios com seleção inteligente.

## 🚀 Instalação Rápida (Linux)

### Método 1: Instalação Automática (Recomendado)

```bash
# Clonar e instalar em 2 comandos
git clone https://github.com/BrennoAlves/cli-tools.git
cd cli-tools && ./install.sh
```

### Método 2: Instalação + Configuração Automática

```bash
# Instalar e configurar tudo de uma vez
git clone https://github.com/BrennoAlves/cli-tools.git
cd cli-tools && ./install.sh && ./quick-setup.sh
```

### Método 3: Manual (se preferir)

```bash
git clone https://github.com/BrennoAlves/cli-tools.git
cd cli-tools
pip install -e .
cp .env.example .env
# Edite .env com suas chaves
cli-tools setup
```

## ✅ Verificar Instalação

```bash
cli-tools --version
cli-tools help
```

## 🔑 Configurar APIs

### Obter Chaves (Todas Gratuitas):

1. **Pexels** → https://www.pexels.com/api/ (200 req/hora)
2. **Figma** → https://www.figma.com/developers/api (1000 req/hora)  
3. **Gemini** → https://makersuite.google.com/app/apikey (15 req/min)

### Configuração Rápida:

```bash
./quick-setup.sh  # Configuração interativa
# ou
cli-tools config  # Ver status das chaves
```

## 🎯 Uso Básico

```bash
# Ver status completo
cli-tools status

# Buscar imagens
cli-tools search "escritório moderno" --count 5

# Extrair do Figma  
cli-tools figma "chave_do_arquivo" --max 3

# Baixar repositório com IA
cli-tools repo "facebook/react" "apenas CSS"

# Monitorar custos
cli-tools costs
```

## 📋 Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `status` | Status do sistema | `cli-tools status` |
| `search` | Buscar imagens | `cli-tools search "workspace" --count 3` |
| `figma` | Extrair designs | `cli-tools figma "abc123" --format png` |
| `repo` | Baixar com IA | `cli-tools repo "user/repo" "apenas CSS"` |
| `setup` | Configurar sistema | `cli-tools setup` |
| `config` | Ver configurações | `cli-tools config` |
| `costs` | Monitorar custos | `cli-tools costs` |
| `help` | Ajuda | `cli-tools help` |

## 🤖 IA Integrada

Seleção inteligente de arquivos com linguagem natural:

```bash
# Exemplos de queries inteligentes
cli-tools repo "tailwindcss/tailwindcss" "apenas CSS principais"
cli-tools repo "facebook/react" "só componentes JSX"  
cli-tools repo "microsoft/vscode" "apenas configurações JSON"
```

## 💰 Controle de Custos

Sistema automático de monitoramento:

- ✅ Monitora uso de todas as APIs
- ✅ Alertas antes de exceder limites
- ✅ Dashboard visual com status
- ✅ Confirmação para exceder free tier

```bash
cli-tools costs  # Ver dashboard
cli-tools status # Status com monitoramento
```

## 🔧 Solução de Problemas

### Comando não encontrado:
```bash
# Adicionar ao PATH
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Reinstalar:
```bash
pip install -e . --force-reinstall
```

### APIs não funcionando:
```bash
cli-tools config  # Verificar chaves
./quick-setup.sh  # Reconfigurar
```

## 📁 Estrutura

```
cli-tools/
├── install.sh              # Instalação automática
├── quick-setup.sh          # Configuração rápida  
├── cli_tools/              # Código principal
│   ├── main.py            # CLI nativo
│   ├── lib/               # Bibliotecas
│   └── tools/             # Ferramentas
├── .env.example           # Template de configuração
└── README.md              # Este arquivo
```

## 🎯 Exemplos Práticos

### Buscar Imagens:
```bash
cli-tools search "escritório startup" --count 3
cli-tools search "workspace" --orientation landscape --count 5
```

### Extrair do Figma:
```bash
cli-tools figma "chave_do_arquivo" --max 3 --format png
cli-tools figma "chave_do_arquivo" --output ./designs/
```

### Repositórios com IA:
```bash
cli-tools repo "tailwindcss/tailwindcss" "apenas CSS e SCSS"
cli-tools repo "mui/material-ui" "só componentes JSX"
cli-tools repo "vercel/next.js" "apenas arquivos de configuração"
```

---

**🎉 Instalação em 1 comando, uso imediato!**
