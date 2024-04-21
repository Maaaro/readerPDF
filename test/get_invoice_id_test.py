import pytest

from own.invoice_id import extract_invoice_id

def test_no_excel_file():
    invoice_number = extract_invoice_id(r"C:\Users\mrowk\OneDrive\Desktop\testy\faktury_id.xlsx", "One")
    assert invoice_number == "file not found"






# def test_one_invoice_id():
#     invoice_id = find_invoice_id(r"C:\Users\mrowk\OneDrive\Desktop\testy\faktury_id.xlsx", "26908/BR/2023")
#     assert invoice_id

