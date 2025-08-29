# CLI Tools v2.0 — enxuto e direto

Kit de ferramentas para desenvolvedores com UI minimalista e comandos para automação.

## Instalação (local)
```bash
pip install -r requirements.txt
pip install .
# ou: python -m src.main --help
```

Possíveis problemas
- “ModuleNotFoundError: textual”: instale dependências (requirements.txt) para usar a UI.
- Sem chaves de API: configure `.env` (ver abaixo) ou use o form “Configurações” na UI.
- Rede bloqueada: `repo` cai em fallback de ZIP; `search/figma` e IA podem falhar — veja as mensagens.

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

## .env (exemplo)
```bash
PEXELS_API_KEY=...
FIGMA_API_TOKEN=...
GEMINI_API_KEY=...
CLI_THEME=transparent   # ou dracula
CLI_UI_TOP_PAD=6
```

## Comandos e parâmetros
- `cli-tools ui`: abre a interface interativa (Textual)
- `cli-tools status [--simple] [--live]`
- `cli-tools search <consulta> [--count N] [--orientation landscape|portrait|square] [--output DIR] [--json]`
- `cli-tools figma <file_key> [--mode all|components|css] [--max|-n N] [--format|-f fmt] [--output DIR]`
- `cli-tools repo <usuario/repositorio> [query] [--query|-q QUERY] [--no-ai] [--all] [--output DIR] [--explain LVL] [--dry-run] [--interactive] [--json]`

## Estrutura do projeto
```
src/
├── main.py              # Entry point (Click)
├── commands/            # Comandos isolados (search, figma, repo, status)
└── lib/                 # Bibliotecas compartilhadas
    ├── apis.py          # Integrações Pexels/Figma/Repo (funções puras)
    ├── config.py        # Config unificada (.env + data/config.json)
    ├── ui.py            # UI minimalista com formulários
    └── utils.py         # Status/ajudantes
data/
├── config.json          # Estado (workspace, apis, theme)
└── cache/               # Caches (ex.: metadata.json)
materials/
├── imagens/             # Imagens baixadas
├── figma/               # Exports do Figma
└── repos/               # Repositórios baixados
```

## Exemplos rápidos
```bash
cli-tools search "office desk" -c 1
cli-tools figma AbCdEfGh --mode components -n 3 -f png
cli-tools repo tailwindlabs/tailwindcss -q "components"
cli-tools ui
```
