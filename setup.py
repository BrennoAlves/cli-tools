"""
🛠️ Setup para Ferramentas CLI
Configuração para instalação como comando nativo
"""

from setuptools import setup, find_packages
from pathlib import Path

# Ler README para descrição longa
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="cli-tools-br",
    version="1.0.0",
    description="🛠️ Kit de ferramentas para desenvolvedores com IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Desenvolvedor Brasileiro",
    author_email="dev@exemplo.com",
    url="https://github.com/BrennoAlves/cli-tools",
    
    # Pacotes Python
    packages=find_packages(),
    include_package_data=True,
    
    # Dependências
    install_requires=[
        "click>=8.0.0",
        "requests>=2.25.0",
        "rich>=10.0.0",
    ],
    
    # Comandos CLI nativos
    entry_points={
        "console_scripts": [
            "cli-tools=cli_tools.main:cli",
        ],
    },
    
    # Metadados
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Tools",
        "Topic :: Utilities",
    ],
    
    python_requires=">=3.8",
    
    # Arquivos extras
    package_data={
        "cli_tools": ["*.md", "*.txt"],
    },
)
