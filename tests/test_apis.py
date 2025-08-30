"""Testes para APIs."""
import pytest
from unittest.mock import patch, Mock, MagicMock
import requests

from src.lib.apis import pexels_download_files, figma_download_files


class TestPexelsAPI:
    """Testes para Pexels API."""
    
    @patch('src.lib.apis.get_api_key')
    @patch('src.lib.apis.requests.get')
    @patch('src.lib.apis.get_workspace')
    def test_pexels_download_success(self, mock_workspace, mock_get, mock_key):
        """Testa download bem-sucedido do Pexels."""
        # Setup mocks
        mock_key.return_value = 'test_key'
        mock_workspace.return_value = '/tmp/test'
        
        mock_response = Mock()
        mock_response.json.return_value = {
            'photos': [{
                'id': '123',
                'src': {'medium': 'http://test.com/image.jpg'}
            }]
        }
        mock_response.raise_for_status.return_value = None
        
        # Mock para download da imagem
        mock_image_response = Mock()
        mock_image_response.content = b'fake_image_data'
        mock_image_response.raise_for_status.return_value = None
        
        mock_get.side_effect = [mock_response, mock_image_response]
        
        with patch('src.lib.apis.Path.mkdir'), \
             patch('builtins.open', create=True), \
             patch('src.lib.apis.Path.stat') as mock_stat, \
             patch('src.lib.apis._load_cache', return_value={}), \
             patch('src.lib.apis._save_cache'):
            
            mock_stat.return_value.st_size = 1024
            
            result = pexels_download_files('test query', count=1)
            
            assert len(result) == 1
            assert 'nome' in result[0]
            assert 'tamanho' in result[0]
    
    @patch('src.lib.apis.get_api_key')
    def test_pexels_no_api_key(self, mock_key):
        """Testa erro quando não há chave API."""
        mock_key.return_value = None
        
        with pytest.raises(RuntimeError, match='PEXELS_API_KEY não configurada'):
            pexels_download_files('test')


class TestFigmaAPI:
    """Testes para Figma API."""
    
    @patch('src.lib.apis.get_api_key')
    def test_figma_no_api_key(self, mock_key):
        """Testa erro quando não há token Figma."""
        mock_key.return_value = None
        
        with pytest.raises(RuntimeError, match='FIGMA_API_TOKEN não configurado'):
            figma_download_files('test_key')
    
    @patch('src.lib.apis.get_api_key')
    @patch('src.lib.apis.requests.get')
    def test_figma_api_error(self, mock_get, mock_key):
        """Testa erro de API do Figma."""
        mock_key.return_value = 'test_token'
        
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError('API Error')
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.HTTPError):
            figma_download_files('test_key')
