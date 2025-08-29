# 🗺️ Plano de Ação — CLI Tools v2.0

Este documento consolida um checkup completo do sistema, lista o que é legado, o que falta para ficar pronto para “mercado”, e um plano objetivo para simplificar e reduzir o tamanho do projeto sem perder capacidades.

## 🎯 Objetivos
- Dual‑mode sólido: UI para humanos + comandos paramétricos para automação/agents.
- Confiável: erros previsíveis, limites/quotas respeitados, cache eficiente.
- Leve e modular: fácil de manter, instalar e estender.
- Pronto para distribuição (PyPI), com testes, docs e versionamento.

---

## 🔎 Checkup Atual
- Estrutura
  - main: já enxuto (src/main.py) registrando comandos isolados e `ui`.
  - commands: comandos isolados (`search`, `figma`, `repo`, `status`).
  - lib: `ui`, `config`, `apis` (wrappers), `utils`.
  - tools: scripts legados com lógica (Pexels/Figma/Repo) — ainda em uso via subprocess.
  - core: módulos legados (config, diretórios, dashboards, interface, controle_uso).
  - data/: config.json (novo estado unificado), cache/logs sendo migrados para data/.
- UI
  - Menu minimalista centralizado (Textual), tecla `T` para tema, persistência no `.env`/data.
  - Espaçamento superior configurável por `CLI_UI_TOP_PAD`.
- CLI/Comandos
  - search: padrão `--count 1`; saída organizada por categoria quando `--output` ausente.
  - figma: `--mode` (all/components/css) — CSS básico gerado quando solicitado.
  - repo: IA opcional (query) com fallback para clone completo; flags para `--all`, `--no-ai`.
- Configuração
  - .env criado, `data/config.json` criado e usado por lib/config.
  - Ainda coexistem `core/config*.py` (legado) e `lib/config.py` (novo).
- Cache/Logs
  - `metadata.json` migrado para `data/cache/metadata.json`.
  - Logs em `data/logs/` (migrado na ferramenta de imagens).
- Dependências
  - `textual`, `rich`, `click`, `requests`, `python-dotenv`.
- Testes/CI
  - Ausentes (unit/integration) e CI (lint/test/build).
- Distribuição
  - Ainda não empacotado como pacote PyPI (`console_scripts`).

---

## 🧹 Legado a Eliminar ou Migrar
- `src/tools/` (lógica de APIs em scripts)
  - Migrar Pexels/Figma/Repo para `src/lib/apis.py` (funções puras) e remover `subprocess`.
  - Remover `tools/` após migração completa.
- `src/core/`
  - `config.py`, `config_ia.py`, `config_diretorios.py`: consolidar em `lib/config.py` (única fonte).
  - `controle_uso.py`, `rich_dashboards*.py`, `interface.py`: consolidar em `lib/utils.py` (dashboards, tracking) e remover o restante.
- `materials/` (workspace exemplar)
  - Manter criação on‑demand via `lib/config.get_workspace()`; não versionar conteúdo.
- Caches/Logs espalhados
  - Padronizar: `data/cache` e `data/logs`. Excluir de distribuição.

---

## 🧩 Itens Faltantes para “Ferramenta de Mercado”
- Robustez técnica
  - Tratamento de erros consistente (timeouts, backoff, HTTP status, JSON inválido).
  - Rate limiting configurável por API; retries com jitter exponencial.
  - Timeouts configuráveis em `config.json`/env.
  - Concurrency segura p/ downloads (limite ajustável) e cancelamento.
- Segurança
  - Armazenamento de chaves: opção de `keyring` (quando disponível), com fallback .env/config.json.
  - Nunca logar chaves; sanitize em exceptions.
- Qualidade do Código
  - Tipagem (mypy), lint (ruff/flake8), formatação (black), docstrings (pydocstyle).
  - Testes unitários (mock de HTTP) e de integração (smoke com env OFFLINE).
- Observabilidade
  - Logging estruturado (níveis: DEBUG/INFO/WARN/ERROR), habilitado por flag/env.
  - Métricas básicas: contagem de usos/erros por API.
- Empacotamento
  - pyproject.toml com `console_scripts=cli-tools`.
  - Excluir `data/`, `materials/`, `logs`, `cache` do build.
  - Compatibilidade Windows/macOS/Linux (paths, encoding).
- UX e Docs
  - Autocompleção (Click shell completion).
  - Mensagens UX mais curtas/padrão; help enriquecido com exemplos reais.
  - Documentação no README + comandos `--help` coesos.
- Extensibilidade
  - Design de plugin (entry points) para novas tools.
  - Camada `lib/apis.py` como contrato estável.

