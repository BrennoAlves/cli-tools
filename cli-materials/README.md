# 🛠️ CLI Tools - Materiais de Apoio

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
mv cli-materials /novo/local/
cli-tools config --workspace /novo/local/cli-materials
```
