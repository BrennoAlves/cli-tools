#!/usr/bin/env python3
"""
Configuração de APIs para cli-tools
"""
import os
from pathlib import Path
from dotenv import load_dotenv

class ConfigAPI:
    def __init__(self):
        # Carregar variáveis do .env com múltiplas tentativas
        current_dir = Path.cwd()
        
        # Lista de possíveis locais para .env (em ordem de prioridade)
        possible_envs = []
        
        # 1. .env no diretório atual
        possible_envs.append(current_dir / '.env')
        
        # 2. Se estivermos em qualquer subdiretório de cli-tools
        search_dir = current_dir
        for _ in range(10):  # máximo 10 níveis
            if search_dir.name == 'cli-tools':
                possible_envs.append(search_dir / '.env')
                break
            if search_dir.parent == search_dir:  # chegou na raiz
                break
            search_dir = search_dir.parent
        
        # 3. Verificar se há cli-tools no path atual
        if 'cli-tools' in str(current_dir):
            # Tentar encontrar o diretório cli-tools
            parts = Path(current_dir).parts
            for i, part in enumerate(parts):
                if part == 'cli-tools':
                    cli_tools_path = Path(*parts[:i+1])
                    possible_envs.append(cli_tools_path / '.env')
                    break
        
        # 4. .env da instalação
        possible_envs.append(Path(__file__).parent.parent.parent / '.env')
        
        # 5. .env global
        possible_envs.append(Path.home() / '.local/share/cli-tools/.env')
        
        # Carregar o primeiro .env encontrado
        env_loaded = False
        for env_path in possible_envs:
            if env_path.exists():
                load_dotenv(env_path)
                env_loaded = True
                break
        
        # Se não encontrou nenhum .env, tentar carregar variáveis do ambiente
        if not env_loaded:
            # Tentar carregar do ambiente do sistema
            pass
        
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
