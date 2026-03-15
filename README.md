### Safedocs

Ferramenta para gerar documentos DOCX a partir de arquivos JSON usando o template técnico da Safesoft.

#### Instalação

- **Pré-requisitos**: Python 3.10+ e `pip` instalados.
- Instale as dependências:

```bash
pip install -r requirements.txt
```

#### Estrutura principal

 - `safedocs/` – código da aplicação
   - `main.py` – ponto de entrada simples (usa caminhos padrão do `config.py`).
   - `cli.py` – interface de linha de comando configurável.
   - `config.py` – caminhos padrão para JSON, template, saída e imagem placeholder.
   - `generator.py` – orquestra a geração do documento.
   - `cover.py` – geração da capa a partir de `meta`.
   - `blocks.py` – renderização de blocos (`paragrafo`, `secao`, `tabela`, `imagem`, etc.).
   - `styles.py` – definição de estilos de parágrafo e de texto.
   - `models.py` – modelos tipados (`Meta`, `Block`, `DocumentData`) e validação do JSON.
   - `utils.py` – utilitários (cores, tabelas).
- `data/` – arquivos JSON de entrada (ex.: `dados_json.json`).
- `templates/` – `template.docx` e `imagem.png` (placeholder da capa/imagens).
- `output/` – documentos gerados.
- `examples/` – exemplos de JSON (ex.: `simple_paragraph.json`).
- `tests/` – testes automatizados.

#### Como rodar

Usando os caminhos padrão definidos em `config.py`:

```bash
python -m safedocs.main
```

Ou usando a CLI com parâmetros customizados:

```bash
python -m safedocs.cli \
  --json data/dados_json.json \
  --template templates/template.docx \
  --output output/documento_final.docx \
  --placeholder-image templates/imagem.png
```

#### Formato do JSON

O JSON deve conter dois campos principais:

- `meta`: metadados usados na capa.
- `blocks`: lista ordenada de blocos de conteúdo.

Exemplo mínimo:

```json
{
  "meta": {
    "tipo_do_documento": "Exemplo simples",
    "nome_do_item": "Documento mínimo",
    "codigo": "EX-0001",
    "revisao": "A",
    "data": "2026-03-15"
  },
  "blocks": [
    { "type": "paragrafo", "style": "body", "text": "Parágrafo de exemplo." }
  ]
}
```

##### Campo `meta`

- `tipo_do_documento` (str) – tipo de documento (ex.: "Manual de Instrução"). Esse valor vira o título centralizado da capa.
- `nome_do_item` (str) – nome do item / produto.
- `codigo` (str) – código do documento.
- `revisao` (str) – revisão/versão.
- `data` (str) – data em formato livre (ex.: `2026-03-13`).
- A capa usa sempre o placeholder configurado (via `--placeholder-image` ou o default `templates/imagem.png`) em vez de um campo `cover_image_path`.

##### Tipos de blocos suportados (`blocks[*].type`)

- `paragrafo`
  - Campos:
    - `style` (opcional, str) – estilo de parágrafo (padrão `body`).
    - `run_style` (opcional, str) – estilo padrão do texto se não houver `runs`.
    - `text` (opcional, str) – texto simples.
    - `runs` (opcional, lista) – lista de segmentos com estilos específicos:
      - Cada item: `{ "text": "...", "style": "bold" | "blue" | "italic" | "blue_italic" | ... }`.

- `secao`
  - Campos:
    - `text` (str) – texto da seção (usa o estilo `secao`).

- `subsecao`
  - Campos:
    - `text` (str) – texto da subseção (usa o estilo `subsecao`).

- `subsubsecao`
  - Campos:
    - `text` (str) – texto da subsubseção (usa o estilo `subsubsecao`).

- `subsubsubsecao`
  - Campos:
    - `text` (str) – texto da subsubsubseção (usa o estilo `subsubsubsecao`).

- `lista_com_marcadores`
  - Campos:
    - `items` (lista de strings) – itens da lista com marcador.

- `lista_numerada`
  - Campos:
    - `items` (lista de strings) – itens da lista numerada.

- `tabela`
  - Campos:
    - `columns` (lista de strings) – cabeçalhos.
    - `rows` (lista de listas) – cada sublista é uma linha da tabela.

- `imagem`
  - Campos:
    - `path` (str) – caminho da imagem.
    - `width_cm` (opcional, número) – largura em cm (padrão: 8).
    - `caption` (opcional, str) – legenda abaixo da imagem.
  - Se a imagem não existir, o placeholder configurado é usado automaticamente (sem exibir `[Imagem não encontrada]` quando o placeholder estiver disponível).

- `quebra_de_pagina`
  - Insere uma quebra de página.

#### Testes

Para rodar os testes (requer `pytest` instalado):

```bash
pytest
```

