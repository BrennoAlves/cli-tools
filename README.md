# CLI Tools

Kit de ferramentas para desenvolvedores com interface de linha de comando e UI interativa.

## Instalação

```bash
git clone <repo-url>
cd cli-tools
./install.sh
```

## Uso

### Interface Interativa
```bash
cli-tools ui
```

### Comandos Diretos
```bash
# Buscar imagens
cli-tools search "office desk" -c 5

# Baixar do Figma
cli-tools figma AbCdEfGh123 -f png

# Clonar repositório
cli-tools repo user/repo -q "components"

# Status do sistema
cli-tools status
```

## Atualização

```bash
./update.sh
```

## Estrutura

- **Dados:** `~/.local/share/cli-tools/`
- **Materials:** `~/.local/share/cli-tools/materials/`
- **Config:** `~/.local/share/cli-tools/data/config.json`

## Requisitos

- Python 3.10+
- Linux/macOS
