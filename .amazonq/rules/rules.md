# 📋 Regras de Desenvolvimento — **CLI Tools v2.3 (duas vias, PT‑BR)**

> Objetivo: **velocidade com segurança**. Agora há duas vias de trabalho: **Via Rápida** (mudanças pequenas/baixo risco, **sem PR por padrão**) e **Via Completa** (mudanças médias/grandes). Abertura de PR só quando **solicitado** ou quando for **atualização grande**.

---

## 1. Duas vias de fluxo

### 🚀 Via Rápida (pequena/baixo risco)

Use quando **todas** as condições forem verdadeiras:

* Até **2 arquivos** alterados **e** até **±20 linhas** no total.
* Mudança **local** (ex.: texto/label/estilo de botão, pequeno handler, cópia, layout pontual).
* **Sem** alteração de contratos/API, migrations, segurança, performance crítica, scripts de deploy, workflows, libs core, componentes compartilhados sensíveis.
* **Sem** mudanças em `.github/` nem em `.amazonq/` (exceto o **Diário**).

**Fluxo (curto):**

1. **💾 Commit checkpoint** em `dev`.
2. **🔎 Mini‑investigação** (1–3 linhas) + **Miniplano** (1–3 linhas).
3. **❓ Sinal verde rápido**: *“Mudança pequena (via rápida). Posso prosseguir? ✅/❌”*.
4. **✅ Implementar** o miniplano.
5. **🧪 Quick‑check** local (`./scripts/quick_check.sh`).
6. **📝 Diário** atualizado.
7. **🔕 PR**: **não abrir** por padrão. Abra **somente se solicitado** pelo operador/gerente **ou** se a mudança deixar de ser pequena.
8. (Opcional, se solicitado) **Teste do operador**: fornecer passos curtos; aguardar **“✅ testado ok”**.

> **Exemplo**: “Atualizar texto e ícone do botão ‘Salvar’ em `src/ui/Button.tsx`” → **Via Rápida**.

---

### 🧱 Via Completa (média/alta)

Qualquer item abaixo **ativa** a Via Completa:

* > 2 arquivos ou >±20 linhas; envolve **componentes compartilhados**, **múltiplos módulos** ou **refactor**.
* Altera **API/contratos**, **migrations**, **segurança** (auth/segredos), **desempenho crítico**.
* Modifica **workflows** (`.github/`), **deploy**, **infra**, **scripts**.
* Solicitação explícita para abrir PR.

**Fluxo (completo):**

1. **💾 Checkpoint** em `dev` → 2) **Investigar** → 3) **Plano**
2. **🛑 Aprovação**: *“Posso prosseguir? ✅/❌”* → 5) **✅ Executar**
3. **📝 Diário** → 7) **🧪 Teste (plano claro) e validação do operador** → 8) **🔀 Abrir PR** `dev`→`main` (**somente aqui**)
4. **🤖 CI/Auto‑merge** (squash quando verde) → 10) **🔎 Verificação pós‑merge (GH CLI)**
5. **📄 Resumo curto** do que foi feito.

---

## 2) Itens **Nunca Fazer** / **Sempre Fazer**

**❌ Nunca**

* Implementar sem aprovação (Via Rápida tem aprovação curta, mas **tem** gate).
* Pular etapas da via escolhida.
* Alterar arquivos **enquanto explica** o plano.
* Deixar artefatos temporários versionados.

**✅ Sempre**

* Commit checkpoint **antes** de qualquer alteração.
* Investigar (mesmo que breve na Via Rápida).
* Atualizar o **Diário de Bordo** ao final.
* **SSH** para clone (nunca HTTPS).
* Usar `scratch/` (git‑ignored) para rascunhos/POCs.

**Diário:** `/home/desk/cli-tools/.amazonq/rules/diario_de_bordo.md`

Formato:

```markdown
### YYYY-MM-DD - Título da Task ✅
- **Problema:** ...
- **Solução:** ...
- **Arquivos:** ...
- **Resultado:** ...
- **Próximo:** ...
```

---

## 3) Política **machine‑readable** (para agents) — `.amazonq/rules/rules.yaml`

