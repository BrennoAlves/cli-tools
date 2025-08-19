# 🖥️ CLI Tools - Interface Textual

## 🚀 Como Usar

### Executar Interface Textual
```bash
# Interface completa
cli-tools ui

# Modo demo (sem APIs reais)
cli-tools ui --demo
```

### Executar Diretamente
```bash
# Aplicação principal
python cli_tools/textual_app/main_app.py

# Aplicação avançada
python cli_tools/textual_app/advanced_app.py

# Demo simples
python cli_tools/textual_app/demo_simple.py
```

## 🎮 Navegação

### Teclas Globais
- **q**: Sair da aplicação
- **d**: Alternar tema escuro/claro
- **c**: Abrir configurações
- **s**: Tirar screenshot
- **Ctrl+C**: Sair forçado

### Navegação por Widgets
- **Tab**: Próximo widget
- **Shift+Tab**: Widget anterior
- **Enter**: Ativar botão/confirmar
- **Esc**: Voltar/Fechar modal
- **Setas**: Navegar em listas/tabelas

## 🎯 Funcionalidades

### 📊 Dashboard Tab
- **Métricas em tempo real**: APIs ativas, requests, storage
- **Gráfico de uso**: Sparkline dos últimos 7 dias
- **Tabela detalhada**: Status, performance, quotas

### 🔍 Search Tab
- **Formulário avançado**: Query, quantidade, orientação
- **Filtros**: Tamanho, tipo, cores
- **Progress bar**: Com ETA durante busca
- **Modal de resultados**: Lista interativa

### 📁 Repos Tab
- **DirectoryTree**: Explorador de arquivos
- **TextArea**: Preview de código com syntax highlighting
- **Navegação**: Click para selecionar arquivos

### 📋 Logs Tab
- **RichLog**: Logs coloridos em tempo real
- **Controles**: Limpar, exportar, auto-scroll
- **Formatação**: Markup e highlighting

## 🎨 Widgets Implementados

### Entrada de Dados
- **Input**: Campos de texto com validação
- **Select**: Dropdowns com opções
- **RadioSet**: Botões de rádio
- **Checkbox**: Caixas de seleção
- **Switch**: Interruptores
- **SelectionList**: Seleção múltipla

### Exibição
- **DataTable**: Tabelas interativas
- **Tree**: Navegação hierárquica
- **DirectoryTree**: Explorador de arquivos
- **TextArea**: Editor de código
- **RichLog**: Logs formatados
- **Sparkline**: Gráficos simples
- **ProgressBar**: Barras de progresso

### Layout
- **TabbedContent**: Interface com abas
- **Collapsible**: Seções recolhíveis
- **Container**: Agrupamento
- **Horizontal/Vertical**: Layout flexível

### Interação
- **Button**: Botões com variants
- **Modal**: Janelas modais
- **ListView**: Listas interativas
- **LoadingIndicator**: Indicadores de carregamento

## 🎨 Tema Dracula

### Cores Principais
- **Background**: #282a36 (Dracula dark)
- **Foreground**: #f8f8f2 (Dracula white)
- **Primary**: #bd93f9 (Dracula purple)
- **Success**: #50fa7b (Dracula green)
- **Warning**: #ffb86c (Dracula orange)
- **Error**: #ff5555 (Dracula red)
- **Info**: #8be9fd (Dracula cyan)

### Elementos Estilizados
- **Borders**: #6272a4 (Dracula comment)
- **Focus**: #bd93f9 (Dracula purple)
- **Hover**: Variações das cores principais
- **Cards**: Bordas coloridas por tipo

## 🔧 Integração com CLI Tools

### APIs Reais
- **ConfigAPI**: Leitura de chaves de API
- **ControladorUso**: Métricas de uso
- **ConfigDiretorios**: Workspace paths

### Funcionalidades
- **Status real**: APIs, workspace, arquivos
- **Navegação**: DirectoryTree do materials/
- **Logs**: Sistema de logging integrado
- **Configuração**: Modal para APIs

## 🚀 Próximos Passos

### Funcionalidades Planejadas
- [ ] Integração real com comando search
- [ ] Interface para comando figma
- [ ] Browser de repositórios com IA
- [ ] Chat integrado com Gemini
- [ ] Sistema de notificações
- [ ] Temas personalizáveis
- [ ] Plugins e extensões

### Melhorias Técnicas
- [ ] Testes automatizados
- [ ] Performance optimization
- [ ] Responsividade aprimorada
- [ ] Acessibilidade
- [ ] Documentação completa

## 📸 Screenshots

Para gerar screenshots:
```bash
# Na aplicação, pressione 's'
# Ou via código:
python -c "
from textual_app.advanced_app import AdvancedCLIToolsApp
import asyncio

async def screenshot():
    app = AdvancedCLIToolsApp()
    async with app.run_test() as pilot:
        await pilot.pause(1.0)
        app.save_screenshot('cli_tools_textual.svg')
        print('Screenshot salvo!')

asyncio.run(screenshot())
"
```

## 🎉 Resultado Final

✅ **Interface TUI completa usando Textual framework**  
✅ **15+ widgets diferentes implementados**  
✅ **4 tabs funcionais com funcionalidades reais**  
✅ **Tema Dracula personalizado**  
✅ **Navegação por teclado e mouse**  
✅ **Integração com APIs do CLI Tools**  
✅ **Modals, workers assíncronos, eventos**  
✅ **CSS styling avançado**  

**Agora você tem uma interface TUI moderna e funcional! 🚀**
