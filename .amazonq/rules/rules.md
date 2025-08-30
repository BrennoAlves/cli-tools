# 📋 REGRAS DE DESENVOLVIMENTO - CLI Tools v2.0

## 🚨 **REGRA PRINCIPAL - NUNCA VIOLAR**

### **📋 FLUXO OBRIGATÓRIO PARA TODA TASK:**

1. **💾 COMMIT** - Commitar estado atual na branch dev ANTES de qualquer alteração
2. **🔍 INVESTIGAR** - Verificar arquivos e entender o problema
3. **📋 PLANO** - Criar plano de ação estruturado  

🛑 **STOP POINT OBRIGATÓRIO** 🛑

4. **❓ APROVAÇÃO** - Pedir aprovação explícita ("Posso prosseguir? ✅/❌")
5. **⏳ AGUARDAR** - NÃO fazer nada sem ver "✅" ou "aprovado"

🛑 **SÓ CONTINUAR APÓS APROVAÇÃO** 🛑

6. **✅ EXECUTAR** - Implementar após aprovação
7. **📝 DOCUMENTAR** - Atualizar diário de bordo

### **🚫 NUNCA FAZER:**
- Implementar sem aprovação
- Pular etapas "por ser simples"
- Fazer alterações "enquanto explica"
- Prosseguir sem confirmação explícita
- **Deixar arquivos de teste temporários no projeto**

### **✅ SEMPRE FAZER:**
- **Commitar na dev ANTES de qualquer alteração**
- Investigar antes de propor
- Aguardar aprovação explícita
- **Atualizar diário de bordo no final de TODA task**
- **Deletar arquivos test_*.py e test_*.html temporários após uso**
- **SEMPRE usar SSH para clone de repositórios**

### **🧠 LEMBRETE COMPORTAMENTAL:**
- **PARE** após criar o plano
- **PERGUNTE** "Posso prosseguir? ✅/❌"  
- **AGUARDE** resposta explícita
- **NÃO implemente** por impulso

---

## 📝 **REGRA DE DOCUMENTAÇÃO OBRIGATÓRIA**

### **📋 APÓS COMPLETAR QUALQUER TASK:**

**⚠️ SEMPRE ATUALIZAR O DIÁRIO DE BORDO ⚠️**

**Formato obrigatório:**
```markdown
### YYYY-MM-DD - Título da Task ✅
- **Problema:** O que foi solicitado
- **Solução:** O que foi implementado
- **Arquivos:** Lista de arquivos modificados
- **Resultado:** Status final
- **Próximo:** Próximos passos
```

**Localização:** `/home/desk/cli-tools/.amazonq/rules/diario_de_bordo.md`

---

## 🔐 **REGRA DE CLONE SSH OBRIGATÓRIA**

### **📋 SEMPRE USAR SSH PARA REPOSITÓRIOS:**

**✅ Formato correto:**
```bash
git clone git@github.com:usuario/repositorio.git
```

**❌ NUNCA usar HTTPS:**
```bash
git clone https://github.com/usuario/repositorio.git  # ❌ PROIBIDO
```

**Motivos:**
- Autenticação automática via chave SSH
- Maior segurança
- Não requer token/senha
- Padrão para desenvolvimento profissional

---

## 💾 **REGRA DE COMMIT OBRIGATÓRIA**

### **📋 WORKFLOW DE COMMIT:**

1. **Sempre trabalhar na branch `dev`**
2. **Commitar TODA implementação completa**
3. **Usar mensagens descritivas**
4. **Documentar pendências conhecidas**

**Formato de commit:**
```bash
git add arquivos_relevantes
git commit -m "tipo: descrição concisa

- Funcionalidade implementada
- Arquivos modificados
- Melhorias aplicadas

Pendências:
- Problema conhecido 1
- Problema conhecido 2"
```

---

## 🛠️ **STACK TECNOLÓGICA**


- **Tema:** Dracula (#bd93f9, #8be9fd, #50fa7b)

### **🚫 TECNOLOGIAS PROIBIDAS:**
- HTTPS para clone (usar SSH)
---

## 🎯 **OBJETIVO DO PROJETO**

**CLI Tools v2.0 - Kit de ferramentas para desenvolvedores:**
- Busca de imagens (Pexels API)
- Extração de designs (Figma API)
- Download inteligente de repositórios (GitHub + IA)
- Interface moderna com navegação por setas
- Dual mode: Humanos (UI) + Agents (CLI)

---

## 📁 **ESTRUTURA DE ARQUIVOS**

**Projeto Principal:** `/home/desk/cli-tools/`
**Documentação:** `/home/desk/cli-tools/.amazonq/`
**Diário de Bordo:** `/home/desk/cli-tools/.amazonq/rules/diario_de_bordo.md`

---

## 🔄 **WORKFLOW RESUMIDO**

```
COMMIT → TASK → Investigar → Plano → Aprovação → Implementar → Documentar
```

**⚠️ NUNCA pular etapas! ⚠️**

---

## 📋 **CHECKLIST OBRIGATÓRIO**

Antes de finalizar qualquer task:

- [ ] Commit do estado atual realizado ✅
- [ ] Investigação realizada ✅
- [ ] Plano aprovado pelo gerente ✅  
- [ ] Implementação completa ✅
- [ ] Diário de bordo atualizado ✅
- [ ] Próximos passos definidos ✅

---

## 🔁 Atualização de Fluxo — Integração e Deploy (2025‑08‑30)

- Testes automatizados rodam apenas na branch `dev` (workflow `CI`).
- O `CI` dispara somente em Pull Requests com base na `main` (gatilho `pull_request` para `main`).
- A branch `main` é protegida e exige:
  - PR obrigatório (sem push direto) e histórico linear;
  - Status check obrigatório: `CI` aprovado (strict/up-to-date);
  - Conversas resolvidas antes de merge.
- Auto‑merge por squash está habilitado: ao ficar verde, o PR é mesclado automaticamente.
- Documentação interna (`.amazonq/`) deve existir apenas na `dev`. Se alguma cópia surgir na `main`, remova no PR.

Fluxo prático:
1) Trabalhe na `dev` (ou branch criada a partir de `dev`).
2) Abra PR para `main`.
3) Aguarde o `CI` passar.
4) Auto‑merge executa o squash automaticamente quando o `CI` ficar verde.

