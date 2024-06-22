import fnmatch
import os
import pymupdf

def find_invoice(invoices_folder: str, invoice_number: str) -> list[str]:
    filepaths: list[str] = pdf_files(invoices_folder)
    if len(invoice_number) == 0:
        raise Exception("empty invoice number")
    if len(filepaths) == 0:
        return ["no file found"]
    list_of_comments = []
    list_of_paths = []
    for filepath in filepaths:
        list_pdf_files = []
        filepath_result_comment = []
        with pymupdf.open(filepath) as pdf_file:
            file_content = ""

            for page in pdf_file:
                file_content += page.get_text().strip()
            if invoice_number in file_content:
                list_pdf_files.append(filepath)
                filepath_result_comment.append("ok")
            list_of_paths.append(list_pdf_files)
            list_of_comments.append(filepath_result_comment)
    total = []
    for path, comment in zip(list_of_paths, list_of_comments):
        for number, ko in zip(path, comment):
            if 'ok' in ko:
                total.append(number)
    return total

def pdf_page_content(filepath: str) -> str:
    try:
        with pymupdf.open(filepath, 'rb') as pdf_file:
            page_content = ""

            for page in pdf_file:
                page_content += page.get_text().strip()

            return page_content
    except:
        return "malformed pdf file"

def pdf_files(folder: str) -> list[str]:
    list_of_pdf_files = []
    for root, subFolders, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, "*.pdf"):
            path = os.path.join(root + os.sep, filename).replace("\\", "/")
            list_of_pdf_files.append(path)

    return list_of_pdf_files
