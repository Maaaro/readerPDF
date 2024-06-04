from own.invoice_id import invoice_numbers, add_comment, remove_comment


def test_no_excel_file():
    invoice_number = invoice_numbers("None pdf file/*.xlsx", "One", "")
    assert invoice_number == "file not found"

def test_empty_table():
    invoice_number = invoice_numbers("get_invoice_id_tests_folder/faktury_id.xlsx", "EmptyTable", "NR faktury")
    assert invoice_number == "data not found"

def test_empty_invoice_number_column():
    invoice_number = invoice_numbers("get_invoice_id_tests_folder/faktury_id.xlsx", "NoSerachColumn",
                                            "NR faktury")
    assert invoice_number == "column not found"

def test_one_invoice_number():
    invoice_number = invoice_numbers("get_invoice_id_tests_folder/faktury_id.xlsx", "One", "NR faktury")
    assert invoice_number == ["26908/BR/2023"]

def test_two_invoice_number():
    invoice_number = invoice_numbers("get_invoice_id_tests_folder/faktury_id.xlsx", "Two", "NR faktury")
    assert invoice_number == ["26908/BR/2023", "PL3654810710"]

def test_new_comment():
    remove_comment("get_invoice_id_tests_folder/faktury_id.xlsx", "AddComment","Komentarz do 1_wf" )
    comment = add_comment("get_invoice_id_tests_folder/faktury_id.xlsx", "AddComment", [1,2], "1_wf")
    commentexist = "Komentarz do 1_wf" in comment
    assert commentexist == True
