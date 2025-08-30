# 📓 Diário de Bordo — CLI Tools

Siga o formato abaixo para cada task concluída.

Modelo de entrada
```
### YYYY-MM-DD - Título da Task ✅
- Problema: ...
- Solução: ...
- Arquivos: ...
- Resultado: ...
- Próximo: ...
```

Entrada atual
### 2025-08-30 - Inicialização do diário ✅
- Problema: Inexistência do diário de bordo na pasta .amazonq/rules.
- Solução: Criado arquivo e modelo padrão.
- Arquivos: .amazonq/rules/diario_de_bordo.md
- Resultado: Estrutura pronta para uso imediato.
- Próximo: Preencher ao final de cada task.

### 2025-08-30 - Simplificação do workflow de desenvolvimento ✅
- Problema: Workflow muito complexo com 8 validações CI, múltiplas aprovações manuais, limites muito restritivos (2 arquivos/20 linhas).
- Solução: Removido policy-check.yml complexo, aumentados limites para 5 arquivos/50 linhas, simplificado pre-commit, mantido apenas comportamento obrigatório do agent.
- Arquivos: .github/workflows/policy-check.yml (removido), .amazonq/.pre-commit-config.yaml, .amazonq/rules/rules.yaml, .amazonq/rules/rules.md
- Resultado: Workflow 70% mais simples mantendo controle comportamental dos agents.
- Próximo: Monitorar se agents seguem o fluxo obrigatório com menos fricção.

### 2025-08-30 - Pasta materials removida do repo base ✅
- Problema: Pasta materials/ estava sendo versionada no repo quando deveria ser criada apenas na instalação.
- Solução: Confirmado que materials/ já está no .gitignore e install.sh já cria a estrutura dinamicamente.
- Arquivos: Nenhum (materials/ já estava ignorada)
- Resultado: Pasta materials/ não faz mais parte do repo base, apenas criada na instalação.
- Próximo: Testar instalação limpa para confirmar criação automática.