```yaml
versao: 2.3
vias:
  rapida:
    max_arquivos: 2
    max_linhas_totais: 20
    require_pr: false
    require_teste_operador: false
    permitido:
      - ui/texto/estilo pontual
      - pequenos handlers locais
    proibido:
      - api/contratos
      - migrations
      - seguranca/segredos
      - desempenho_critico
      - workflows/.github
      - deploy/infra/scripts
      - componentes_compartilhados
  completa:
    require_pr: true
    require_teste_operador: true
    label_pr: "lane: full"

aprovacao:
  tokens:
    - "✅"
    - "aprovado"
  teste_tokens:
    - "✅ testado ok"
    - "aprovado para PR"

comportamento_agent:
  respostas:
    - "## Investigação"
    - "## Plano"
    - "## Pedido de aprovação: Posso prosseguir? ✅/❌"
    - "## Plano de Testes (se via completa ou se solicitado)"
    - "## Pedido de aprovação de testes: Pronto para testar? ✅/❌ (via completa)"
  hard_stop:
    antes_de_executar: true
    antes_de_abrir_pr: true

convencoes:
  diario: 
    - ".amazonq/rules/diario_de_bordo.md"
  scratch:
    - "scratch/"
  code_globs:
    - "**/*.py"
    - "**/*.ts"
    - "**/*.tsx"
    - "**/*.js"
    - "**/*.sh"
    - "**/*.go"
    - "**/*.rs"
```

> **Como o agent decide a via**: se exceder limites ou cair em proibidos → **Completa**. Caso contrário → **Rápida** (sem PR por padrão). Sempre pedir sinal verde curto.

---

## 4) Automação de **enforcement**

### 4.1 Pre‑commit — `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.5.5
    hooks:
      - id: ruff
  - repo: https://github.com/pre-commit/pygrep-hooks
    rev: v1.10.0
    hooks:
      - id: text-unicode-replacement-char
  - repo: local
    hooks:
      - id: forbid-https-github
        name: proibir https do github (use SSH)
        entry: bash -c 'if git grep -n "https://github.com/" -- . >/dev/null; then echo "Use SSH (git@github.com:...)"; exit 1; fi'
        language: system
        pass_filenames: false
      - id: forbid-scratch-commits
        name: proibir versionar scratch/
        entry: bash -c 'if git ls-files -- scratch/ | grep -q .; then echo "Não versione scratch/"; exit 1; fi'
        language: system
        pass_filenames: false
```

**Instalação:**

```bash
pipx install pre-commit || pip install pre-commit
pre-commit install
```

### 4.2 Commit‑msg (exigir indicação da via) — `scripts/check_commit_lane.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
MSG_FILE="$1"
if ! grep -Eiq '^lane: (rapido|completo)$' "$MSG_FILE"; then
  echo 'Inclua no commit: "lane: rapido" ou "lane: completo" (linha separada).';
  exit 1
fi
```

Adicionar ao pre‑commit (estágio `commit-msg`):

```yaml
  - repo: local
    hooks:
      - id: require-commit-lane
        name: exigir lane no commit
        entry: scripts/check_commit_lane.sh
        language: system
        stages: [commit-msg]
```

**Exemplo de commit (Via Rápida):**

```git
feat(ui): ajusta label do botão "Salvar"
lane: rapido
```

### 4.3 Template de PR — `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Checklist
- [ ] Via **Completa**
- [ ] Plano escrito; execução **após** ✅/aprovado
- [ ] Plano de Testes e **✅ testado ok** (operador)
- [ ] Diário atualizado
- [ ] Sem `scratch/` versionado
- [ ] Sem `https://github.com` (SSH only)

> Marque o PR com o **label**: `lane: full`

## Plano
(arquivos, passos, riscos)

## Plano de Testes
(passos + critérios de aceitação)
```

### 4.4 CODEOWNERS — `.github/CODEOWNERS`

```
* @seu-usuario-github
```

### 4.5 GitHub Action — **policy-check** — `.github/workflows/policy-check.yml`

```yaml
name: policy-check
on:
  pull_request:
    branches: [ main ]
permissions:
  contents: read
  pull-requests: write
  issues: read
jobs:
  policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - name: Diff da base
        id: diff
        run: |
          git fetch origin ${{ github.base_ref }} --depth=1
          echo "files=$(git diff --name-only FETCH_HEAD...HEAD | tr '
' ' ' )" >> $GITHUB_OUTPUT
      - name: Proibir HTTPS do GitHub
        run: |
          if git grep -n "https://github.com/" -- . >/dev/null; then
            echo "Use SSH (git@github.com:...)"; exit 1; fi
      - name: Proibir scratch/ versionado
        run: |
          CHANGED="${{ steps.diff.outputs.files }}"
          echo "$CHANGED" | tr ' ' '
' | grep '^scratch/' && { echo 'Não versione scratch/'; exit 1; } || true
      - name: Bloquear .amazonq na main
        if: github.base_ref == 'main'
        run: |
          echo "${{ steps.diff.outputs.files }}" | tr ' ' '