### Formulários Navegáveis (UI)
- Menus internos para cada comando (sem sair para terminal cru):
  - Search: formulário com campos (consulta, count, orientation, output), preview de resultado (quando possível), validação inline.
  - Figma: formulário com (file_key, format, mode, max_images, output), descrição do efeito de cada opção, validação de chave.
  - Repo: formulário com (repositorio, query, flags no_ai/all/explain/interactive/output), ajuda contextual do que cada flag faz.
  - Status/Help/Config/Costs: telas navegáveis com botões/inputs (ex.: alterar tema, workspace, chaves de API) e validação em tempo real.
- Comportamento: mesma estética (tema Dracula), navegação por setas/Tab/Shift+Tab, Enter para confirmar, Esc para voltar.
- Integração: UI chama diretamente `lib/apis` (não `click.prompt`) e exibe progresso/erros no próprio app.

---

## ✂️ Reduzir Tamanho do Projeto
- Consolidar módulos duplicados
  - `core/*` → `lib/*` (config, utils). Remover `core/*` após migração.
  - `tools/*` → `lib/apis.py` (funções puras). Remover `tools/*` após migrar comandos para `lib/apis`.
- Remover artefatos
  - `__pycache__/`, `*.pyc`, `data/logs/*`, `data/cache/*` do versionamento e do pacote.
- Simplificar UI
  - Uma única UI (lib/ui.py). Evitar múltiplas variantes.
- Documentação
  - Manter um README enxuto e mover guias longos para docs/ (opcional).

---

## 🛠️ Plano por Fases (Incremental)

### Fase 1 — Consolidar Config e Estado
- [ ] `lib/config.py`: absorver `core/config.py`, `config_ia.py`, `config_diretorios.py` (workspace, env, tema, IA, limites).
- [ ] Ajustar comandos para usar somente `lib/config`.
- [ ] Remover `core/config*.py` após validação.

### Fase 2 — Migrar Lógicas de API
- [ ] `lib/apis.py`: migrar Pexels (`buscar-imagens.py`) para funções puras (sem subprocess).
- [ ] Migrar Figma (`extrator-figma.py`) com `mode=all|components|css` e baixar com streaming.
- [ ] Migrar Repo (`baixar-repo.py`) e Gemini (consulta/análise) com tratamento de cota/erros.
- [ ] Remover `src/tools/` após migrar e ajustar `commands/*` para chamar `lib/apis` direto.

### Fase 2.5 — UI de Formulários (sem terminal cru)
- [ ] Adicionar componentes de formulário no `lib/ui.py` (inputs, selects, validadores, mensagens de ajuda).
- [ ] Criar telas dedicadas para cada comando (`search`, `figma`, `repo`) e para `config/help/status/costs`.
- [ ] Encadear formulários (wizard simples) quando fizer sentido; botão “Voltar” e “Executar”.
- [ ] Executar ações e exibir progresso/resultados dentro da UI (sem cair no stdout cru).

### Fase 3 — Qualidade, Testes e CI
- [ ] Adicionar type hints + ruff/black/mypy.
- [ ] Testes unitários (mock requests) e smoke tests (offline) p/ cada comando.
- [ ] GitHub Actions: lint, tests, build (wheel + sdist).

### Fase 4 — Empacotamento e DX
- [ ] `pyproject.toml` com `console_scripts = ["cli-tools=src.main:cli"]`.
- [ ] Release sem arquivos grandes (excluir `data/`, `materials/`).
- [ ] Auto‑compleção (Click) e instruções de instalação.

### Fase 5 — Observabilidade e Polimento
- [ ] Logging estruturado (configurável por env) e níveis ajustáveis.
- [ ] Rate limits configuráveis em `config.json`.
- [ ] Melhor UX nas mensagens (`–quiet`, `–json` coerentes).

---

## ✅ Critérios de Aceite
- `cli-tools` instala via pip e roda em Windows/macOS/Linux.
- Todos os comandos funcionam sem subprocess (lib/apis puro).
- Testes passando (unit + smoke offline), CI verde.
- Projeto sem `core/` e `tools/` legados.
- Tamanho do pacote otimizado; sem dados/caches no wheel.

---

## ⚠️ Riscos e Mitigações
- Dependências HTTP externas instáveis → mock e circuit breaker simples.
- Limites de API → configuração de quotas + retries; fail‑soft com mensagens claras.
- Refatoração ampla → migrar em pequenas etapas, manter compatibilidade até a substituição total.

---

## ⏱️ Cronograma Sugerido
- Semana 1: Fase 1 (config) + início Fase 2 (Pexels).
- Semana 2: Fase 2 (Figma/Repo/Gemini) + remoção de tools.
- Semana 3: Fase 3 (tests/CI) + Fase 4 (packaging).
- Semana 4: Fase 5 (observabilidade) + hardening final.

---

## 📌 Observações Finais
- .env criado com placeholders; `data/config.json` inicial pronto.
- UI e comandos já isolados; wrappers de subprocess mantêm compatibilidade até a migração das APIs.
- Após concluir fases 1–2, o projeto ficará significativamente menor e mais manutenível.
