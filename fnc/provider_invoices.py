import os

import pymupdf


def find_invoices(sourcePath: str, invoiceNumber: str) -> list[str]:
    if is_dir_empty(sourcePath):
        raise Exception('Provider invoice directory is empty.')
    if not is_there_any_pdf_files(sourcePath):
        raise Exception('Provider invoice directory does not contain invoices.')
    found_invoices = []
    for file in directory_files(sourcePath):
        content = read_pdf_content(os.path.join(sourcePath, file))
        if invoiceNumber in content:
            found_invoices.append(file)
    return found_invoices


def is_there_any_pdf_files(path: str) -> bool:
    for root, subFolders, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".pdf"):
                return True
    return False


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
            files.append(directory_file(path, root, file))
    return files


def directory_file(path: str, root: str, file: str) -> str:
    if has_subfolder(path, root):
        return subfolder(path, root) + "/" + file
    return file


def subfolder(path: str, root: str) -> str:
    return root.removeprefix(path).replace("\\", "")


def has_subfolder(path: str, root: str) -> bool:
    return path != root


def is_dir_empty(path: str) -> bool:
    return len(os.listdir(path)) == 0
