from pytest import raises

from fnc.case import Case, read_input_cases
from test.project_path import project_path

def test_parse_input_cases_from_xlsx_file():
    assert read_input_cases(project_path('input_cases/fixture/inputCases.valid.xlsx')) == [
        Case('FV/2022/08/1253/3/11034', '1', 'wf1'),
        Case('eIC155687424', '2', 'wf2'),
        Case('100156909563/RA/2024', '3', None),
        Case('PL3654810710', '4', None),
        Case('F/000895/23/RO', '5', None),
        Case('26908/BR/2023', '6', None),
        Case('8492', '7', 'wf7'),
    ]

def test_empty_invoice_number_in_any_row_is_malformed_file():
    with raises(Exception) as exception_info:
        read_input_cases(project_path('input_cases/fixture/inputCases.emptyInvoiceNumber.xlsx'))
    assert str(exception_info.value) == 'Row #1 does not contain an invoice number.'

def test_empty_lp_number_in_any_row_is_malformed_file():
    with raises(Exception) as exception_info:
        read_input_cases(project_path('input_cases/fixture/inputCases.emptyLpNumber.xlsx'))
    assert str(exception_info.value) == 'Row #1 does not contain an LP number.'

def test_reading_a_missing_file_raises_exception():
    with raises(Exception) as exception_info:
        read_input_cases(project_path('input_cases/fixture/missing-file'))
    assert str(exception_info.value) == 'Failed to open input cases file, file does not exist.'
