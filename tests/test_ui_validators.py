"""Testes para validadores da UI."""
import pytest

from src.lib.ui import validate_query, validate_count, validate_figma_key, validate_repo


class TestValidators:
    """Testes para funções de validação."""
    
    def test_validate_query_valid(self):
        """Testa validação de query válida."""
        is_valid, msg = validate_query("office desk")
        assert is_valid is True
        assert msg == ""
    
    def test_validate_query_empty(self):
        """Testa validação de query vazia."""
        is_valid, msg = validate_query("")
        assert is_valid is False
        assert "não pode estar vazia" in msg
    
    def test_validate_query_too_short(self):
        """Testa validação de query muito curta."""
        is_valid, msg = validate_query("a")
        assert is_valid is False
        assert "pelo menos 2 caracteres" in msg
    
    def test_validate_count_valid(self):
        """Testa validação de count válido."""
        is_valid, msg = validate_count("5")
        assert is_valid is True
        assert msg == ""
    
    def test_validate_count_invalid_number(self):
        """Testa validação de count inválido."""
        is_valid, msg = validate_count("abc")
        assert is_valid is False
        assert "Deve ser um número" in msg
    
    def test_validate_count_too_low(self):
        """Testa validação de count muito baixo."""
        is_valid, msg = validate_count("0")
        assert is_valid is False
        assert "maior que 0" in msg
    
    def test_validate_count_too_high(self):
        """Testa validação de count muito alto."""
        is_valid, msg = validate_count("100")
        assert is_valid is False
        assert "Máximo 80" in msg
    
    def test_validate_figma_key_valid(self):
        """Testa validação de figma key válida."""
        is_valid, msg = validate_figma_key("abcdefghij1234567890")
        assert is_valid is True
        assert msg == ""
    
    def test_validate_figma_key_empty(self):
        """Testa validação de figma key vazia."""
        is_valid, msg = validate_figma_key("")
        assert is_valid is False
        assert "não pode estar vazio" in msg
    
    def test_validate_figma_key_too_short(self):
        """Testa validação de figma key muito curta."""
        is_valid, msg = validate_figma_key("abc")
        assert is_valid is False
        assert "muito curto" in msg
    
    def test_validate_repo_valid(self):
        """Testa validação de repo válido."""
        is_valid, msg = validate_repo("facebook/react")
        assert is_valid is True
        assert msg == ""
    
    def test_validate_repo_empty(self):
        """Testa validação de repo vazio."""
        is_valid, msg = validate_repo("")
        assert is_valid is False
        assert "não pode estar vazio" in msg
    
    def test_validate_repo_no_slash(self):
        """Testa validação de repo sem barra."""
        is_valid, msg = validate_repo("facebook")
        assert is_valid is False
        assert "Formato: usuario/repositorio" in msg
    
    def test_validate_repo_empty_parts(self):
        """Testa validação de repo com partes vazias."""
        is_valid, msg = validate_repo("/react")
        assert is_valid is False
        assert "Formato: usuario/repositorio" in msg
