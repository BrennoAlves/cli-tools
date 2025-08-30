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

gh pr view "$PR_NUMBER" --json state,mergeable,mergeStateStatus,headRefName,baseRefName | jq . || true
echo "❌ Não houve auto-merge. Verifique CI/proteções e volte ao passo 2 (Investigar)."
exit 1

