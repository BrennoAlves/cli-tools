"""Testes para configuração."""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open

from src.lib.config import get_api_key, get_workspace, get_theme, set_api_key


def test_get_api_key_from_env():
    """Testa obtenção de chave da env."""
    with patch.dict(os.environ, {'PEXELS_API_KEY': 'test_key'}):
        key = get_api_key('pexels')
        assert key == 'test_key'


def test_get_api_key_missing():
    """Testa chave ausente."""
    with patch.dict(os.environ, {}, clear=True):
        with patch('src.lib.config._load_config', return_value={'apis': {}}):
            key = get_api_key('nonexistent')
            assert key is None


def test_set_api_key():
    """Testa definição de chave API."""
    with patch('src.lib.config._load_config', return_value={'apis': {}}), \
         patch('src.lib.config._save_config') as mock_save:
        set_api_key('test', 'value')
        mock_save.assert_called_once()


def test_get_workspace():
    """Testa obtenção do workspace."""
    workspace = get_workspace()
    assert isinstance(workspace, str)
    assert 'materials' in workspace


def test_get_theme_from_env():
    """Testa obtenção de tema da env."""
    with patch.dict(os.environ, {'CLI_THEME': 'dracula'}):
        theme = get_theme()
        assert theme == 'dracula'


def test_get_theme_default():
    """Testa tema padrão."""
    with patch.dict(os.environ, {}, clear=True):
        with patch('src.lib.config._load_config', return_value={}):
            theme = get_theme()
            assert theme == 'transparent'
