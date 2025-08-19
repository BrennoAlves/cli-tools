# 🛠️ CLI Tools

Kit de ferramentas para desenvolvedores com IA integrada.

## ⚡ Instalação (Comando Único)

```bash
curl -sSL https://raw.githubusercontent.com/BrennoAlves/cli-tools/main/install.sh | bash
```

## 🚀 Uso

```bash
# Status do sistema
cli-tools status

# Buscar imagens
cli-tools search "escritório moderno" -n 5

# Extrair designs do Figma  
cli-tools figma "abc123def" -n 3 --format png

# Baixar repositório com IA
cli-tools repo "tailwindcss/tailwindcss" -q "componentes"

# Configurar IA
cli-tools ai-config --interactive
```

## 🔑 APIs Necessárias

- **Pexels**: https://www.pexels.com/api/ (200 req/hora gratuito)
- **Figma**: https://www.figma.com/developers/api (gratuito)  
- **Gemini**: https://makersuite.google.com/app/apikey (15 req/min gratuito)

## 📋 Comandos

| Comando | Descrição |
|---------|-----------|
| `search` | Buscar e baixar imagens |
| `figma` | Extrair designs do Figma |
| `repo` | Baixar repositório com IA |
| `status` | Status do sistema |
| `config` | Configurar APIs |
| `ai-config` | Configurar IA |

## 🎯 Exemplos

```bash
# Busca com orientação
cli-tools search "logo startup" --orientation landscape -n 3

# Repo apenas CSS
cli-tools repo "facebook/react" -q "apenas CSS" --dry-run

# Figma em SVG
cli-tools figma "design-key" -n 5 --format svg

# Saída JSON para pipelines
cli-tools search "interface" --json | jq '.urls[]'
```

---

**v1.1.0** - Ferramentas modernas para desenvolvedores modernos
