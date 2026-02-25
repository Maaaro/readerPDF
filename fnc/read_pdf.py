import pymupdf


def read_pdf_content(pdf_path: str) -> str:
    try:
        with pymupdf.open(pdf_path) as pdf_file:
            content = ''
            for page in pdf_file:
                content += page.get_text().strip()
            return content
    except Exception as e:
            print(f"Failed to read PDF: {pdf_path}")
            print(f"Error: {str(e)}")
            return ""