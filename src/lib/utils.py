"""
Utilitários: dashboard e helpers de saída sem dependências do core legado.
"""

import os
from pathlib import Path
from typing import Dict

from .config import get_api_key, get_workspace


def _dir_stats(path: Path) -> Dict[str, float]:
    files = 0
    size = 0
    try:
        for p in path.rglob('*'):
            if p.is_file():
                files += 1
                size += p.stat().st_size
    except Exception:
        pass
    return {"files": files, "size_mb": round(size / (1024 * 1024), 2)}


def get_status_text(simple: bool = True) -> str:
    ws = Path(get_workspace())
    imgs = ws / 'imagens'
    figm = ws / 'figma'
    repos = ws / 'repos'
    for d in (ws, imgs, figm, repos):
        d.mkdir(parents=True, exist_ok=True)

    apis = {
        'pexels': bool(get_api_key('pexels')),
        'figma': bool(get_api_key('figma')),
        'gemini': bool(get_api_key('gemini')),
    }

    s_imgs = _dir_stats(imgs)
    s_figm = _dir_stats(figm)
    s_repos = _dir_stats(repos)
    total_files = s_imgs['files'] + s_figm['files'] + s_repos['files']
    total_mb = round(s_imgs['size_mb'] + s_figm['size_mb'] + s_repos['size_mb'], 2)

    lines = []
    lines.append("📊 Status do Sistema\n")
    lines.append("--- APIs ---")
    for k, ok in apis.items():
        lines.append(f"{'✅' if ok else '❌'} {k}")
    lines.append("")
    lines.append("--- Workspace ---")
    lines.append(f"📁 {ws}")
    lines.append(f"imagens: {s_imgs['files']} arquivos, {s_imgs['size_mb']} MB")
    lines.append(f"figma:   {s_figm['files']} arquivos, {s_figm['size_mb']} MB")
    lines.append(f"repos:   {s_repos['files']} arquivos, {s_repos['size_mb']} MB")
    lines.append(f"TOTAL:   {total_files} arquivos, {total_mb} MB")
    return "\n".join(lines) + "\n"


def show_dashboard(simple: bool = True, live: bool = False):
    # Ignora live por enquanto; imprime texto simples
    print(get_status_text(simple=True))
