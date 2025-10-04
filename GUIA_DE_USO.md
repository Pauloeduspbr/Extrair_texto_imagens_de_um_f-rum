# 📖 GUIA DE USO - Extrator ForexFactory

Este guia explica como usar os **3 scripts disponíveis** para extrair posts e imagens do ForexFactory.

---

## 🎯 Qual Script Usar?

| Script | Quando Usar | Tempo Estimado |
|--------|-------------|----------------|
| **extrair_uma_pagina.py** | Testes rápidos, uma página apenas | ~1-2 min |
| **extrator_range_paginas.py** | Escolher quantidade ou range específico | Variável |
| **extrator_multipaginas.py** | Extrair thread completa | Longo |

---

## 📄 Script 1: `extrair_uma_pagina.py`

### 🎯 Para que serve?
Extrai **apenas a primeira página** de uma thread. Ideal para:
- Testes rápidos
- Verificar se o sistema está funcionando
- Extrair threads pequenas (1 página)

### 📝 Como usar:
```bash
python extrair_uma_pagina.py
```

### 📊 Resultado:
- Arquivo: `posts_uma_pagina.json`
- Pasta: `imagens_extraidas/`
- Tempo: ~1-2 minutos

### ✅ Exemplo de uso:
```
🚀 EXTRATOR FOREXFACTORY - VERSÃO CORRIGIDA
═══════════════════════════════════════════
▶️  Testar versão corrigida? (ENTER ou 'n'): [ENTER]
🔧 Iniciando Chrome...
✅ Chrome iniciado!
🎯 FAÇA LOGIN E NAVEGUE:
⏳ Pressione ENTER quando pronto: [ENTER]
✅ 16 posts extraídos
✅ 9 imagens baixadas
🎉 EXTRAÇÃO CORRIGIDA COMPLETA!
```

---

## 📑 Script 2: `extrator_range_paginas.py` ⭐ **NOVO**

### 🎯 Para que serve?
Extrai um **range customizado** de páginas. Você escolhe:
- **Quantidade específica**: "Quero 15 páginas" ou "Quero 100 páginas"
- **Range de páginas**: "Páginas 1 até 10" ou "Páginas 5 até 25"
- **Todas as páginas**: Extrai thread completa

### 📝 Como usar:
```bash
python extrator_range_paginas.py
```

### 🎮 Interface Interativa:
```
📊 TOTAL DE PÁGINAS DISPONÍVEIS: 243

🎯 OPÇÕES DE EXTRAÇÃO:
1️⃣  Extrair uma quantidade específica (ex: 15, 100)
2️⃣  Extrair um range de páginas (ex: 1-10, 5-25)
3️⃣  Extrair TODAS as páginas (243 páginas)

▶️  Escolha uma opção (1/2/3):
```

### 📋 Exemplos de uso:

#### Exemplo 1: Extrair 15 páginas
```
▶️  Escolha uma opção (1/2/3): 1
📝 Quantas páginas extrair? (1-243): 15
✅ Configurado: Páginas 1 até 15
```

#### Exemplo 2: Extrair páginas 10 até 25
```
▶️  Escolha uma opção (1/2/3): 2
📝 Digite o range (ex: 1-10, 5-25): 10-25
✅ Configurado: Páginas 10 até 25 (16 páginas)
```

#### Exemplo 3: Extrair páginas 1 até 100
```
▶️  Escolha uma opção (1/2/3): 1
📝 Quantas páginas extrair? (1-243): 100
✅ Configurado: Páginas 1 até 100
```

### 📊 Resultado:
```
topico_completo/
├── json_por_pagina/
│   ├── pagina_1.json
│   ├── pagina_2.json
│   └── ...
├── imagens_por_pagina/
│   ├── pagina_1/
│   ├── pagina_2/
│   └── ...
└── resumos/
    ├── resumo_range.json
    └── topico_range.json
```

### ⏱️ Tempo Estimado:
- **10 páginas**: ~5-10 minutos
- **50 páginas**: ~20-30 minutos
- **100 páginas**: ~40-60 minutos

---

## 📚 Script 3: `extrator_multipaginas.py`

### 🎯 Para que serve?
Extrai **TODAS as páginas** de uma thread automaticamente. Ideal para:
- Backup completo de threads
- Análise de threads grandes
- Arquivamento de histórico completo

### 📝 Como usar:
```bash
python extrator_multipaginas.py
```

