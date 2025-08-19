#!/usr/bin/env python3
"""
Configuração de APIs para cli-tools
"""
import os
from pathlib import Path
from dotenv import load_dotenv

class ConfigAPI:
    def __init__(self):
        # Carregar variáveis do .env
        env_path = Path.home() / '.local/share/cli-tools/.env'
        if env_path.exists():
            load_dotenv(env_path)
        
        self.pexels_key = os.getenv('PEXELS_API_KEY')
        self.figma_token = os.getenv('FIGMA_API_TOKEN')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
    
    def tem_pexels(self):
        return bool(self.pexels_key)
    
    def tem_figma(self):
        return bool(self.figma_token)
    
    def tem_gemini(self):
        return bool(self.gemini_key)

def validar_chaves_api():
    """Valida se as chaves de API estão configuradas"""
    config = ConfigAPI()
    
    problemas = {}
    
    if not config.tem_pexels():
        problemas['pexels'] = "Chave não configurada"
    
    if not config.tem_figma():
        problemas['figma'] = "Token não configurado"
    
    if not config.tem_gemini():
        problemas['gemini'] = "Chave não configurada"
    
    return problemas
