import os

import pymupdf

def find_invoices(sourcePath: str, invoiceNumber: str) -> list[str]:
    if is_dir_empty(sourcePath):
        raise Exception('Provider invoice directory is empty.')
    found_invoices = []
    for file in directory_files(sourcePath):
        content = read_pdf_content(os.path.join(sourcePath, file))
        if invoiceNumber in content:
            found_invoices.append(file)
    return found_invoices

def read_pdf_content(pdf_path: str) -> str:
    with pymupdf.open(pdf_path) as pdf_file:
        content = ''
        for page in pdf_file:
            content += page.get_text().strip()
        return content

def directory_files(path: str) -> list[str]:
    files = []
    for root, subFolders, filenames in os.walk(path):
        for file in filenames:
            files.append(file)
    return files

def is_dir_empty(path: str) -> bool:
    return len(os.listdir(path)) == 0
