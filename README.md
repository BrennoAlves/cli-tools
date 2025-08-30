# CLI Tools v2.0 — Kit de ferramentas para desenvolvedores

Interface interativa moderna com comandos para automação.

## Instalação

### Via pip (recomendado)
```bash
pip install cli-tools
```

### Desenvolvimento local
```bash
git clone https://github.com/user/cli-tools.git
cd cli-tools
pip install -r requirements.txt
pip install -e .
```

## Uso Rápido

### Interface Interativa
```bash
cli-tools
# ou
cli-tools ui
```

### Comandos Diretos
```bash
# Buscar imagens
cli-tools search "office desk" -c 3

# Extrair do Figma  
cli-tools figma AbCdEfGh --mode components -n 5

# Baixar repositório
cli-tools repo facebook/react -q "components"

# Ver status
cli-tools status
```

## Configuração

Crie um arquivo `.env` ou configure via interface:

```bash
PEXELS_API_KEY=sua_chave_pexels
FIGMA_API_TOKEN=seu_token_figma  
GEMINI_API_KEY=sua_chave_gemini
CLI_THEME=transparent  # ou dracula
```

## Funcionalidades

- 🔍 **Busca de imagens** - Pexels API com download automático
- 🎨 **Extração Figma** - Components, CSS, múltiplos formatos
- 📦 **Download inteligente** - Repositórios com IA seletiva
- 🎮 **Interface moderna** - Navegação por setas, validação em tempo real
- ⚙️ **Dual mode** - UI para humanos, CLI para automação

## Comandos e Parâmetros

```bash
cli-tools search <consulta> [--count N] [--orientation landscape|portrait|square] [--output DIR]
cli-tools figma <file_key> [--mode all|components|css] [--max N] [--format png|jpg|svg] [--output DIR]  
cli-tools repo <usuario/repositorio> [query] [--query QUERY] [--no-ai] [--all] [--output DIR]
cli-tools status [--simple] [--live]
cli-tools ui
```

## Estrutura de Arquivos

```
materials/
├── imagens/     # Imagens baixadas (organizadas por categoria)
├── figma/       # Exports do Figma  
└── repos/       # Repositórios baixados
```

## Desenvolvimento

```bash
# Executar testes (apenas branch dev)
python run_tests.py

# Build para distribuição
python build.py

# Instalar dependências de dev
pip install -e ".[dev]"
```

## Licença

MIT License - veja LICENSE para detalhes.
