# Extrator de Texto e Imagens - ForexFactory# Extrator de Texto e Imagens - ForexFactory# Extrair Texto e Imagens de um Fórum



Sistema automatizado para extrair texto e imagens de threads do fórum ForexFactory, com suporte a autenticação e navegação multi-página.



## 🚀 FuncionalidadesSistema automatizado para extrair texto e imagens de threads do fórum ForexFactory, com suporte a autenticação e navegação multi-página.Este script automatiza a extração de texto e imagens de threads de fóruns, especificamente do ForexFactory.



- **Extração completa de threads**: Navega automaticamente por todas as páginas de uma thread

- **Autenticação automática**: Login no ForexFactory para acessar conteúdo restrito

- **Download de imagens**: Baixa todas as imagens dos posts com autenticação adequada## 🚀 Funcionalidades## Funcionalidades

- **Organização hierárquica**: Organiza dados por página em estrutura de pastas

- **Anti-detecção**: Medidas contra bloqueio por sistemas anti-bot

- **Saída estruturada**: Dados salvos em JSON com metadados completos

- **Seleção flexível**: Extraia páginas específicas, ranges ou thread completa- **Extração completa de threads**: Navega automaticamente por todas as páginas de uma thread- **Instalação automática de dependências**: O script instala automaticamente todos os pacotes necessários



## 📁 Estrutura do Projeto- **Autenticação automática**: Login no ForexFactory para acessar conteúdo restrito- **Configuração automática do ChromeDriver**: Não é necessário baixar ou configurar manualmente o ChromeDriver



```- **Download de imagens**: Baixa todas as imagens dos posts com autenticação adequada- **Extração completa de posts**: Extrai autor, data, texto e imagens de todos os posts

├── extrator_range_paginas.py     # ⭐ Script com range customizável (NOVO)

├── extrator_multipaginas.py      # Script para thread completa- **Organização hierárquica**: Organiza dados por página em estrutura de pastas- **Download automático de imagens**: Salva todas as imagens encontradas nos posts

├── extrair_uma_pagina.py         # Script para página única

├── GUIA_DE_USO.md                # 📖 Guia detalhado de uso- **Anti-detecção**: Medidas contra bloqueio por sistemas anti-bot- **Navegação automática entre páginas**: Percorre automaticamente todas as páginas da thread

├── posts_uma_pagina.json         # Dados extraídos (página única)

├── imagens_extraidas/            # Imagens baixadas (página única)- **Saída estruturada**: Dados salvos em JSON com metadados completos- **Saída em JSON**: Salva todos os dados extraídos em formato JSON estruturado

└── topico_completo/              # Estrutura completa por páginas

    ├── json_por_pagina/          # JSONs organizados por página

    ├── imagens_por_pagina/       # Imagens organizadas por página

    └── resumos/                  # Estatísticas e resumos## 📁 Estrutura do Projeto## Como usar

```



## 🎯 Scripts Disponíveis

```1. **Execute o script diretamente**:

### 1. Extração com Range Customizado ⭐ **RECOMENDADO**

```bash├── extrator_multipaginas.py      # Script principal - extração completa   ```bash

python extrator_range_paginas.py

```├── extrair_uma_pagina.py   # Script para página única   python extarct.py

- Escolha **quantidade de páginas** (ex: 15, 100)

- Escolha **range de páginas** (ex: 1-10, 5-25)├── posts_uma_pagina.json   # Dados extraídos (página única)   ```

- Interface interativa e intuitiva

- Controle total sobre extração├── imagens_extraidas/            # Imagens baixadas (página única)

- 📖 **Ver [GUIA_DE_USO.md](GUIA_DE_USO.md) para detalhes**

└── topico_completo/              # Estrutura completa por páginas2. **O script irá automaticamente**:

### 2. Extração Multi-Página (Thread Completa)

```bash    ├── json_por_pagina/          # JSONs organizados por página   - Instalar os pacotes necessários (selenium, beautifulsoup4, requests, webdriver-manager)

python extrator_multipaginas.py

```    ├── imagens_por_pagina/       # Imagens organizadas por página   - Baixar e configurar o ChromeDriver

