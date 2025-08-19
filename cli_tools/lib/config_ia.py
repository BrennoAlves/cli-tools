#!/usr/bin/env python3
"""
Configuração da IA para cli-tools
"""
import os
import json
from enum import Enum
from pathlib import Path

class NivelExplicacao(Enum):
    SILENCIOSO = "silencioso"
    BASICO = "basico"
    DETALHADO = "detalhado"
    DEBUG = "debug"

class ConfigIA:
    def __init__(self):
        self.config_path = Path.home() / '.local/share/cli-tools/ia_config.json'
        self.config = self._carregar_config()
    
    def _carregar_config(self):
        """Carrega configuração da IA"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Configuração padrão
        return {
            'nivel_explicacao': NivelExplicacao.BASICO.value,
            'interface_moderna': True,
            'auto_confirmar': False
        }
    
    def salvar_config(self):
        """Salva configuração da IA"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_nivel_explicacao(self):
        """Retorna o nível de explicação atual"""
        return NivelExplicacao(self.config.get('nivel_explicacao', NivelExplicacao.BASICO.value))
    
    def set_nivel_explicacao(self, nivel: NivelExplicacao):
        """Define o nível de explicação"""
        self.config['nivel_explicacao'] = nivel.value
        self.salvar_config()

def config_ia():
    """Configura o comportamento da IA"""
    from .interface import InterfaceLimpa
    
    interface = InterfaceLimpa()
    config = ConfigIA()
    
    interface.print_titulo("🤖 Configuração da IA")
    
    print("A IA pode explicar suas decisões em diferentes níveis:")
    print("• Silencioso - Só mostrar resultado")
    print("• Básico - Resultado + resumo (recomendado)")
    print("• Detalhado - Mostrar processo completo")
    print("• Debug - Tudo + informações técnicas")
    
    # Simulação de seleção (sem biblioteca externa)
    print(f"\nNível atual: {config.get_nivel_explicacao().value}")
    
    opcoes = {
        '1': NivelExplicacao.SILENCIOSO,
        '2': NivelExplicacao.BASICO,
        '3': NivelExplicacao.DETALHADO,
        '4': NivelExplicacao.DEBUG
    }
    
    print("\nEscolha o nível:")
    print("1. Silencioso")
    print("2. Básico (recomendado)")
    print("3. Detalhado")
    print("4. Debug")
    
    try:
        escolha = input("\nDigite o número (1-4) [2]: ").strip() or '2'
        
        if escolha in opcoes:
            config.set_nivel_explicacao(opcoes[escolha])
            interface.print_sucesso(f"Nível configurado para: {opcoes[escolha].value}")
        else:
            interface.print_aviso("Opção inválida, mantendo configuração atual")
    
    except KeyboardInterrupt:
        print("\n")
        interface.print_aviso("Configuração cancelada")
    
    return config

# Instância global
config_ia = ConfigIA()
