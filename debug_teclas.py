#!/usr/bin/env python3
"""
Debug das teclas para identificar o problema
"""

import sys
sys.path.append('cli_tools')

def debug_teclas():
    from cli_tools.lib.menu_navegavel import MenuNavegavel, OpcaoMenu
    
    print("🔍 Debug das Teclas")
    print("=" * 20)
    print("Pressione teclas para ver os códigos:")
    print("• Setas ↑↓ devem mostrar \\x1b[A e \\x1b[B")
    print("• Enter deve mostrar \\r ou \\n")
    print("• Esc deve mostrar \\x1b")
    print("• Ctrl+C para sair")
    print()
    
    # Criar menu simples
    menu = MenuNavegavel("Debug", "Teste de teclas")
    menu.adicionar_opcao(OpcaoMenu("1", "Opção 1", "", "1️⃣"))
    menu.adicionar_opcao(OpcaoMenu("2", "Opção 2", "", "2️⃣"))
    
    # Versão com debug
    import termios
    import tty
    
    while True:
        try:
            print("Pressione uma tecla (Ctrl+C para sair):")
            
            # Ler tecla com debug
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                
                if ch == '\x1b':
                    try:
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[':
                            ch3 = sys.stdin.read(1)
                            tecla_completa = ch + ch2 + ch3
                            print(f"🎯 Sequência de escape: {repr(tecla_completa)}")
                        else:
                            tecla_completa = ch + ch2
                            print(f"🎯 Escape + outro: {repr(tecla_completa)}")
                    except:
                        tecla_completa = ch
                        print(f"🎯 Esc puro: {repr(tecla_completa)}")
                else:
                    tecla_completa = ch
                    print(f"🎯 Tecla normal: {repr(tecla_completa)}")
                
                # Testar lógica
                if tecla_completa == '\x1b[A':
                    print("✅ SETA CIMA detectada corretamente")
                elif tecla_completa == '\x1b[B':
                    print("✅ SETA BAIXO detectada corretamente")
                elif tecla_completa == '\x1b':
                    print("✅ ESC PURO detectado corretamente")
                elif tecla_completa in ['\r', '\n']:
                    print("✅ ENTER detectado corretamente")
                elif tecla_completa == '\x03':
                    print("✅ CTRL+C detectado - saindo...")
                    break
                else:
                    print(f"❓ Tecla não mapeada: {repr(tecla_completa)}")
                
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
        except KeyboardInterrupt:
            print("\n❌ Ctrl+C detectado - saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            break

if __name__ == "__main__":
    debug_teclas()
