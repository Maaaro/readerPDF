import glob
import os

import pytest
from PyPDF2 import PdfReader

def find_invoice(invoices_folder: str, invoice_number: str) -> str:
    invoice_filepaths = glob.glob(invoices_folder + "/*.pdf")
    if len(invoice_number) == 0:
        raise Exception("empty invoice number")
    if len(invoice_filepaths) == 0:
        return "no file found"

    try:
        reader = PdfReader(invoice_filepaths[0])
        textFromPDF: str = reader.pages[0].extract_text()
        if invoice_number in textFromPDF:
            return os.path.basename(invoice_filepaths[0])
        return "no file found"
    except:
        raise Exception("malformed pdf file")



def test_one_invoice_one_file():
    invoice_filename = find_invoice("find_invoice_resources",
                                    "FV/2022/08/1253/3/11034")
    assert invoice_filename == "FV_2022_08_1253_3_11034-V1457523.pdf"

def test_pdf_file():
    invoice_filename = find_invoice("None pdf file",
                                    "FV/2022/08/1253/3/11034")
    assert invoice_filename == "no file found"

def test_empty_folder():
    invoice_filename = find_invoice("empty", "FV/2022/08/1253/3/11034")
    assert invoice_filename == "no file found"

def test_empty_invoice_number():
    with pytest.raises(Exception) as e:
        find_invoice("empty", "")
    assert str(e.value) == "empty invoice number"

def test_malformed_pdf():
    with pytest.raises(Exception) as e:
        find_invoice("malformed pdf", "FV/2022/08/1253/3/11034")
    assert str(e.value) == "malformed pdf file"

def test_no_match():
    invoice_filename = find_invoice("no match for invoice number",
                                    "FV/007/00/0000/0/0004")
    assert invoice_filename == "no file found"
