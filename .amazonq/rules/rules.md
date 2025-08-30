# 📋 Regras de Desenvolvimento — **CLI Tools v2.4 (duas vias, PT‑BR)**

> Objetivo: **velocidade com segurança**. Duas vias: **Via Rápida** (mudanças pequenas/baixo risco, **sem PR por padrão**) e **Via Completa** (mudanças médias/grandes). Foco no **comportamento obrigatório do agent**.

---

## 1. Duas vias de fluxo

### 🚀 Via Rápida (pequena/baixo risco)

Use quando **todas** as condições forem verdadeiras:

* Até **5 arquivos** alterados **e** até **±50 linhas** no total.
* Mudança **local** (ex.: texto/label/estilo, pequeno handler, documentação, config simples).
* **Sem** alteração de contratos/API, migrations, segurança, performance crítica, scripts de deploy, workflows.

**Fluxo (curto):**

1. **💾 Commit checkpoint** em `dev`.
2. **🔎 Mini‑investigação** (1–3 linhas) + **Miniplano** (1–3 linhas).
3. **❓ Sinal verde rápido**: *"Mudança pequena (via rápida). Posso prosseguir? ✅/❌"*.
4. **✅ Implementar** o miniplano.
5. **🧪 Quick‑check** local (`.amazonq/scripts/quick_check.sh`).
6. **📝 Diário** atualizado.
7. **🔕 IMPORTANTE**: **NUNCA** merge para main. **SEMPRE** commit direto em `dev`.

> **⚠️ REGRA CRÍTICA**: Via Rápida **NUNCA** vai para main automaticamente. Fica na `dev` até ser solicitado merge explícito ou virar Via Completa.

### 🧱 Via Completa (média/alta)

Qualquer item abaixo **ativa** a Via Completa:

* > 5 arquivos ou >±50 linhas; envolve **múltiplos módulos** ou **refactor**.
* Altera **API/contratos**, **migrations**, **segurança**, **desempenho crítico**.
* Modifica **workflows** (`.github/`), **deploy**, **infra**, **scripts**.

**Fluxo (completo):**

1. **💾 Checkpoint** em `dev` → 2) **Investigar** → 3) **Plano**
2. **🛑 Aprovação**: *"Posso prosseguir? ✅/❌"* → 5) **✅ Executar**
3. **📝 Diário** → 7) **🧪 Teste + ✅ do operador** → 8) **🔀 PR** `dev`→`main`
4. **🤖 CI/Auto‑merge** → 10) **📄 Resumo**

---

## 2) Itens **Nunca Fazer** / **Sempre Fazer**

**❌ Nunca**

* Implementar sem aprovação (ambas vias têm gate de aprovação).
* Pular etapas da via escolhida.
* Alterar arquivos **enquanto explica** o plano.

**✅ Sempre**

* Commit checkpoint **antes** de qualquer alteração.
* Investigar (mesmo que breve na Via Rápida).
* Atualizar o **Diário de Bordo** ao final.
* Usar `scratch/` (git‑ignored) para rascunhos/POCs.

**Diário:** `/home/desk/cli-tools/.amazonq/rules/diario_de_bordo.md`

---

## 3) Resumo visual

```
VIA RÁPIDA: Checkpoint → Mini-investigação/Plano → ✅ breve → Implementar → Quick-check → Diário → Commit direto

VIA COMPLETA: Checkpoint → Investigar → Plano → 🛑 Aprovação → Executar → Diário → 🧪 Teste + ✅ do operador → PR → CI/Auto‑merge → Resumo
```
