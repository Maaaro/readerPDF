import os
import tempfile
import pytest

from own.find_invoices import find_invoice

def test_one_invoice_one_file():
    invoice_filename = find_invoice("find_invoice_resources",
                                    "FV/2022/08/1253/3/11034")
    assert invoice_filename == ["find_invoice_resources/FV_2022_08_1253_3_11034-V1457523.pdf"]

def test_pdf_file():
    invoice_filename = find_invoice("None pdf file",
                                    "FV/2022/08/1253/3/11034")
    assert invoice_filename == ['no file found']

def empty_folder():
    parent = tempfile.gettempdir()
    if not os.path.exists(os.path.join(parent, "empty")):
        os.makedirs(os.path.join(parent, "empty"))
    return os.path.join(parent, "empty")

def test_empty_folder():
    invoice_filename = find_invoice(empty_folder(), "FV/2022/08/1253/3/11034")
    assert invoice_filename == ['no file found']

def test_empty_invoice_number():
    with pytest.raises(Exception) as e:
        find_invoice(empty_folder(), "")
    assert str(e.value) == "empty invoice number"

def test_malformed_pdf():
    with pytest.raises(Exception) as e:
        find_invoice("malformed pdf", "FV/2022/08/1253/3/11034")
    assert str(e.value) == "Failed to open file 'malformed pdf/test.pdf'."

def test_no_match():
    invoice_filename = find_invoice("no match for invoice number",
                                    "FV/007/00/0000/0/0004")
    assert invoice_filename == []
