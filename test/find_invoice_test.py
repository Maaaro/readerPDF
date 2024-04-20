import glob
import os

def find_invoice(invoices_folder: str, invoice_number: str) -> str:
    invoice_filepaths = glob.glob(invoices_folder + "/*")
    return os.path.basename(invoice_filepaths[0])

def test_one_invoice_one_file():
    invoice_filename = find_invoice("find_invoice_resources",
                                    "FV/2022/08/1253/3/11034")
    assert invoice_filename == "FV_2022_08_1253_3_11034-V1457523.pdf"
