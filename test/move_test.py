import os.path

from pytest import raises

from own.invoice import pdf_files
from own.invoice_id import new_filenames
from own.move import run_program


# def test_standard():
#     run_program('input', '', 'output', '', '')


def test_validate_non_empty_input_directory():
    with raises(Exception) as exp:
        run_program('', '', 'output', '')
    assert str(exp.value) == 'Empty input directory'


def test_validate_non_empty_output_directory():
    with raises(Exception) as exp:
        run_program('output', '', '', '')
    assert str(exp.value) == 'Empty output directory'


def test_copies_file_from_input_directory():
    create_file("../resource/bankStatements/e.txt", 'car3')
    run_program("../resource/bankStatements/", 'e.txt', "../resource/tmp/", '5_wb.txt')
    assert read_file("../resource/tmp/5_wb.txt") == 'car3'


def test_copies_two_files_from_input():
    create_file("../resource/bankStatements/a.txt", 'car1')
    create_file("../resource/bankStatements/b.txt", 'car2')
    run_program("../resource/bankStatements", 'a.txt', "../resource/tmp/", '1_wb.txt')
    run_program("../resource/bankStatements", 'b.txt', "../resource/tmp/", '2_wb.txt')
    assert read_file("../resource/tmp/2_wb.txt") == 'car2'


def test_rename_file_with_bank_statement_ordinal_number():
    remove_if_exists("../resource/tmp/a.txt")
    create_file("../resource/bankStatements/a.txt", 'green')
    run_program("../resource/bankStatements", 'a.txt', "../resource/tmp/", '1_wb.txt')
    assert read_file("../resource/tmp/1_wb.txt") == 'green'


def test_move_two_file_with_bank_statement_ordinal_number():
    create_file("../resource/bankStatements/c.txt", 'blue')
    create_file("../resource/bankStatements/d.txt", 'red')
    run_program("../resource/bankStatements/", 'c.txt', "../resource/tmp/", '3_wb.txt')
    run_program("../resource/bankStatements/", 'd.txt', "../resource/tmp/", '4_wb.txt')

    assert read_file("../resource/tmp/4_wb.txt") == 'red'


def test_two_files_with_the_same_invoice_number():
    invoicefound = ["fv_pl_1_1bf5a3c1809c7fe44bd2e78915c3.pdf", "fv_pl_1_1bf5a3c1809c7fe44bd07882e78915c3.pdf"]
    # "26908/BR/2023"
    new_filename = new_filenames("get_invoice_id_tests_folder/faktury_id.xlsx", "TheSame", "Lp", "_fv.pdf")
    run_program("test/two_file_with_the_same_invoice_number", invoicefound[1], "../resource/tmp/", new_filename)

    output = pdf_files("../resource/tmp/")
    assert output == ["aa_fv.pdf", "aa1_fv.pdf"]


def remove_if_exists(filename: str) -> None:
    if os.path.isfile(filename):
        os.remove(filename)


def read_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()


def create_file(filename: str, body: str) -> None:
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    with open(filename, mode='w') as file:
        file.write(body)


def rename_filename(output_dir: str, filename: str, new_filename: str) -> None:
    if os.path.isdir(os.path.dirname(output_dir + filename)):
        os.rename(output_dir + filename, output_dir + new_filename)
