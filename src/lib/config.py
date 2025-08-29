"""
Configuração unificada (.env + data/config.json) e preferências.
"""

import os
import json
from pathlib import Path

DATA_DIR = Path.cwd() / 'data'
DATA_DIR.mkdir(exist_ok=True)
CONFIG_FILE = DATA_DIR / 'config.json'

DEFAULTS = {
    'workspace': str(Path.cwd() / 'materials'),
    'theme': 'transparent',
    'ui_top_pad': 6,
    'apis': {
        'pexels': {'key': None, 'usage': 0},
        'figma': {'token': None, 'usage': 0},
        'gemini': {'key': None, 'usage': 0},
    },
}


def _load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return DEFAULTS.copy()


def _save_config(cfg: dict) -> None:
    try:
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass


def get_api_key(name: str) -> str | None:
    # Env tem prioridade
    env_map = {
        'pexels': 'PEXELS_API_KEY',
        'figma': 'FIGMA_API_TOKEN',
        'gemini': 'GEMINI_API_KEY',
    }
    env_var = env_map.get(name)
    if env_var and os.getenv(env_var):
        return os.getenv(env_var)
    cfg = _load_config()
    item = cfg.get('apis', {}).get(name, {})
    return item.get('key') or item.get('token')


def set_api_key(name: str, value: str) -> None:
    cfg = _load_config()
    if name not in cfg['apis']:
        cfg['apis'][name] = {}
    if name == 'figma':
        cfg['apis'][name]['token'] = value
    else:
        cfg['apis'][name]['key'] = value
    _save_config(cfg)


def get_workspace() -> str:
    cfg = _load_config()
    return cfg.get('workspace', DEFAULTS['workspace'])


def set_workspace(path: str) -> None:
    cfg = _load_config()
    cfg['workspace'] = path
    _save_config(cfg)


def get_theme() -> str:
    # Env tem prioridade
    theme = os.getenv('CLI_THEME')
    if theme in ('transparent', 'dracula'):
        return theme
    cfg = _load_config()
    t = cfg.get('theme', 'transparent')
    return t if t in ('transparent', 'dracula') else 'transparent'


def set_theme(theme: str) -> None:
    if theme not in ('transparent', 'dracula'):
        return
    cfg = _load_config()
    cfg['theme'] = theme
    _save_config(cfg)


def get_ui_top_pad() -> int:
    try:
        return int(os.getenv('CLI_UI_TOP_PAD', '6'))
    except ValueError:
        return 6

