"""
Menu simples sem Textual - alternativa para evitar problemas de terminal
"""

import os
import sys
from pathlib import Path

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    """Imprime o cabeçalho do CLI Tools"""
    print("\n" + "="*60)
    print("🛠️  CLI TOOLS v2.0 - Kit de Ferramentas para Desenvolvedores")
    print("="*60)

def print_menu_options(options, selected_index):
    """Imprime as opções do menu com destaque na selecionada"""
    print("\nComandos disponíveis:")
    print("-" * 30)
    
    for i, (cmd, desc) in enumerate(options):
        if i == selected_index:
            print(f"→ [{i+1}] {cmd:<12} - {desc}")
        else:
            print(f"  [{i+1}] {cmd:<12} - {desc}")

def get_user_choice(max_options):
    """Obtém a escolha do usuário"""
    while True:
        try:
            print(f"\nEscolha uma opção (1-{max_options}) ou 'q' para sair: ", end="")
            choice = input().strip().lower()
            
            if choice == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= max_options:
                return choice_num - 1
            else:
                print(f"❌ Opção inválida. Digite um número entre 1 e {max_options}.")
        
        except ValueError:
            print("❌ Digite um número válido ou 'q' para sair.")
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            return None

def show_simple_menu():
    """Mostra um menu simples sem Textual"""
    
    options = [
        ("buscar", "Buscar e baixar imagens do Pexels"),
        ("figma", "Extrair designs e assets do Figma"),
        ("repo", "Baixar repositórios GitHub com IA"),
        ("status", "Ver status das APIs e sistema"),
        ("config", "Configurar chaves de API"),
        ("costs", "Monitorar uso e custos das APIs"),
        ("setup", "Configuração inicial do sistema"),
        ("help", "Mostrar ajuda e exemplos"),
    ]
    
    while True:
        clear_screen()
        print_header()
        print_menu_options(options, -1)  # -1 = nenhuma selecionada
        
        choice = get_user_choice(len(options))
        
        if choice is None:
            print("\n👋 Até logo!")
            break
        
        command = options[choice][0]
        
        # Mapear comandos em português para inglês se necessário
        command_map = {
            "buscar": "search",
            "figma": "figma", 
            "repo": "repo",
            "status": "status",
            "config": "config",
            "costs": "costs",
            "setup": "setup",
            "help": "help"
        }
        
        return command_map.get(command, command)
    
    return None

def run_simple_cli_interface():
    """Interface simples alternativa"""
    return show_simple_menu()
