import pymupdf


def read_pdf_content(pdf_path: str) -> str:
    with pymupdf.open(pdf_path) as pdf_file:
        content = ''
        for page in pdf_file:
            content += page.get_text().strip()
        return content
