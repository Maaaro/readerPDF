import glob
import os

from PyPDF2 import PdfReader

def find_invoice(invoices_folder: str, invoice_number: str) -> str:
    invoice_filepaths: list[str] = glob.glob(invoices_folder + "/*.pdf")
    if len(invoice_number) == 0:
        raise Exception("empty invoice number")
    if len(invoice_filepaths) == 0:
        return "no file found"

    if invoice_number in pdf_page_content(invoice_filepaths[0]):
        return os.path.basename(invoice_filepaths[0])
    return "no file found"

def pdf_page_content(filepath: str):
    try:
        reader = PdfReader(filepath)
        return reader.pages[0].extract_text()
    except:
        raise Exception("malformed pdf file")
