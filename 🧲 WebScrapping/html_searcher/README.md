# Buscador de Texto em Páginas Web

Script Python que permite buscar texto específico na estrutura HTML de qualquer página web.

## Funcionalidades

- 🔍 **Busca precisa**: Localiza texto em qualquer parte da estrutura HTML
- 📍 **Localização detalhada**: Mostra linha exata e tipo de elemento HTML
- 🎯 **Contexto visual**: Exibe o contexto ao redor do texto encontrado
- 📊 **Estatísticas**: Conta ocorrências no HTML e no texto visível
- 💾 **Exportação**: Salva resultados em arquivo de texto
- 🎨 **Interface colorida**: Output formatado e fácil de ler
- ⚙️ **Opções flexíveis**: Busca case-sensitive ou case-insensitive
- ⚠️ **Detecção de páginas dinâmicas**: Avisa quando a página usa JavaScript (YouTube, etc.)
- 📏 **Tamanho do arquivo**: Mostra o tamanho estimado antes de salvar resultados

## Instalação

1. Clone/baixe os arquivos
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

Execute o script:
```bash
python text_searcher.py
```

O script solicitará:
1. **URL da página** a ser analisada
2. **Texto a ser buscado**
3. **Tipo de busca** (case-sensitive ou não)

## Exemplo de Uso

```
====================================================
    BUSCADOR DE TEXTO EM PÁGINAS WEB
====================================================

Digite a URL da página: https://example.com
Digite o texto a ser buscado: Python

Opções de busca:
1. Case sensitive (diferencia maiúsculas/minúsculas)
2. Case insensitive (não diferencia maiúsculas/minúsculas)
Escolha uma opção (1 ou 2, padrão=2): 2

🌐 Acessando a página...
✅ Página carregada com sucesso!

🔍 Analisando estrutura HTML...

===============================================================================
                     RESULTADOS DA BUSCA
===============================================================================
URL analisada: https://example.com
Texto buscado: 'Python'
Ocorrências na estrutura HTML: 3
Ocorrências no texto visível: 5

📍 DETALHES DAS OCORRÊNCIAS:
-------------------------------------------------------------------------------

[1] Linha 45 - Cabeçalho
Código HTML:
   <h2>Curso de >>>Python<<< para Iniciantes</h2>
Contexto(s):
   1. <h2>Curso de >>>Python<<< para Iniciantes</h2>

[2] Linha 78 - Parágrafo
Código HTML:
   <p>Aprenda >>>Python<<< de forma prática</p>
Contexto(s):
   1. <p>Aprenda >>>Python<<< de forma prática</p>

[3] Linha 102 - Link
Código HTML:
   <a href="/tutorial">Tutorial de >>>Python<<<</a>
Contexto(s):
   1. <a href="/tutorial">Tutorial de >>>Python<<<</a>

📊 RESUMO POR TIPO DE ELEMENTO:
----------------------------------------
Cabeçalho: 1 ocorrência(s)
Parágrafo: 1 ocorrência(s)
Link: 1 ocorrência(s)

💾 Deseja salvar os resultados em um arquivo?
   Tamanho estimado do arquivo: 2.3 KB
   (s/n): s
✅ Resultados salvos em: busca_resultado_20250711_143022.txt
```

⚠️ **Exemplo de aviso para página dinâmica:**
```
🌐 Acessando a página...
⚠️  AVISO: Esta página (youtube.com) é conhecida por ser dinâmica.
   O conteúdo pode ser carregado via JavaScript após o carregamento inicial.
   Os resultados podem não refletir todo o conteúdo visível ao usuário.
✅ Página carregada com sucesso!
```

## Avisos Importantes

### Páginas Dinâmicas
O script detecta automaticamente páginas que usam JavaScript pesado (como YouTube, Instagram, Facebook) e exibe avisos apropriados. Para essas páginas, o conteúdo mostrado pode não refletir tudo que é visível ao usuário, pois o JavaScript não é executado.

**Sites com detecção automática:**
- YouTube, Instagram, Facebook, Twitter/X
- LinkedIn, TikTok, Netflix, Spotify, Discord
- E outros sites que usam frameworks como React, Vue.js, Angular

**Para páginas dinâmicas, considere:**
- Usar ferramentas como Selenium para execução de JavaScript
- APIs específicas dos serviços (YouTube API, etc.)
- Ferramentas especializadas em scraping de SPAs

### Tamanho dos Arquivos
Antes de salvar os resultados, o script calcula e exibe o tamanho estimado do arquivo, permitindo que você decida se quer prosseguir com o download baseado no espaço disponível.

## Tipos de Elementos Identificados

O script identifica automaticamente os seguintes tipos de elementos HTML:

- **Cabeçalho** (h1, h2, h3, h4, h5, h6)
- **Parágrafo** (p)
- **Link** (a)
- **Div** (div)
- **Span** (span)
- **Título da Página** (title)
- **Meta Tag** (meta)
- **Imagem** (img)
- **Script** (script)
- **CSS/Style** (style)
- **Outro HTML** (outros elementos)
- **Texto/Conteúdo** (texto sem tags)

## Características Técnicas

- **Headers personalizados**: Simula navegador real para evitar bloqueios
- **Timeout configurável**: Evita travamentos em páginas lentas
- **Encoding UTF-8**: Suporte completo a caracteres especiais
- **Tratamento de erros**: Mensagens claras para diferentes tipos de erro
- **Validação de URL**: Verifica formato antes de fazer requisição

## Dependências

- `requests`: Para requisições HTTP
- `beautifulsoup4`: Para parsing de HTML
- `lxml`: Parser XML/HTML rápido
- `colorama`: Para output colorido no terminal

## Limitações

- Funciona apenas com páginas HTML acessíveis via HTTP/HTTPS
- Não executa JavaScript (para sites dinâmicos, considere usar Selenium)
- Respeita robots.txt implicitamente através de headers apropriados
- Algumas páginas podem bloquear bots mesmo com headers de navegador

## Casos de Uso

- 🕵️ **Auditoria de conteúdo**: Verificar se texto específico aparece em páginas
- 📊 **Análise de SEO**: Buscar palavras-chave em elementos específicos
- 🔍 **Debug de HTML**: Localizar onde texto aparece na estrutura
- 📝 **Pesquisa de conteúdo**: Encontrar informações específicas em páginas
- 🎯 **Verificação de meta tags**: Buscar textos em elementos meta

## Contribuições

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades!
