from own.invoice_id import extract_invoice_number

def test_no_excel_file():
    invoice_number = extract_invoice_number("None pdf file/*.xlsx", "One", "")
    assert invoice_number == "file not found"

def test_empty_table():
    invoice_number = extract_invoice_number("get_invoice_id_tests_folder/faktury_id.xlsx", "EmptyTable", "NR faktury")
    assert invoice_number == "data not found"

def test_empty_invoice_number_column():
    invoice_number = extract_invoice_number("get_invoice_id_tests_folder/faktury_id.xlsx", "NoSerachColumn",
                                            "NR faktury")
    assert invoice_number == "column not found"

def test_one_invoice_number():
    invoice_number = extract_invoice_number("get_invoice_id_tests_folder/faktury_id.xlsx", "One", "NR faktury")
    assert invoice_number == ["26908/BR/2023"]

def test_two_invoice_number():
    invoice_number = extract_invoice_number("get_invoice_id_tests_folder/faktury_id.xlsx", "Two", "NR faktury")
    assert invoice_number == ["26908/BR/2023", "PL3654810710"]
