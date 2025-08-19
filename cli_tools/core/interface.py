#!/usr/bin/env python3
"""
Interface limpa para cli-tools
"""
import os
import sys
from typing import List, Optional

class InterfaceLimpa:
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.cores = {
            'verde': '\033[92m',
            'amarelo': '\033[93m',
            'vermelho': '\033[91m',
            'azul': '\033[94m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        if not self.quiet:
            os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_colorido(self, texto: str, cor: str = 'reset'):
        """Imprime texto colorido"""
        if not self.quiet:
            cor_code = self.cores.get(cor, self.cores['reset'])
            print(f"{cor_code}{texto}{self.cores['reset']}")
    
    def print_titulo(self, titulo: str):
        """Imprime um título destacado"""
        if not self.quiet:
            print(f"\n{self.cores['bold']}{self.cores['azul']}{titulo}{self.cores['reset']}\n")
    
    def print_sucesso(self, mensagem: str):
        """Imprime mensagem de sucesso"""
        if not self.quiet:
            print(f"{self.cores['verde']}✅ {mensagem}{self.cores['reset']}")
    
    def print_aviso(self, mensagem: str):
        """Imprime mensagem de aviso"""
        if not self.quiet:
            print(f"{self.cores['amarelo']}⚠️  {mensagem}{self.cores['reset']}")
    
    def print_erro(self, mensagem: str):
        """Imprime mensagem de erro"""
        print(f"{self.cores['vermelho']}❌ {mensagem}{self.cores['reset']}")
    
    def mostrar_status(self, mensagem: str):
        """Mostra status de operação"""
        if not self.quiet:
            print(f"{self.cores['azul']}🔄 {mensagem}{self.cores['reset']}")
    
    def mostrar_cabecalho(self, titulo: str, subtitulo: str = ""):
        """Mostra cabeçalho formatado"""
        if not self.quiet:
            print(f"\n{self.cores['bold']}{self.cores['azul']}{titulo}{self.cores['reset']}")
            if subtitulo:
                print(f"{self.cores['azul']}{subtitulo}{self.cores['reset']}")
            print("=" * 50)
            print()
    
    def mostrar_erro(self, mensagem: str):
        """Mostra erro formatado"""
        print(f"{self.cores['vermelho']}❌ {mensagem}{self.cores['reset']}")
    
    def mostrar_sucesso(self, mensagem: str):
        """Mostra sucesso formatado"""
        if not self.quiet:
            print(f"{self.cores['verde']}✅ {mensagem}{self.cores['reset']}")
    
    def mostrar_resultados(self, titulo: str, dados: list):
        """Mostra resultados em tabela"""
        if not self.quiet:
            print(f"\n{self.cores['bold']}{titulo}{self.cores['reset']}")
            print("-" * 40)
            for i, item in enumerate(dados, 1):
                print(f"{i:2d}. {item}")
            print()
    
    def mostrar_status_config(self, configs: dict):
        """Mostra status das configurações"""
        if not self.quiet:
            print(f"{self.cores['bold']}📊 Status das APIs:{self.cores['reset']}")
            for api, info in configs.items():
                status = "✅" if info['ok'] else "❌"
                cor = self.cores['verde'] if info['ok'] else self.cores['vermelho']
                print(f"{cor}{status} {api.title()}: {info['info']}{self.cores['reset']}")
            print()
    
    def mostrar_ajuda(self, comandos: list):
        """Mostra ajuda dos comandos"""
        if not self.quiet:
            print(f"{self.cores['bold']}📚 Comandos Disponíveis:{self.cores['reset']}")
            for cmd in comandos:
                print(f"{self.cores['azul']}• {cmd['uso']}{self.cores['reset']}: {cmd['descricao']}")
            print()
    
    def mostrar_progresso(self, atual: int, total: int, item: str = ""):
        """Mostra progresso de operação"""
        if not self.quiet:
            porcentagem = (atual / total) * 100
            print(f"{self.cores['azul']}📥 [{atual}/{total}] ({porcentagem:.1f}%) {item}{self.cores['reset']}")
    
    def mostrar_erro(self, mensagem: str):
        """Alias para print_erro"""
        self.print_erro(mensagem)
    
    def mostrar_sucesso(self, mensagem: str):
        """Alias para print_sucesso"""
        self.print_sucesso(mensagem)
    
    def mostrar_aviso(self, mensagem: str):
        """Alias para print_aviso"""
        self.print_aviso(mensagem)
    
    def confirmar(self, pergunta: str, padrao: bool = True) -> bool:
        """Pede confirmação do usuário"""
        if self.quiet:
            return padrao
            
        opcoes = "[S/n]" if padrao else "[s/N]"
        resposta = input(f"{pergunta} {opcoes}: ").strip().lower()
        
        if not resposta:
            return padrao
        
        return resposta in ['s', 'sim', 'y', 'yes']
    
    def mostrar_cabecalho(self, titulo: str, versao: str = ""):
        """Mostra cabeçalho do aplicativo"""
        if not self.quiet:
            print(f"\n{self.cores['bold']}{self.cores['azul']}🛠️  {titulo}{self.cores['reset']}")
            if versao:
                print(f"{self.cores['azul']}{versao}{self.cores['reset']}")
            print("=" * 50)
    
    def mostrar_status_config(self, configs: dict):
        """Mostra status das configurações"""
        if not self.quiet:
            print(f"\n{self.cores['bold']}📊 Status das APIs:{self.cores['reset']}")
            
            for nome, status in configs.items():
                if status:
                    print(f"{self.cores['verde']}✅ {nome.title()}: Configurado{self.cores['reset']}")
                else:
                    print(f"{self.cores['vermelho']}❌ {nome.title()}: Não configurado{self.cores['reset']}")
    
    def mostrar_ajuda(self, comandos):
        """Mostra ajuda dos comandos"""
        if not self.quiet:
            print(f"\n{self.cores['bold']}📚 Comandos Disponíveis:{self.cores['reset']}")
            
            if isinstance(comandos, list):
                # Lista de dicionários
                for cmd in comandos:
                    nome = cmd.get('comando', cmd.get('nome', 'N/A'))
                    desc = cmd.get('descricao', cmd.get('desc', 'Sem descrição'))
                    uso = cmd.get('uso', nome)
                    print(f"{self.cores['azul']}• {uso}{self.cores['reset']}: {desc}")
            elif isinstance(comandos, dict):
                # Dicionário simples
                for comando, descricao in comandos.items():
                    print(f"{self.cores['azul']}• {comando}{self.cores['reset']}: {descricao}")
