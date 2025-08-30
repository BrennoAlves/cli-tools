# Relatório de Validação — CLI Tools

Data: 2025-08-30
Branch: dev
Local: .amazonq/rules/RELATORIO_ESTRUTURA_CLI.md

## Visão Geral
- CLI em Python com Click (comandos) e Textual (UI).
- Estrutura: `src/main.py` (entry), `src/commands/*`, `src/lib/*`, `tests/*` (apenas dev).
- Empacotamento: `pyproject.toml` com `console_scripts` e `MANIFEST.in` alinhados.
- CI: pipeline “CI” configurada na dev para PRs com base na main.

## Pontos Validados
- Comandos: `search`, `figma`, `repo`, `status` registrados no grupo Click.
- Biblioteca: `lib/config.py` (estado/config), `lib/apis.py` (APIs), `lib/ui.py` (TUI), `lib/utils.py` (helpers).
- Config: `data/config.json` gerado em runtime (não versionado) e agora gerado também na instalação.
- Instalador: `install.sh` passou a criar `data/config.json` com defaults ao final da instalação.
- Ignore: `.gitignore` evita `venv/`, `data/`, `materials/`, caches, `.amazonq/` na main.

## Inconsistências Entre Branches (resolvidas/alinhadas)
- Testes e CI apenas na dev; main sem workflows.
- Baseline unificado (main via PR de sincronização): Python >=3.10 e deps atualizadas.
- `.amazonq/` mantido apenas na dev (main limpa).

## Regras do Fluxo (resumo)
- PR obrigatório `dev → main` com status `CI` aprovado (strict).
- Auto‑merge por squash ativado: merge automático quando `CI` fica verde.
- Commits e PRs em português; mensagens do CI em português.

## Checklist
- [x] Estrutura de CLI consistente.
- [x] CI em dev disparando para PRs na main.
- [x] Proteção da main ativa (PR + CI + linear history).
- [x] `.amazonq/` apenas na dev.
- [x] `install.sh` gera `data/config.json` com defaults.
