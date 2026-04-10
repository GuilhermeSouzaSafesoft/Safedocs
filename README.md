### Safedocs

Ferramenta para gerar documentos DOCX a partir de arquivos JSON usando o template técnico da Safesoft.

#### Instalação

- **Pré-requisitos**: Python 3.10+ e `pip` instalados.
- Instale as dependências:

```bash
pip install -r requirements.txt
```

#### Como rodar

```bash
python -m safedocs.main
```

Ou com parâmetros customizados:

```bash
python -m safedocs.cli \
  --json data/dados_json.json \
  --template templates/template.docx \
  --output output/documento_final.docx \
  --placeholder-image templates/imagem.png
```

#### Formato do JSON (novo schema)

O JSON deve conter dois campos principais:

- `meta`: metadados da capa.
- `blocks`: lista ordenada de blocos do conteúdo.

Exemplo:

```json
{
  "meta": {
    "tipo_do_documento": "Guia rápido",
    "nome_do_item": "Produto Exemplo",
    "codigo": "EX-API-0001",
    "revisao": "A",
    "data": "2026-03-15"
  },
  "blocks": [
    { "type": "secao", "text": "Seção inicial" },
    { "type": "paragrafo", "text": "Texto enviado via API." },
    { "type": "heading", "level": 2, "text": "Subseção via level" },
    { "type": "lista_com_marcadores", "items": ["Item 1", "Item 2"] },
    { "type": "tabela", "columns": ["A", "B"], "rows": [["1", "2"]] }
  ]
}
```

##### `meta`

- `tipo_do_documento` (string)
- `nome_do_item` (string)
- `codigo` (string)
- `revisao` (string)
- `data` (string)

##### `blocks[*]`

Campos aceitos pelo schema:

- `type` (string) **obrigatório**
- `text` (string)
- `level` (integer)
- `items` (array de strings)
- `columns` (array de strings)
- `rows` (array de arrays de strings)

Tipos de bloco suportados pelo renderizador:

- Português: `paragrafo`, `secao`, `subsecao`, `subsubsecao`, `subsubsubsecao`, `lista_com_marcadores`, `lista_numerada`, `tabela`, `imagem`, `quebra_de_pagina`.
- Compatibilidade legada: `paragraph`, `heading` (usa `level`), `bullets`, `numbered`, `table`, `image`, `page_break`, `title`.

#### API FastAPI

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:

- `GET /`
- `GET /health`
- `POST /generate-docx`
- `POST /generate-docx-action`

#### Testes

```bash
pytest
```
