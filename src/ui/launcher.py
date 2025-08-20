"""
🚀 UI Launcher - Ponto de entrada para interface moderna
"""

import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
sys.path.append(str(Path(__file__).parent.parent))

from ui.app import run_cli_app

def main():
    """Ponto de entrada principal"""
    try:
        run_cli_app()
    except KeyboardInterrupt:
        print("\n👋 Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
