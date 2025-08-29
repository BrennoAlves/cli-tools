"""
Wrappers de API para comandos. Atualmente delega para scripts existentes
via subprocess para manter compatibilidade durante a migração.

Quando capture=True, retorna (returncode, stdout, stderr) com saída capturada.
Caso contrário, executa direto no terminal e retorna o objeto CompletedProcess.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple, Union, Dict
import hashlib
import json
import time
import requests

from .config import get_api_key, get_workspace

BASE = Path(__file__).parent.parent


def pexels_download(query: str, count: int = 1, output: Optional[str] = None, orientation: Optional[str] = None, json_out: bool = False, capture: bool = False) -> Union[subprocess.CompletedProcess, Tuple[int,str,str]]:
    cmd = [sys.executable, str(BASE / 'tools' / 'buscar-imagens.py'), 'download', query, '--count', str(count)]
    if output:
        cmd += ['--output', output]
    if orientation:
        cmd += ['--orientation', orientation]
    if json_out:
        cmd += ['--format', 'json']
    if capture:
        cp = subprocess.run(cmd, capture_output=True, text=True)
        return cp.returncode, cp.stdout, cp.stderr
    return subprocess.run(cmd)


def _cache_path() -> Path:
    p = BASE.parent / 'data' / 'cache'
    p.mkdir(parents=True, exist_ok=True)
    return p / 'metadata.json'


def _load_cache() -> Dict[str, Dict]:
    cp = _cache_path()
    if cp.exists():
        try:
            return json.loads(cp.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}


def _save_cache(data: Dict[str, Dict]) -> None:
    cp = _cache_path()
    try:
        cp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception:
        pass


def pexels_download_files(query: str, count: int = 1, orientation: Optional[str] = None, output: Optional[str] = None) -> List[Dict]:
    """Busca no Pexels e baixa arquivos direto, sem subprocess. Retorna lista de arquivos baixados."""
    key = get_api_key('pexels')
    if not key:
        raise RuntimeError('PEXELS_API_KEY não configurada')
    headers = {"Authorization": key}
    params = {"query": query, "per_page": max(1, min(count, 80))}
    if orientation:
        params['orientation'] = orientation
    resp = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    photos = data.get('photos', [])

    # Diretório de saída
    if not output:
        category = ''.join(c for c in (query or 'geral') if c.isalnum() or c in ('-','_')).strip('_-') or 'geral'
        output = str(Path(get_workspace()) / 'imagens' / category)
    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)

    cache = _load_cache()
    results: List[Dict] = []
    for i, photo in enumerate(photos, 1):
        url = photo.get('src', {}).get('medium') or photo.get('src', {}).get('original')
        if not url:
            continue
        safe_query = ''.join(c for c in query if c.isalnum() or c in ('-','_')).strip('_-') or 'img'
        name = f"{safe_query}_{i}_{photo.get('id','n')}.webp"
        path = outdir / name
        h = hashlib.md5(url.encode()).hexdigest()[:12]
        # cache hit
        if path.exists() and h in cache:
            meta = cache[h]
            st = path.stat()
            if st.st_size == meta.get('size', 0):
                results.append({"caminho": str(path), "nome": name, "tamanho": f"{st.st_size/(1024*1024):.2f} MB"})
                continue
        # baixa
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        content = r.content
        with open(path, 'wb') as f:
            f.write(content)
        st = path.stat()
        cache[h] = {"url": url, "arquivo": str(path), "size": st.st_size, "mtime": st.st_mtime, "timestamp": time.time()}
        results.append({"caminho": str(path), "nome": name, "tamanho": f"{st.st_size/(1024*1024):.2f} MB"})
    _save_cache(cache)
    return results


def figma_download(file_key: str, fmt: str = 'png', scale: float = 1.0, output: Optional[str] = None, nodes: Optional[List[str]] = None, max_images: int = 5, mode: str = 'all', capture: bool = False) -> Union[subprocess.CompletedProcess, Tuple[int,str,str]]:
    cmd = [sys.executable, str(BASE / 'tools' / 'extrator-figma.py'), 'download', file_key, '--format', fmt, '--scale', str(scale), '--max-images', str(max_images), '--mode', mode]
    if output:
        cmd += ['--output', output]
    if nodes:
        cmd += ['--nodes', ','.join(nodes)]
    if capture:
        cp = subprocess.run(cmd, capture_output=True, text=True)
        return cp.returncode, cp.stdout, cp.stderr
    return subprocess.run(cmd)


def figma_download_files(file_key: str, fmt: str = 'png', scale: float = 1.0, output: Optional[str] = None, nodes: Optional[List[str]] = None, max_images: int = 5, mode: str = 'all') -> List[Dict]:
    """Baixa exports do Figma diretamente, sem subprocess."""
    token = get_api_key('figma')
    if not token:
        raise RuntimeError('FIGMA_API_TOKEN não configurado')
    headers = {"X-Figma-Token": token, "Content-Type": "application/json"}
    base = "https://api.figma.com/v1"

    # info do arquivo
    r = requests.get(f"{base}/files/{file_key}", headers=headers, timeout=30)
    r.raise_for_status()
    info = r.json()
    file_name = (info.get('name') or 'figma').replace(' ', '_')

    # coletar nós se não fornecido
    if not nodes:
        doc = info.get('document', {})
        collect: List[Dict] = []

        def walk(node, parent=""):
            t = node.get('type')
            nid = node.get('id')
            vis = node.get('visible', True)
            if nid and vis:
                collect.append({"id": nid, "type": t, "parent": parent})
            for c in node.get('children', []) or []:
                walk(c, nid)

        walk(doc)
        types = ['FRAME', 'COMPONENT', 'COMPONENT_SET'] if mode != 'components' else ['COMPONENT', 'COMPONENT_SET']
        nodes = [n['id'] for n in collect if n['type'] in types and (n['parent'] == '' or n['parent'] is None)]
        nodes = nodes[:max_images]

    # modo css básico
    if mode == 'css' and not nodes:
        outdir = Path(output) if output else (Path(get_workspace()) / 'figma')
        outdir.mkdir(parents=True, exist_ok=True)
        css_path = outdir / f"{file_name}.css"
        css = ["/* CSS básico gerado */", ":root { --primary: #bd93f9; --accent: #ff79c6; }", ".btn { padding: 8px 12px; border-radius: 6px; }", ""]
        css_path.write_text("\n".join(css), encoding='utf-8')
        return [{"caminho": str(css_path), "nome": css_path.name, "tamanho": f"{css_path.stat().st_size/1024:.1f} KB"}]

    if not nodes:
        return []

    # obter URLs de export
    params = {"format": fmt, "scale": scale, "ids": ",".join(nodes)}
    r = requests.get(f"{base}/images/{file_key}", headers=headers, params=params, timeout=30)
    r.raise_for_status()
    images = r.json().get('images', {})

    outdir = Path(output) if output else (Path(get_workspace()) / 'figma')
    outdir.mkdir(parents=True, exist_ok=True)
    results: List[Dict] = []
    for i, (nid, url) in enumerate(images.items(), 1):
        if not url:
            continue
        name = f"{file_name}_{nid}_{i}.{fmt}"
        path = outdir / name
        rr = requests.get(url, timeout=120)
        rr.raise_for_status()
        with open(path, 'wb') as f:
            f.write(rr.content)
        st = path.stat()
        results.append({"caminho": str(path), "nome": name, "tamanho": f"{st.st_size/(1024*1024):.2f} MB"})
    return results


def repo_download(repo: str, query: Optional[str] = None, output: Optional[str] = None, no_ai: bool = False, all_clone: bool = False, json_out: bool = False, explain: Optional[str] = None, dry_run: bool = False, interactive: bool = False, capture: bool = False) -> Union[subprocess.CompletedProcess, Tuple[int,str,str]]:
    cmd = [sys.executable, str(BASE / 'tools' / 'baixar-repo.py')]
    if all_clone:
        cmd += ['clone', repo]
    elif no_ai or not query:
        cmd += ['clone', repo]
    else:
        cmd += ['smart', repo, query]
    if output:
        cmd += ['--output', output]
    if explain:
        cmd += ['--explain', explain]
    if dry_run:
        cmd += ['--dry-run']
    if interactive:
        cmd += ['--interactive']
    if json_out:
        cmd += ['--json']
    if capture:
        cp = subprocess.run(cmd, capture_output=True, text=True)
        return cp.returncode, cp.stdout, cp.stderr
    return subprocess.run(cmd)


def repo_download_clone_zip(repo: str, output: Optional[str] = None) -> Path:
    """Clona um repositório via ZIP do GitHub para materials/repos/<repo_name>."""
    import zipfile
    owner_repo = repo.strip()
    if '/' not in owner_repo:
        raise RuntimeError('Formato do repositório inválido. Use usuario/repositorio')
    owner, name = owner_repo.split('/', 1)
    url = f"https://api.github.com/repos/{owner}/{name}/zipball"
    outdir = Path(output) if output else (Path(get_workspace()) / 'repos' / name)
    outdir.mkdir(parents=True, exist_ok=True)
    tmpzip = outdir.parent / f"{name}.zip"
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    tmpzip.write_bytes(r.content)
    with zipfile.ZipFile(tmpzip, 'r') as z:
        z.extractall(outdir.parent)
    tmpzip.unlink(missing_ok=True)
    return outdir


def repo_download_auto(repo: str, query: Optional[str] = None, output: Optional[str] = None, no_ai: bool = False, all_clone: bool = False, explain: Optional[str] = None, dry_run: bool = False, interactive: bool = False) -> Path:
    """Escolhe entre clone completo (zip) ou modo "smart" com IA, conforme flags e disponibilidade.
    - Sem IA (no_ai=True) ou sem query → clone_zip
    - Com IA e query + GEMINI_API_KEY → seleção inteligente de arquivos
    """
    if all_clone or no_ai or not query:
        return repo_download_clone_zip(repo, output=output)
    key = get_api_key('gemini')
    if not key:
        return repo_download_clone_zip(repo, output=output)
    try:
        return _repo_download_smart(repo, query=query, output=output, explain=explain, dry_run=dry_run)
    except Exception:
        # fallback em caso de falha de rede/IA
        return repo_download_clone_zip(repo, output=output)


def _github_list_files(repo: str, limit: int = 200) -> List[str]:
    owner, name = repo.split('/', 1)
    url = f"https://api.github.com/repos/{owner}/{name}/git/trees/HEAD?recursive=1"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json()
    files: List[str] = []
    for item in data.get('tree', [])[: max(1, limit)]:
        if item.get('type') == 'blob':
            files.append(item.get('path'))
    return files


def _gemini_select_files(files: List[str], query: str, api_key: str) -> List[str]:
    """Consulta o Gemini com uma lista resumida de arquivos e a query para obter seleção.
    Retorna subset de arquivos (fallback: heurística simples).
    """
    # resumo (limita tamanho)
    sample = files[:200]
    prompt = (
        "Você é um assistente que seleciona arquivos relevantes em um repositório.\n"
        f"Query: {query}\n"
        "Arquivos (um por linha):\n" + "\n".join(sample) + "\n\n"
        "Responda com uma lista JSON de paths relevantes."
    )
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    r = requests.post(f"{url}?key={api_key}", json=body, timeout=60)
    r.raise_for_status()
    obj = r.json()
    text = (
        obj.get('candidates', [{}])[0]
        .get('content', {})
        .get('parts', [{}])[0]
        .get('text', '')
    )
    # tentar extrair JSON
    import re as _re
    import json as _json
    m = _re.search(r"\[(?:.|\n)*\]", text)
    if m:
        try:
            arr = _json.loads(m.group(0))
            return [p for p in arr if isinstance(p, str) and p in files]
        except Exception:
            pass
    # fallback heurístico: substring naive
    q = query.lower()
    return [p for p in files if q in p.lower()][:50]


def _repo_download_smart(repo: str, query: str, output: Optional[str] = None, explain: Optional[str] = None, dry_run: bool = False) -> Path:
    api_key = get_api_key('gemini')
    files = _github_list_files(repo)
    picked = _gemini_select_files(files, query=query, api_key=api_key)
    owner, name = repo.split('/', 1)
    base_raw = f"https://raw.githubusercontent.com/{owner}/{name}/HEAD/"
    outdir = Path(output) if output else (Path(get_workspace()) / 'repos' / name)
    outdir.mkdir(parents=True, exist_ok=True)
    if dry_run:
        # apenas salva a lista selecionada
        (outdir / 'selected_files.json').write_text(json.dumps(picked, indent=2, ensure_ascii=False))
        return outdir
    # baixa arquivos selecionados
    for p in picked:
        url = base_raw + p
        dest = outdir / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        rr = requests.get(url, timeout=60)
        if rr.status_code == 200:
            dest.write_bytes(rr.content)
    return outdir


def run_cli(args: List[str], capture: bool = True) -> Union[subprocess.CompletedProcess, Tuple[int,str,str]]:
    """Executa o CLI principal com args (ex.: ['status','--simple'])."""
    cmd = [sys.executable, '-m', 'src.main'] + args
    if capture:
        cp = subprocess.run(cmd, capture_output=True, text=True)
        return cp.returncode, cp.stdout, cp.stderr
    return subprocess.run(cmd)