### ⚠️ Atenção:
- Script detecta automaticamente o total de páginas
- Pergunta confirmação se > 10 páginas
- Pode demorar **muito tempo** para threads grandes

### 📊 Resultado:
Mesma estrutura do `extrator_range_paginas.py`, mas com **todas** as páginas.

### ⏱️ Tempo Estimado:
- **50 páginas**: ~20-30 minutos
- **100 páginas**: ~40-60 minutos
- **200+ páginas**: ~2-4 horas

---

## 🔧 Configuração Inicial

### 1. Editar credenciais nos scripts:
```python
USERNAME = 'seu_usuario'
PASSWORD = 'sua_senha'
```

### 2. Alterar URL da thread (se necessário):
```python
THREAD_URL = 'https://www.forexfactory.com/thread/SEU_TOPICO'
```

---

## 📊 Estrutura de Saída

### JSON por Página:
```json
{
  "pagina": 1,
  "total_paginas": 15,
  "posts_extraidos": 20,
  "posts": [
    {
      "numero_global": 1,
      "numero_na_pagina": 1,
      "autor": "foolsgame",
      "data": "Oct 15, 2016 12:51pm",
      "conteudo": "Texto completo...",
      "conteudo_tamanho": 1234,
      "numero_imagens": 2,
      "numero_imagens_baixadas": 2,
      "imagens_baixadas": [
        {
          "nome_arquivo": "pagina_1_post_1_img_1.jpg",
          "tamanho_bytes": 45678
        }
      ]
    }
  ]
}
```

### Resumo Final:
```json
{
  "range_extraido": {
    "pagina_inicio": 1,
    "pagina_fim": 15,
    "total_paginas_extraidas": 15
  },
  "estatisticas": {
    "total_posts": 320,
    "total_imagens_baixadas": 87,
    "autores_unicos": 42,
    "posts_por_autor": {
      "foolsgame": 125,
      "steve2010": 48,
      "pips29": 32
    }
  }
}
```

---

## 🚀 Fluxo de Uso Recomendado

### Para Iniciantes:
1. **Testar primeiro**: `python extrair_uma_pagina.py`
2. **Ver se funciona**: Verificar `posts_uma_pagina.json` e `imagens_extraidas/`
3. **Extrair mais**: `python extrator_range_paginas.py` → Opção 1 → 5 páginas

### Para Usuários Avançados:
1. **Range customizado**: `python extrator_range_paginas.py` → Opção 2 → "1-50"
2. **Análise parcial**: Processar dados extraídos
3. **Completar extração**: Usar Opção 2 → "51-100" para continuar

### Para Backup Completo:
1. **Thread completa**: `python extrator_multipaginas.py`
2. **Aguardar**: Pode levar horas para threads grandes
3. **Verificar**: Resumo final em `topico_completo/resumos/`

---

## 💡 Dicas e Truques

### ✅ Boas Práticas:
- Sempre faça **login manual** antes de iniciar
- Use `extrator_range_paginas.py` para **controle total**
- Para threads > 100 páginas, extraia em **blocos de 50**
- Verifique o **resumo.json** após cada extração

### ⚠️ Evite:
- Extrair threads enormes de uma vez (risco de timeout)
- Fechar o Chrome durante a extração
- Executar múltiplos scripts simultaneamente

### 🔄 Continuar Extração:
Se interrompeu no meio:
```bash
python extrator_range_paginas.py
# Escolha Opção 2
# Digite: 51-100 (ou onde parou)
```

---

## 🐛 Solução de Problemas

### Problema: "Nenhum post extraído"
**Solução**: Verifique se fez login e está na página correta

### Problema: "Imagens não baixam"
**Solução**: 
1. Confirme que fez login
2. Aguarde o script criar a sessão com cookies
3. Teste com `extrair_uma_pagina.py` primeiro

### Problema: "Chrome fecha sozinho"
**Solução**: Não escolha "Fechar Chrome" quando perguntado

### Problema: "Extração muito lenta"
**Solução**: Use `extrator_range_paginas.py` com ranges menores (20-30 páginas)

---

## 📞 Suporte

- **Issues no GitHub**: Para bugs e problemas técnicos
- **Pull Requests**: Melhorias são bem-vindas!
- **Documentação**: README.md para informações gerais

---

**Última atualização**: Outubro 2025  
**Versão**: 3.0 (com extrator_range_paginas.py)