' | grep '^.amazonq/' && { echo '.amazonq/ deve ficar na dev'; exit 1; } || true
      - name: Exigir atualização do Diário quando há código
        run: |
          CHANGED_FILES=$(echo "${{ steps.diff.outputs.files }}" | tr ' ' '
')
          CODE_CHANGED=$(echo "$CHANGED_FILES" | grep -E '\.(py|ts|tsx|js|sh|go|rs)$' || true)
          if [ -n "$CODE_CHANGED" ]; then
            echo "$CHANGED_FILES" | grep -q "^\.amazonq/rules/diario_de_bordo.md$" || { echo 'Atualize o Diário'; exit 1; }
          fi
      - name: Exigir token de aprovação de implementação (comentários)
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PR=${{ github.event.pull_request.number }}
          REPO=${{ github.repository }}
          gh api repos/$REPO/issues/$PR/comments --paginate | jq -r '.[].body' | grep -Ei '(^| )✅($| )|aprovado' >/dev/null || {
            echo 'É necessário comentário de aprovação (✅/aprovado).'; exit 1; }
      - name: Exigir **label** de via completa
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PR=${{ github.event.pull_request.number }}
          REPO=${{ github.repository }}
          gh pr view $PR --repo $REPO --json labels -q '.labels[].name' | grep -Fx 'lane: full' >/dev/null || {
            echo 'Adicione o label do PR: "lane: full" (PRs são só para via completa ou quando solicitados).'; exit 1; }
      - name: Exigir aprovação de testes do operador (PR body)
        run: |
          BODY='${{ github.event.pull_request.body }}'
          echo "$BODY" | grep -Ei '(✅ testado ok|aprovado para PR)' >/dev/null || {
            echo 'Inclua no corpo do PR a aprovação de testes do operador (✅ testado ok / aprovado para PR).'; exit 1; }
```

> Observação: este workflow só atua **em PRs para `main`**. Na **Via Rápida**, como não há PR por padrão, o enforcement fica **local** (pre‑commit + disciplina de Diário).

---

## 5) Quick‑check local — `scripts/quick_check.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# Lint/format
if command -v ruff >/dev/null 2>&1; then ruff .; fi
if command -v black >/dev/null 2>&1; then black --check . || true; fi

# Testes (se existir pytest)
if command -v pytest >/dev/null 2>&1; then pytest -q || { echo '❌ Testes falharam'; exit 1; }; else
  echo '⚠️  pytest não encontrado — execução apenas de lint/format.'
fi

echo '✅ Quick-check ok'
```

---

## 6) `.gitignore`

```gitignore
scratch/
*.tmp
*.tmp.*
.q-cache/
```

---

## 7. Verificação pós‑merge (apenas Via Completa) — `scripts/verifica_auto_merge.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
PR_NUMBER="${1:-$(gh pr view --json number -q .number)}"
echo "Checando PR #$PR_NUMBER em $REPO..."
for i in {1..40}; do
  STATE=$(gh pr view "$PR_NUMBER" --json state -q .state)
  MERGED_AT=$(gh pr view "$PR_NUMBER" --json mergedAt -q .mergedAt)
  if [ "$STATE" = "MERGED" ] && [ -n "$MERGED_AT" ]; then
    echo "✅ Auto-merged em $MERGED_AT"; exit 0; fi
  echo "Aguardando auto-merge… ($i)"; sleep 15
done

gh pr view "$PR_NUMBER" --json state,mergeable,mergeStateStatus,headRefName,baseRefName | jq .
echo "❌ Não houve auto-merge. Verifique CI/proteções e volte ao passo 2 (Investigar)."
exit 1
```

---

## 8. Anti‑sinais de IA & identidade do autor

**Propósito**: não dar pinta de IA e garantir que **toda autoria** apareça no **seu nome**.

### Regras práticas

* **Commits**: sempre **curtos e práticos em português** (assunto ≤ 72 caracteres, sem ponto final). Evite frases de IA (ex.: “auto-generated”, “generated by”, “agent”, “AI assistant”, “ChatGPT”, “Copilot”, “Amazon Q”, “LLM”).
* **Código legível**: estruturas simples, funções curtas, nomes claros. **Sem comentários prolixos** ou colar prompts.
* **Comentários de linha**: usar `//comentario` **sem espaço** após `//` (ex.: `//ok`, não `// ok`).
* **Identidade**: usar **Git/GitHub CLI** sempre no seu usuário para commits/PRs (nada de “agent tal”).

### Configuração recomendada (uma vez)

```bash
git config --global user.name "SEU_NOME"
git config --global user.email "seu@email"
# GitHub CLI
gh auth login
```

---

## 8. Resumo visual

```
VIA RÁPIDA: Checkpoint → Mini-investigação/Plano → ✅ breve → Implementar → Quick-check → Diário → (sem PR por padrão)

VIA COMPLETA: Checkpoint → Investigar → Plano → 🛑 Aprovação → Executar → Diário → 🧪 Teste + ✅ do operador → PR → CI/Auto‑merge → Verificação GH CLI → Resumo
```
