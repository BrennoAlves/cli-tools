# 🏗️ Arquitetura — CLI Tools v2.0

Este documento descreve, em alto nível, a arquitetura atual do projeto e os princípios que orientam as decisões.

Visão Geral
- Dual mode: UI interativa (Textual) para humanos e comandos Click para automação/agents.
- Modularidade: comandos em `src/commands`, biblioteca em `src/lib`, ponto de entrada em `src/main.py`.
- Workspace: conteúdos baixados em `materials/{imagens,figma,repos}` (não versionados).

Estrutura Atual (resumo)
- `src/main.py`: entry point Click (grupo `cli`).
- `src/commands/`: `search`, `figma`, `repo`, `status`.
- `src/lib/`: `config.py` (estado/config), `apis.py` (integrações), `ui.py` (TUI), `utils.py` (helpers).
- `materials/`: `imagens/`, `figma/`, `repos/` (criados na instalação/execução).
- `data/`: `config.json` gerado em runtime/instalação; não versionado.
- `.amazonq/rules/`: documentação interna (este arquivo, rules.md, diário de bordo, relatórios).

Princípios
- Simplicidade: dependências mínimas; empacotamento limpo.
- Observabilidade: mensagens e UX claras no terminal, em português.
- Extensibilidade: novas tools adicionadas como comandos + funções em `lib/apis.py`.

Notas
- Consulte `.amazonq/rules/rules.md` para regras operacionais e fluxo de PR/CI.
- O instalador `install.sh` cria `data/config.json` com defaults e os diretórios em `materials/`.

