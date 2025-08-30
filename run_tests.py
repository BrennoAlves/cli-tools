#!/usr/bin/env python3
"""Script para executar testes - apenas na branch dev."""

import subprocess
import sys
import os
from pathlib import Path


def get_current_branch():
    """Obtém a branch atual."""
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def run_tests():
    """Executa os testes."""
    print("🧪 Executando testes...")
    
    # Usar venv se disponível
    venv_python = Path('.venv/bin/python')
    if venv_python.exists():
        python_cmd = str(venv_python)
    else:
        python_cmd = sys.executable
    
    # Verificar se pytest está instalado
    try:
        result = subprocess.run([python_cmd, '-c', 'import pytest'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ pytest não encontrado no venv. Instalando...")
            subprocess.run([python_cmd, '-m', 'pip', 'install', 'pytest'], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar pytest")
        return False
    
    # Executar testes
    cmd = [python_cmd, '-m', 'pytest', 'tests/', '-v', '--tb=short']
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("✅ Todos os testes passaram!")
        return True
    else:
        print("❌ Alguns testes falharam!")
        return False


def run_lint():
    """Executa verificação de código."""
    print("🔍 Verificando código...")
    
    # Verificar imports
    try:
        result = subprocess.run([sys.executable, '-c', 'import src.main'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Erro de import: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar imports: {e}")
        return False
    
    print("✅ Verificação de código passou!")
    return True


def main():
    """Função principal."""
    branch = get_current_branch()
    
    if branch != 'dev':
        print(f"⚠️ Testes só executam na branch dev. Branch atual: {branch}")
        return False
    
    print(f"📋 Executando testes na branch: {branch}")
    
    # Executar verificações
    lint_ok = run_lint()
    tests_ok = run_tests()
    
    if lint_ok and tests_ok:
        print("🎉 Todas as verificações passaram! Pronto para merge na main.")
        return True
    else:
        print("💥 Algumas verificações falharam. Corrija antes do merge.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