- Extrai **toda a thread** automaticamente

- Organiza dados por página    └── resumos/                  # Estatísticas e resumos   - Extrair todos os posts da thread especificada

- Download completo de imagens

- Ideal para backup completo```   - Salvar as imagens na pasta `forum_images/`



### 3. Extração Página Única (Testes)   - Salvar os dados em `forum_posts.json`

```bash

python extrair_uma_pagina.py## 🎯 Scripts Disponíveis

```

- Extrai apenas a primeira página## Configuração

- Ideal para testes rápidos

- Menor uso de recursos### 1. Extração Multi-Página (Recomendado)



## 🎮 Exemplo de Uso (Range Customizado)```bashVocê pode modificar as seguintes variáveis no início do script:



```bashpython extrator_multipaginas.py

$ python extrator_range_paginas.py

```- `THREAD_URL`: URL da thread do fórum a ser extraída

📊 TOTAL DE PÁGINAS DISPONÍVEIS: 243

- Extrai **toda a thread** automaticamente- `OUTPUT_JSON`: Nome do arquivo JSON de saída

🎯 OPÇÕES DE EXTRAÇÃO:

1️⃣  Extrair uma quantidade específica (ex: 15, 100)- Organiza dados por página- `IMAGES_DIR`: Diretório onde as imagens serão salvas

2️⃣  Extrair um range de páginas (ex: 1-10, 5-25)

3️⃣  Extrair TODAS as páginas (243 páginas)- Download completo de imagens



▶️  Escolha uma opção (1/2/3): 1- Estatísticas detalhadas## Dependências (instaladas automaticamente)

📝 Quantas páginas extrair? (1-243): 15

✅ Configurado: Páginas 1 até 15



▶️  Iniciar extração? (ENTER para SIM): ### 2. Extração Página Única- selenium

🎉 Extração completa!

``````bash- beautifulsoup4



## ✅ Thread de Exemplopython extrair_uma_pagina.py- requests



O sistema foi testado e validado com:```- webdriver-manager

- **URL**: https://www.forexfactory.com/thread/592890-a-very-simple-system-trade-with-arrow

- **Resultado**: 100% taxa de sucesso para imagens autenticadas- Extrai apenas a primeira página



## 🔧 Configuração- Ideal para testes rápidos## Estrutura de saída



Os scripts instalam automaticamente as dependências:- Menor uso de recursos

- `selenium` - Automação web

- `beautifulsoup4` - Parse HTMLO arquivo JSON gerado contém um array de posts com a seguinte estrutura:

- `requests` - Download de imagens

- `webdriver-manager` - Gerenciamento ChromeDriver## ✅ Thread de Exemplo```json



### Editar credenciais (em cada script):[

```python

USERNAME = 'seu_usuario'O sistema foi testado e validado com:  {

PASSWORD = 'sua_senha'

THREAD_URL = 'https://www.forexfactory.com/thread/SEU_TOPICO'- **URL**: https://www.forexfactory.com/thread/592890-a-very-simple-system-trade-with-arrow    "author": "Nome do autor",

```

- **Credenciais**:  /     "date": "Data do post",

## 📊 Estrutura de Dados

- **Resultado**: 16 posts extraídos, 9 imagens baixadas (100% sucesso)    "text": "Texto completo do post",

```json

{    "images": ["url1.jpg", "url2.png"]

  "numero_global": 1,

  "numero_na_pagina": 1,## 🔧 Configuração  }

  "autor": "foolsgame",

  "data_post": "Oct 15, 2016 12:51pm",]

  "conteudo": "Texto completo do post...",

  "conteudo_tamanho": 1234,Os scripts instalam automaticamente as dependências:```

  "numero_imagens": 2,

  "numero_imagens_baixadas": 2,- `selenium` - Automação web

  "imagens": [

    {- `beautifulsoup4` - Parse HTML## Requisitos do sistema

      "nome_arquivo": "pagina_1_post_1_img_1.jpg",

      "url_original": "https://...",- `requests` - Download de imagens

      "baixada": true,

      "tamanho_bytes": 45678- `webdriver-manager` - Gerenciamento ChromeDriver- Python 3.6+

    }

  ]- Google Chrome instalado

}

