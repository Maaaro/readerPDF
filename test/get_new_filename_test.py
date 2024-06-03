from own.invoice_id import new_filenames

def test_no_excel_file():
    new_filename = new_filenames("None pdf file/*.xlsx", "One", "", "")
    assert new_filename == "file not found"

def test_empty_table():
    new_filename = new_filenames("get_invoice_id_tests_folder/faktury_id.xlsx", "EmptyTable", "Lp", "")
    assert new_filename == "data not found"

def test_empty_new_filename_column():
    new_filename = new_filenames("get_invoice_id_tests_folder/faktury_id.xlsx", "NoSerachColumn",
                                 "Lp", "")
    assert new_filename == "column not found"

def test_one_new_filename():
    new_filename = new_filenames("get_invoice_id_tests_folder/faktury_id.xlsx", "One", "Lp", "_fv.pdf")
    assert new_filename == ["1_fv.pdf"]

def test_two_new_filename():
    new_filename = new_filenames("get_invoice_id_tests_folder/faktury_id.xlsx", "Two", "Lp", "_fv.pdf")
    assert new_filename == ["1_fv.pdf", "2_fv.pdf"]
