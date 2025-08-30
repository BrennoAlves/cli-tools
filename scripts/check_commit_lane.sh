#!/usr/bin/env bash
set -euo pipefail
MSG_FILE="$1"
if ! grep -Eiq '^lane: (rapido|completo)$' "$MSG_FILE"; then
  echo 'Inclua no commit: "lane: rapido" ou "lane: completo" (linha separada).'
  exit 1
fi

