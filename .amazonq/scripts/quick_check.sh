#!/usr/bin/env bash
set -euo pipefail

# Lint/format opcionais
if command -v ruff >/dev/null 2>&1; then ruff .; fi
if command -v black >/dev/null 2>&1; then black --check . || true; fi

# Testes (se existir pytest)
if command -v pytest >/dev/null 2>&1; then
  pytest -q || { echo '❌ Testes falharam'; exit 1; }
else
  echo '⚠️  pytest não encontrado — execução apenas de lint/format.'
fi

echo '✅ Quick-check ok'

