# 🏗️ Arquitetura CLI Tools v2.0

## 📋 Visão Geral

CLI Tools é um kit de ferramentas para desenvolvedores fornecerem contexto para IA, focado em ferramentas de terminal que servem para para humanos quanto para agents de IA usarem. Atualemnte tem:
- Busca e download de imagens - Chamado *image*
- Extração de designs do Figma - Chamado *desgin*
- Download inteligente de repositórios - Chamado *repo*
Todos eles tem que ter opção completas, por exemplo baixar tudo, baixa y, baixar x... etc, para atender diversos casos de uso, mas sempre com simplificidade, tendo um comportamento "padrão" para quem só quer algo rápido. A navegação para humanos tem que ser por interface, selecionado opções a aparecendo as subopções (ter gemini cli como referencia), enquanto tudo tambem tem que ser acessavel por comandos com parametros, exemplo cli-tools repo -o 5 -t (ficticoi esses parametros mas é esse o conceito), para atender usuarios avançados e agents chegarem logo onde querem sem ter que passar por interface humanizadas
- A instalação tem que ser passo a passo, instgalando e configurando tudo, depois dando opções para selecionar temas e para adicionar na hora ou depois as keys das ias, se a pessoa foi adicionado tem que validar na hora se ta valida, se não estiver avisa e continua na tela, mas tem que ter um botão de pular a inserção, aí depois tem como configurar pela opções de configs 

## 🎯 Princípios de Design

### 1. **Dual Mode**
- **Humanos**: Interface menu interativa com navegação por setas, leve e elegante
- **Agents**: Comandos únicos tradicionais para automação

### 2. **Modularidade**
- Core separado da interface
- APIs isoladas em módulos
- Fácil extensão e manutenção

### 3. **UX Moderna**
- Cores vibrantes (tema Dracula)
- Feedback visual imediato
- Navegação intuitiva
- Emojis e ícones

## 🏛️ Estrutura Atual

### **Estrutura do Projeto (v2.0)**
```
cli-tools/                  # 📁 Repositório principal
├── src/                    # 🐍 Código fonte Python
│   ├── __init__.py        # 📦 Inicialização do pacote
│   ├── main.py            # 🚀 Entry point principal
│   ├── menu_app/          # 🎮 Interface TUI interativa
│   │   ├── __pycache__/   # 🗂️ Cache Python
│   │   └── interactive_menu.py
│   ├── core/              # ⚙️ Lógica de negócio e APIs
│   │   ├── __init__.py
│   │   ├── __pycache__/   # 🗂️ Cache Python
│   │   ├── config.py      # ⚙️ Configuração geral
│   │   ├── config_ia.py   # 🤖 Configuração IA/Gemini
│   │   ├── config_diretorios.py # 📁 Gestão de diretórios
│   │   ├── controle_uso.py # 📊 Controle de uso das APIs
│   │   ├── interface.py   # 🖥️ Interface base
│   │   ├── navegacao_cli.py # 🧭 Navegação CLI
│   │   ├── rich_dashboards.py # 📊 Dashboards Rich completos
│   │   └── rich_dashboards_simple.py # 📊 Dashboards simplificados
│   └── tools/             #  Ferramentas específicas
│       ├── __pycache__/   # 🗂️ Cache Python
│       ├── buscar-imagens.py # 🔍 Busca de imagens (Pexels)
│       ├── extrator-figma.py # 🎨 Extração Figma
│       └── baixar-repo.py    # 📦 Download de repositórios
├── materials/             # 📁 Workspace de arquivos
│   ├── README.md         # 📖 Documentação do workspace
│   ├── imagens/          # 🖼️ Imagens baixadas
│   ├── figma/            # 🎨 Designs do Figma
│   └── repos/            # 📦 Repositórios clonados
├── .amazonq/             # 📚 Documentação de desenvolvimento
│   └── docs/
│       ├── arquitetura.md    # 🏗️ Este arquivo
│       └── diario_de_bordo.md # 📋 Histórico de desenvolvimento
├── .env                   # 🔑 Configuração local (gitignored)
├── .gitignore            # 🚫 Arquivos ignorados
├── README.md             # 📖 Documentação pública
├── requirements.txt      # 📦 Dependências Python
└── install.sh            # 🚀 Script de instalação
```

