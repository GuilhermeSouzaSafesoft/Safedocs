
def validar_arquivos():
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(
            f"Template não encontrado: '{TEMPLATE_FILE}'"
        )

    if not JSON_FILE.exists():
        raise FileNotFoundError(
            f"JSON não encontrado: '{JSON_FILE}'"
        )


def limpar_paragrafos(doc):
    while doc.paragraphs:
        p = doc.paragraphs[0]._element
        p.getparent().remove(p)

def gerar_capa(doc, meta):
    document_type = meta.get("document_type", "")
    item_name = meta.get("item_name", "")
    document_code = meta.get("document_code", "")
    revision = meta.get("revision", "")
    date = meta.get("date", "")

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run(document_type.upper())
    r.font.name = "Corbel"
    r.font.size = Pt(22)
    r.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run(item_name)
    r.font.name = "Corbel"
    r.font.size = Pt(18)

    for _ in range(8):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run(f"Código: {document_code}")
    r.font.name = "Corbel"
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run(f"Data: {date}")
    r.font.name = "Corbel"
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run(f"Versão: {revision}")
    r.font.name = "Corbel"
    r.font.size = Pt(12)

    doc.add_page_break()


def gerar_documento():
    validar_arquivos()

    doc = Document(str(TEMPLATE_FILE))
    limpar_paragrafos(doc)

    gerar_capa(doc, dados_json["meta"])

    for block in dados_json["blocks"]:
        render_block(doc, block)

    doc.save(str(OUTPUT_FILE))
    print(f"Documento gerado com sucesso: {OUTPUT_FILE}")
    files.download(str(OUTPUT_FILE))
