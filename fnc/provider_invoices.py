import os
import time

import pymupdf

def find_invoices(sourcePath: str, invoiceNumber: str) -> tuple[list[str], list[str]]:
    start = time.time()
    if is_dir_empty(sourcePath):
        raise Exception('Provider invoice directory is empty.')
    if not is_there_any_pdf_files(sourcePath):
        raise Exception('Provider invoice directory does not contain invoices.')
    found_invoices = []
    comments = []
    for file in directory_files(sourcePath):
        content = read_pdf_content(os.path.join(sourcePath, file))
        if invoiceNumber in content:
            found_invoices.append(file)
            comments.append(invoiceNumber)
    end = time.time()
    result = round(end - start,2)
    if not comments:
        status = "Invoice wasn't found"
    else:
        status = "Invoice was found"
    print ("Looking for invoice number: ", invoiceNumber, " for ", result, " sec. ", status)
    return found_invoices, comments


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
            # if file.endswith(".pdf"):
            #     root = root.replace("\\","/")
            #     files.append(directory_file(path, root, file))
            if file.endswith(".pdf"):
                rel_path = os.path.relpath(os.path.join(root, file), path)
                rel_path = rel_path.replace("\\", "/")
                files.append(rel_path)
    return files


def directory_file(path: str, root: str, file: str) -> str:
    if has_subfolder(path, root):
        return subfolder(path, root) + "/" + file
    return file


def subfolder(path: str, root: str) -> str:
    path = path.rstrip("\\/")
    return root.removeprefix(path).lstrip("\\/").replace("\\", "/")


def has_subfolder(path: str, root: str) -> bool:
    return path != root


def is_dir_empty(path: str) -> bool:
    return len(os.listdir(path)) == 0