## 🛠️ Ferramentas 

- image -> a ideia dele é buscar imagens por palavra chave, o usuario vai pedir para o agent buscar imagens de escritorio, o agent vai usar essa tool para pegar pela api, para isso ele vai passar as dimensões ideias para o uso e o termo de busca sempre em ingles. O padrão é sempre baixar uma imagem e usar, a menos que o usuario peça varias. Para o uso de humanos tem que ser configuravel todos esses parametros de busca. Salvando em (materials/image/(nome do arquivo tem que ser intutitvo com o que foi pedido e o formato tem que ser .webp))

- repo -> a ideia é puxar a lista de arquivos de um repositorio do github e passar para o gemini flash, junto com o pedido do usuario, por exemplo baixe todos os arquivos de frontend, aí o gemini vai retornar um json com todos os arquivos que devem ser baixados e a tool vai e baixa, salvando dentro de materials/repo/(nome do repositorio)

- figma -> a ideia é usar a api do figma para acessar um projeto e baixar componentes de acordo com a solicitação do usuario, por exemplo ter a opção de baixar tudo, outra de baixar só o css, outra de baixar só os componentes, etc. Depois vai ser salvo em materials/repo/(nome do figma)

## 🔌 Integrações de API


### **Pexels API**
- Busca de imagens
- Download automático
- Organização por categorias
- Controle de quota

### **Figma API**
- Extração de designs
- Múltiplos formatos (PNG, SVG, JPG)
- Organização automática
- Metadados preservados

### **Google Gemini**
- Análise inteligente de repositórios
- Seleção de arquivos relevantes
- Processamento de linguagem natural
- Otimização de downloads

## 📁 Workspace Inteligente

### **Estrutura Automática**
```
materials/
├── imagens/
│   ├── categoria1/
│   ├── categoria2/
├── figma/
│   ├── projeto1/
│   ├── projeto2/
└── repos/
    ├── repo1/
    ├── repo2/
```

### **Organização**
- Criação automática de diretórios
- Nomenclatura consistente
- Limpeza automática de arquivos antigos

## 🎨 Sistema de Temas

### **Dracula Theme**
- Cores consistentes em toda aplicação
- Alto contraste para legibilidade
- Suporte a diferentes terminais
- Fallbacks para terminais limitados

### **Componentes Visuais**
- Progress bars animadas
- Status indicators coloridos
- Emojis contextuais

## 🔧 Sistema de Configuração

### **Hierarquia**
1. Variáveis de ambiente
2. Arquivo .env na raiz do projeto
3. Configuração global (~/.cli-tools/)
4. Padrões do sistema

### **APIs Suportadas**
- Chaves criptografadas
- Validação automática
- Teste de conectividade
- Rotação de chaves

## 📊 Monitoramento e Métricas

### **Controle de Uso**
- Tracking de requests por API
- Limites e quotas
- Alertas de proximidade do limite
- Histórico de uso

### **Performance**
- Tempo de resposta das APIs
- Cache hit/miss ratios
- Tamanho de downloads
- Estatísticas de uso

## 🚀 Extensibilidade

### **Plugin System**
- Interface padronizada
- Carregamento dinâmico
- Configuração por plugin
- Isolamento de dependências

### **Custom Commands**
- Registro automático
- Help integrado
- Validação de parâmetros
- Error handling consistente

## 🔒 Segurança

### **API Keys**
- Armazenamento seguro
- Nunca em logs
- Validação contínua

### **Downloads**
- Verificação de integridade
- Limites de tamanho
