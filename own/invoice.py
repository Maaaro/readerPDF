import fnmatch
import os
from typing import List, Any

import PyPDF2


def find_invoice(invoices_folder: str, invoice_number: str) -> list[str]:
    filepaths: list[str] = pdf_files(invoices_folder)
    if len(invoice_number) == 0:
        raise Exception("empty invoice number")
    if len(filepaths) == 0:
        return ["no file found"]
    list_pdf_files = []
    for filepath in filepaths:
        # convert_pdf_file(filepath)
        if invoice_number in pdf_page_content(filepath):
            list_pdf_files.append(filepath)
    if list_pdf_files == []:
        return ["no file found"]
    else:
        return list_pdf_files


def pdf_page_content(filepath: str):
    try:
        reader = PyPDF2.PdfReader(open(filepath, 'rb'), strict=False)
        return reader.pages[0].extract_text()

    except:
        raise Exception("malformed pdf file")


def pdf_files(folder: str) -> list[str]:
    list_of_pdf_files = []
    for root, subFolders, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, "*.pdf"):
            list_of_pdf_files.append(os.path.join(root + os.sep, filename).replace("\\", "/"))

    return list_of_pdf_files
