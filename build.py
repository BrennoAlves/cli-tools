#!/usr/bin/env python3
"""Script de build para distribuição PyPI."""

import subprocess
import sys
import shutil
from pathlib import Path


def clean_build():
    """Limpa arquivos de build anteriores."""
    print("🧹 Limpando builds anteriores...")
    
    dirs_to_clean = ['build', 'dist', 'src/cli_tools.egg-info']
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  ✅ Removido: {dir_name}")


def run_tests():
    """Executa testes antes do build."""
    print("🧪 Executando testes...")
    
    result = subprocess.run([sys.executable, 'run_tests.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Testes falharam! Build cancelado.")
        print(result.stdout)
        print(result.stderr)
        return False
    
    print("✅ Testes passaram!")
    return True


def build_package():
    """Constrói o pacote."""
    print("📦 Construindo pacote...")
    
    # Build wheel e source distribution
    cmd = [sys.executable, '-m', 'build']
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("✅ Pacote construído com sucesso!")
        
        # Listar arquivos gerados
        dist_dir = Path('dist')
        if dist_dir.exists():
            print("\n📁 Arquivos gerados:")
            for file in dist_dir.iterdir():
                size = file.stat().st_size / 1024  # KB
                print(f"  📄 {file.name} ({size:.1f} KB)")
        
        return True
    else:
        print("❌ Erro no build!")
        return False


def check_package():
    """Verifica o pacote construído."""
    print("🔍 Verificando pacote...")
    
    try:
        # Verificar com twine se disponível
        result = subprocess.run([sys.executable, '-m', 'twine', 'check', 'dist/*'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Pacote válido!")
        else:
            print("⚠️ Avisos no pacote:")
            print(result.stdout)
    except FileNotFoundError:
        print("⚠️ twine não encontrado, pulando verificação")


def main():
    """Função principal."""
    print("🚀 Iniciando build do CLI Tools v2.0")
    
    # Verificar se build está disponível
    try:
        import build
    except ImportError:
        print("📦 Instalando build...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'build'], check=True)
    
    # Executar etapas
    clean_build()
    
    if not run_tests():
        return False
    
    if not build_package():
        return False
    
    check_package()
    
    print("\n🎉 Build concluído com sucesso!")
    print("💡 Para publicar: python -m twine upload dist/*")
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
