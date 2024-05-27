import glob
import os

from PyPDF2 import PdfReader


def find_invoice(invoices_folder: str, invoice_number: str) -> str:
    filepaths: list[str] = pdf_files(invoices_folder)
    if len(invoice_number) == 0:
        raise Exception("empty invoice number")
    if len(filepaths) == 0:
        return "no file found"

    for filepath in filepaths:
        if invoice_number in pdf_page_content(filepath):
            return os.path.basename(filepath)
    return "no file found"


def pdf_page_content(filepath: str):
    try:
        reader = PdfReader(filepath)
        return reader.pages[0].extract_text()
    except:
        raise Exception("malformed pdf file")


def pdf_files(folder: str) -> list[str]:
    return glob.glob(folder + "/*.pdf")
