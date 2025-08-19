#!/usr/bin/env python3
"""
Controle de uso das APIs para cli-tools
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class ControleUso:
    def __init__(self):
        self.uso_path = Path.home() / '.local/share/cli-tools/uso_apis.json'
        self.uso_data = self._carregar_uso()
    
    def _carregar_uso(self):
        """Carrega dados de uso das APIs"""
        if self.uso_path.exists():
            try:
                with open(self.uso_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Dados padrão
        return {
            'pexels': {'requests_hoje': 0, 'ultimo_reset': datetime.now().isoformat()},
            'figma': {'requests_hoje': 0, 'ultimo_reset': datetime.now().isoformat()},
            'gemini': {'requests_hoje': 0, 'ultimo_reset': datetime.now().isoformat()}
        }
    
    def _salvar_uso(self):
        """Salva dados de uso"""
        self.uso_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.uso_path, 'w') as f:
            json.dump(self.uso_data, f, indent=2)
    
    def _reset_se_necessario(self, api: str):
        """Reseta contador se passou um dia"""
        if api not in self.uso_data:
            self.uso_data[api] = {'requests_hoje': 0, 'ultimo_reset': datetime.now().isoformat()}
            return
        
        ultimo_reset = datetime.fromisoformat(self.uso_data[api]['ultimo_reset'])
        if datetime.now() - ultimo_reset > timedelta(days=1):
            self.uso_data[api]['requests_hoje'] = 0
            self.uso_data[api]['ultimo_reset'] = datetime.now().isoformat()
    
    def registrar_uso(self, api: str, requests: int = 1):
        """Registra uso de uma API"""
        self._reset_se_necessario(api)
        self.uso_data[api]['requests_hoje'] += requests
        self._salvar_uso()
    
    def get_uso_hoje(self, api: str) -> int:
        """Retorna uso de hoje para uma API"""
        self._reset_se_necessario(api)
        return self.uso_data.get(api, {}).get('requests_hoje', 0)
    
    def get_limite(self, api: str) -> int:
        """Retorna limite diário da API"""
        limites = {
            'pexels': 200,  # 200 requests/hora, assumindo uso moderado
            'figma': 1000,  # Limite generoso para API do Figma
            'gemini': 900   # 15 requests/minuto = ~900/hora
        }
        return limites.get(api, 100)
    
    def pode_usar(self, api: str, requests: int = 1) -> bool:
        """Verifica se pode usar a API"""
        uso_atual = self.get_uso_hoje(api)
        limite = self.get_limite(api)
        return uso_atual + requests <= limite
    
    def verificar_limite(self, api: str, requests: int = 1) -> tuple:
        """Verifica limite e retorna (pode_usar, mensagem)"""
        if self.pode_usar(api, requests):
            return True, "OK"
        else:
            uso_atual = self.get_uso_hoje(api)
            limite = self.get_limite(api)
            return False, f"Limite excedido: {uso_atual}/{limite}"
    
    def get_status_todas(self) -> dict:
        """Retorna status de uso de todas as APIs"""
        status = {}
        for api in ['pexels', 'figma', 'gemini']:
            uso = self.get_uso_hoje(api)
            limite = self.get_limite(api)
            status[api] = {
                'uso_hoje': uso,
                'limite': limite,
                'percentual': (uso / limite) * 100 if limite > 0 else 0,
                'pode_usar': self.pode_usar(api)
            }
        return status
    
    def mostrar_dashboard_uso(self):
        """Mostra dashboard de uso das APIs"""
        status = self.get_status_todas()
        
        print(f"\n📊 Dashboard de Uso das APIs:")
        print("=" * 40)
        
        for api, dados in status.items():
            uso = dados['uso_hoje']
            limite = dados['limite']
            percentual = dados['percentual']
            
            # Cor baseada no percentual de uso
            if percentual < 50:
                cor = '\033[92m'  # Verde
            elif percentual < 80:
                cor = '\033[93m'  # Amarelo
            else:
                cor = '\033[91m'  # Vermelho
            
            print(f"{cor}{api.title()}: {uso}/{limite} ({percentual:.1f}%)\033[0m")
        
        print()

def monitorar_custos():
    """Monitora custos e uso das APIs"""
    controle = ControleUso()
    return controle.get_status_todas()

# Alias para compatibilidade
controlador_uso = ControleUso()
