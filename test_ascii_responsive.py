#!/usr/bin/env python3
"""
Teste visual do ASCII art responsivo
"""

import sys
import os
sys.path.append('cli_tools')

from cli_tools.chat.ascii_art import get_responsive_ascii, get_header_with_subtitle

def test_responsive_ascii():
    """Testar ASCII art em diferentes tamanhos"""
    
    print("🎨 Teste de ASCII Art Responsivo - CLI Tools\n")
    
    # Testar diferentes larguras
    test_widths = [120, 80, 60, 40, 30, 20, 15]
    
    for width in test_widths:
        print(f"{'='*50}")
        print(f"📏 Largura: {width} colunas")
        print(f"{'='*50}")
        
        # ASCII art simples
        ascii_art = get_responsive_ascii(width)
        print("ASCII Art:")
        print(ascii_art)
        print()
        
        # Header completo com subtítulo
        header = get_header_with_subtitle(width, "2.0")
        print("Header Completo:")
        print(header)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_responsive_ascii()
