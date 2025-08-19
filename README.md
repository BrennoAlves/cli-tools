# 🛠️ CLI Tools v1.1.0

Kit de ferramentas para desenvolvedores com IA integrada. Busque imagens, extraia designs do Figma e baixe repositórios com seleção inteligente.

## ⚡ Instalação Rápida

### Método 1: Instalação Interativa (Recomendado)
```bash
curl -sSL https://raw.githubusercontent.com/BrennoAlves/cli-tools/main/install-interactive.sh | bash
```

### Método 2: Manual
```bash
git clone https://github.com/BrennoAlves/cli-tools.git
cd cli-tools
./install.sh
```

## 🚀 Uso Rápido

```bash
# Ver status e configuração
cli-tools status

# Buscar imagens (flags duplas: --count/-c ou --number/-n)
cli-tools search "escritório moderno" -n 5
cli-tools search "logo startup" --count 3 --orientation landscape

# Extrair designs do Figma
cli-tools figma "abc123def" --number 3 --format png

# Baixar repositório com IA (flags duplas: --query/-q)
cli-tools repo "tailwindcss/tailwindcss" -q "componentes"
cli-tools repo "facebook/react" --query "apenas CSS"

# Configurar comportamento da IA
cli-tools ai-config --interactive
cli-tools ai-config --explain detailed
```

## 🤖 Controle da IA

### Interface Moderna com Navegação
- **🎮 Navegação por setas** - Interface estilo Gemini (↑↓ + Enter)
- **🔢 Seleção rápida** - Digite números 1-4 para escolha direta
- **🔄 Fallback automático** - Menu tradicional se terminal não suportar
- **🤖 Compatível com IAs** - Comandos diretos funcionam normalmente

### Modelos Pré-Configurados
```bash
# Interface navegável
cli-tools ai-config --interactive

# Comandos diretos (para IAs)
cli-tools ai-config --modelo conservador  # 🛡️ Máxima segurança
cli-tools ai-config --modelo equilibrado  # ⚖️ Padrão balanceado  
cli-tools ai-config --modelo yolo         # 🚀 Rápido e direto
```

### Modos Especiais
- `--dry-run` - Mostrar o que seria feito sem executar
- `--interactive` - Modo interativo com confirmações
- `--json` - Saída em formato JSON para pipelines

### Exemplos Avançados
```bash
# Ver o que a IA faria sem executar
cli-tools repo "vercel/next.js" -q "configurações" --dry-run

# Modo interativo com explicação detalhada
cli-tools repo "user/repo" -q "CSS" --interactive --explain detailed

# Pipeline com JSON
cli-tools search "logo" --json | jq '.urls[]' | xargs wget
```

## 📋 Comandos Disponíveis

| Comando | Descrição | Flags Principais |
|---------|-----------|------------------|
| `search` | Buscar e baixar imagens | `-n/--number`, `-o/--output`, `--json` |
| `figma` | Extrair designs do Figma | `-n/--number`, `-f/--format`, `--json` |
| `repo` | Baixar repositório com IA | `-q/--query`, `--explain`, `--dry-run` |
| `status` | Status do sistema | - |
| `config` | Configurar APIs | - |
| `ai-config` | Configurar IA | `--interactive`, `--show`, `--explain` |
| `costs` | Monitorar custos | - |
| `help` | Ajuda e exemplos | - |

## 🔑 APIs Necessárias

### 🖼️ Pexels (Busca de Imagens)
- **Gratuita**: 200 requests/hora
- **Obter**: https://www.pexels.com/api/
- **Uso**: Buscar e baixar imagens profissionais

### 🎨 Figma (Extração de Designs)
- **Gratuita**: Para seus próprios arquivos
- **Obter**: https://www.figma.com/developers/api
- **Uso**: Extrair designs e assets

### 🤖 Google Gemini (IA)
- **Gratuita**: 15 requests/minuto
- **Obter**: https://makersuite.google.com/app/apikey
- **Uso**: Seleção inteligente de arquivos

## 🎯 Exemplos Práticos

### Desenvolvimento Frontend
```bash
# Buscar imagens para mockups
cli-tools search "dashboard interface" -n 5 --orientation landscape

# Baixar apenas CSS de um framework
cli-tools repo "tailwindcss/tailwindcss" -q "apenas CSS e configurações"

# Extrair ícones do Figma
cli-tools figma "design-system-key" -n 10 --format svg
```

### Pesquisa e Referências
```bash
# Baixar documentação específica
cli-tools repo "facebook/react" -q "documentação e exemplos"

# Buscar inspiração visual
cli-tools search "modern website design" -n 8 --json > inspirations.json
```

### Pipeline Automatizado
```bash
# Script para coletar referências
#!/bin/bash
cli-tools search "ui components" -n 5 -o ./references/images/
cli-tools repo "chakra-ui/chakra-ui" -q "componentes" -o ./references/code/
cli-tools figma "design-tokens" -n 3 -o ./references/designs/
```

## ⚙️ Configuração Avançada

### Arquivo .env
```bash
# APIs
PEXELS_API_KEY=sua_chave_aqui
FIGMA_API_TOKEN=seu_token_aqui
GEMINI_API_KEY=sua_chave_aqui

# Configurações
DEFAULT_TIMEOUT=30
DOWNLOAD_TIMEOUT=120
MAX_RETRIES=3
```

### Configuração da IA
```bash
# Configuração interativa
cli-tools ai-config --interactive

# Configuração rápida
cli-tools ai-config --explain detailed

# Ver configuração atual
cli-tools ai-config --show
```

## 🔒 Segurança

- ✅ Validação rigorosa de entrada
- ✅ Sanitização de URLs e arquivos
- ✅ Proteção contra path traversal
- ✅ Rate limiting automático
- ✅ Sem chaves expostas no código

## 📊 Status do Projeto

- **Versão**: 1.1.0
- **Status**: Produção
- **Segurança**: 9.2/10
- **UX**: Modernizado
- **IA**: Transparente e controlável

## 🤝 Contribuição

```bash
git clone https://github.com/BrennoAlves/cli-tools.git
cd cli-tools
# Fazer alterações
git commit -m "Sua contribuição"
git push origin main
```

## 📚 Links

- **Repositório**: https://github.com/BrennoAlves/cli-tools
- **Issues**: https://github.com/BrennoAlves/cli-tools/issues
- **Releases**: https://github.com/BrennoAlves/cli-tools/releases

---

**🎯 CLI Tools v1.1.0 - Ferramentas modernas para desenvolvedores modernos**
