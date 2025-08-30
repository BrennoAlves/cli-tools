#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Instalando pre-commit (se necessário) e configurando hooks..."
if ! command -v pre-commit >/dev/null 2>&1; then
  if command -v pipx >/dev/null 2>&1; then
    pipx install pre-commit || true
  else
    pip install --user pre-commit || true
  fi
fi

CONFIG_PATH=".amazonq/.pre-commit-config.yaml"
pre-commit install --config "$CONFIG_PATH" || true
pre-commit install --config "$CONFIG_PATH" --hook-type commit-msg || true
echo "✅ Hooks instalados."

