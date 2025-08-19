#!/usr/bin/env python3
"""
🗂️ Configuração de Diretórios - CLI Tools
Sistema de diretórios padrão para materiais de apoio
"""

import os
import json
from pathlib import Path

class ConfigDiretorios:
    def __init__(self):
        self.config_dir = Path.home() / '.local/share/cli-tools'
        self.config_file = self.config_dir / 'diretorios.json'
        self._carregar_config()
    
    def _carregar_config(self):
        """Carregar configuração de diretórios"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.workspace_dir = Path(config.get('workspace_dir', self._dir_padrao()))
                    self.imagens_dir = Path(config.get('imagens_dir', self.workspace_dir / 'imagens'))
                    self.figma_dir = Path(config.get('figma_dir', self.workspace_dir / 'figma'))
                    self.repos_dir = Path(config.get('repos_dir', self.workspace_dir / 'repos'))
            except (json.JSONDecodeError, KeyError):
                self._config_padrao()
        else:
            self._config_padrao()
    
    def _dir_padrao(self):
        """Diretório padrão baseado no diretório atual ou home"""
        # Se estamos em um projeto (tem .git), usar ./materials
        cwd = Path.cwd()
        if (cwd / '.git').exists():
            return cwd / 'materials'
        
        # Senão, usar ~/materials
        return Path.home() / 'materials'
    
    def _config_padrao(self):
        """Configuração padrão de diretórios"""
        self.workspace_dir = self._dir_padrao()
        self.imagens_dir = self.workspace_dir / 'imagens'
        self.figma_dir = self.workspace_dir / 'figma'
        self.repos_dir = self.workspace_dir / 'repos'
        self._salvar_config()
    
    def _salvar_config(self):
        """Salvar configuração de diretórios"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        config = {
            'workspace_dir': str(self.workspace_dir),
            'imagens_dir': str(self.imagens_dir),
            'figma_dir': str(self.figma_dir),
            'repos_dir': str(self.repos_dir)
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def configurar_workspace(self, novo_dir):
        """Configurar novo diretório de workspace"""
        novo_dir = Path(novo_dir).resolve()
        
        # Validar se é um diretório válido
        if not self._validar_diretorio(novo_dir):
            return False
        
        self.workspace_dir = novo_dir
        self.imagens_dir = novo_dir / 'imagens'
        self.figma_dir = novo_dir / 'figma'
        self.repos_dir = novo_dir / 'repos'
        
        self._salvar_config()
        self._criar_estrutura()
        return True
    
    def configurar_diretorio_especifico(self, tipo, novo_dir):
        """Configurar diretório específico (imagens, figma, repos)"""
        novo_dir = Path(novo_dir).resolve()
        
        if not self._validar_diretorio(novo_dir):
            return False
        
        if tipo == 'imagens':
            self.imagens_dir = novo_dir
        elif tipo == 'figma':
            self.figma_dir = novo_dir
        elif tipo == 'repos':
            self.repos_dir = novo_dir
        else:
            return False
        
        self._salvar_config()
        novo_dir.mkdir(parents=True, exist_ok=True)
        return True
    
    def _validar_diretorio(self, caminho):
        """Validar se o diretório é seguro"""
        caminho_str = str(caminho)
        
        # Não permitir diretórios do sistema
        diretorios_proibidos = ['/etc', '/root', '/sys', '/proc', '/dev']
        for proibido in diretorios_proibidos:
            if caminho_str.startswith(proibido):
                return False
        
        return True
    
    def _criar_estrutura(self):
        """Criar estrutura de diretórios"""
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.imagens_dir.mkdir(parents=True, exist_ok=True)
        self.figma_dir.mkdir(parents=True, exist_ok=True)
        self.repos_dir.mkdir(parents=True, exist_ok=True)
        
        # Criar README explicativo
        readme_path = self.workspace_dir / 'README.md'
        if not readme_path.exists():
            readme_content = """# 🛠️ CLI Tools - Materials

Este diretório contém materiais baixados pelas ferramentas CLI:

## 📁 Estrutura

- **imagens/** - Imagens do Pexels via `cli-tools search`
- **figma/** - Designs extraídos do Figma via `cli-tools figma`
- **repos/** - Repositórios baixados via `cli-tools repo`

## ⚙️ Configuração

Para alterar os diretórios:
```bash
cli-tools config --workspace /novo/caminho
cli-tools config --imagens /caminho/imagens
cli-tools config --figma /caminho/figma
cli-tools config --repos /caminho/repos
```

## 🔄 Reorganização

Você pode mover este diretório e reconfigurar:
```bash
mv materials /novo/local/
cli-tools config --workspace /novo/local/materials
```
"""
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
    
    def obter_diretorio(self, tipo, criar=True):
        """Obter diretório específico"""
        if tipo == 'imagens':
            dir_path = self.imagens_dir
        elif tipo == 'figma':
            dir_path = self.figma_dir
        elif tipo == 'repos':
            dir_path = self.repos_dir
        elif tipo == 'workspace':
            dir_path = self.workspace_dir
        else:
            return None
        
        if criar:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        return str(dir_path)
    
    def status(self):
        """Status dos diretórios configurados"""
        return {
            'workspace': str(self.workspace_dir),
            'imagens': str(self.imagens_dir),
            'figma': str(self.figma_dir),
            'repos': str(self.repos_dir),
            'workspace_exists': self.workspace_dir.exists(),
            'imagens_exists': self.imagens_dir.exists(),
            'figma_exists': self.figma_dir.exists(),
            'repos_exists': self.repos_dir.exists()
        }

# Instância global
config_diretorios = ConfigDiretorios()