```## 📊 Estrutura de Dados- Conexão com a internet



## 🎛️ Características Técnicas```json

{

- **Anti-detecção**: User-agent rotativo, delays aleatórios  "numero_post": 1,

- **Autenticação**: Compartilhamento de cookies entre Selenium e Requests  "autor": "foolsgame",

- **Robustez**: Tratamento de erros e retry automático  "data_post": "Oct 15, 2016 12:51pm",

- **Flexibilidade**: Extraia 1 página, range customizado ou thread completa  "conteudo": "Texto completo do post...",

- **Performance**: Processamento otimizado por página  "imagens": [

    {

## 📋 Requisitos      "nome_arquivo": "image001.png",

      "url_original": "https://...",

- Python 3.9+      "baixada": true

- Google Chrome instalado    }

- Conexão estável com internet  ]

- Credenciais válidas do ForexFactory}

```

## 🏆 Resultados Comprovados

## 🎛️ Características Técnicas

- ✅ **Taxa de sucesso**: 100% para imagens autenticadas

- ✅ **Cobertura**: Extração completa de texto e metadados- **Anti-detecção**: User-agent rotativo, delays aleatórios

- ✅ **Organização**: Estrutura hierárquica por páginas- **Autenticação**: Compartilhamento de cookies entre Selenium e Requests

- ✅ **Escalabilidade**: Suporte a threads com centenas de páginas- **Robustez**: Tratamento de erros e retry automático

- ✅ **Flexibilidade**: 3 modos de extração diferentes- **Performance**: Processamento paralelo quando possível



## 📖 Documentação Completa## 📋 Requisitos



Para guia detalhado com exemplos de uso, tempo estimado, solução de problemas e melhores práticas:- Python 3.9+

- Google Chrome instalado

👉 **[Leia o GUIA_DE_USO.md](GUIA_DE_USO.md)**- Conexão estável com internet

- Credenciais válidas do ForexFactory

## 🚀 Quick Start

## 🏆 Resultados Comprovados

```bash

# 1. Testar com uma página- ✅ **Taxa de sucesso**: 100% para imagens autenticadas

python extrair_uma_pagina.py- ✅ **Cobertura**: Extração completa de texto e metadados

- ✅ **Organização**: Estrutura hierárquica por páginas

# 2. Extrair range customizado (15 páginas)- ✅ **Escalabilidade**: Suporte a threads com centenas de páginas

python extrator_range_paginas.py

# Escolha: Opção 1 → Digite: 15## 🔄 Logs de Execução



# 3. Extrair thread completaO sistema gera logs detalhados incluindo:

python extrator_multipaginas.py- Progresso da extração por página

```- Status de download de imagens

- Estatísticas de posts processados

## 🛠️ Desenvolvimento- Identificação de autores únicos

- Tempo total de processamento

Este projeto evoluiu através de múltiplas iterações para superar:

- Proteções anti-bot do ForexFactory## 🛠️ Desenvolvimento

- Sistemas de autenticação complexos

- Download de imagens com cookiesEste projeto evoluiu através de múltiplas iterações para superar:

- Organização escalável de dados- Proteções anti-bot do ForexFactory

- Flexibilidade na seleção de páginas- Sistemas de autenticação complexos

- Download de imagens com cookies

## 📞 Suporte- Organização escalável de dados



- **Issues**: Para bugs e problemas técnicos---

- **Pull Requests**: Melhorias são bem-vindas!

- **GUIA_DE_USO.md**: Documentação detalhada**Última atualização**: Outubro 2025  

**Status**: Totalmente funcional e testado
---

**Última atualização**: Outubro 2025  
**Versão**: 3.0 (com extrator_range_paginas.py)  
**Status**: Totalmente funcional e testado