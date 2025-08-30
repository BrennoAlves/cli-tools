# 📋 Regras Simplificadas — **CLI Tools v3.0**

> **Objetivo:** Velocidade máxima com controle mínimo. Sem PRs, sem fricção.

---

## 1. Fluxo Único Simplificado

### 🚀 Baixo Impacto (direto na dev)
- Até **5 arquivos** e **±50 linhas**
- Mudanças locais: texto, estilo, docs, configs simples
- **Sem** API, migrations, segurança, workflows

**Fluxo:**
1. **💾 Checkpoint** em `dev`
2. **🔎 Investigação** + **Plano**
3. **❓ Aprovação OBRIGATÓRIA**: "Posso prosseguir? ✅/❌"
4. **✅ Implementar** (só após aprovação)
5. **🧪 Quick-check** local
6. **📝 Diário**
7. **💾 Commit direto** em `dev`

### 🧱 Alto Impacto (dev → teste → main → GitHub)
- Qualquer coisa > 5 arquivos/50 linhas
- API, migrations, segurança, workflows
- Múltiplos módulos, refactors

**Fluxo:**
1. **🔄 Sync**: `git checkout main && git merge dev` (antes de começar)
2. **💾 Checkpoint** em `dev`
3. **🔎 Investigação** + **Plano**
4. **❓ Aprovação OBRIGATÓRIA**: "Posso prosseguir? ✅/❌"
5. **✅ Implementar** na `dev` (só após aprovação)
6. **📝 Diário**
7. **🧪 Teste do operador OBRIGATÓRIO**: "✅ testado ok"
8. **🔄 Merge**: `git checkout main && git merge dev`
9. **📤 Push**: `git push origin main`

---

## 2. Checklist para IAs

**TODAS as tasks precisam:**
- [ ] **Aprovação do operador** (✅/❌) - OBRIGATÓRIO
- [ ] Pasta `.amazonq/` não está sendo versionada
- [ ] Diário atualizado
- [ ] Quick-check passou (baixo impacto)
- [ ] **Teste do operador passou** (alto impacto) - OBRIGATÓRIO

**Nunca fazer:**
- Implementar sem aprovação do operador
- Versionar `.amazonq/`
- Pular etapas do fluxo
- Mergear alto impacto sem teste do operador

---

## 3. Comandos Úteis

```bash
# Quick-check local
.amazonq/scripts/quick_check.sh

# Sync dev → main (alto impacto)
git checkout main && git merge dev

# Push para GitHub (alto impacto)
git push origin main

# Status
git status && git log --oneline -5
```

**Diário:** `.amazonq/rules/diario_de_bordo.md`
