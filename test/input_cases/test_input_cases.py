from pathlib import Path

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from pytest import raises

from fnc.case import Case, read_input_cases
from test.project_path import project_path


def test_parse_input_cases_from_xlsx_file():
    test_path = project_path("input_cases/fixture/inputCases.valid.xlsx")
    df = create_complex_df()
    create_excel_file(df, test_path)
    input_cases, _ = read_input_cases(test_path)

    assert input_cases == [
        Case('FV/2022/08/1253/3/11034', '1', 'wf1'),
        Case('eIC155687424', '2', 'wf2'),
        Case('100156909563/RA/2024', '3', None),
        Case('PL3654810710', '4', None),
        Case('F/000895/23/RO', '5', None),
        Case('26908/BR/2023', '6', None),
        Case('8492', '7', 'wf7'),
    ]
    cleanup_test_file(test_path)


def test_remove_rows_with_empty_invoice_ID():
    test_path = project_path("input_cases/fixture/inputCases.empty_invoice_id.xlsx")
    df = create_df_with_empty_Invoice_number_to_remove()
    create_excel_file(df, test_path)
    input_cases, _ = read_input_cases(test_path)
    assert input_cases == [
        Case('FV/2022/08/1253/3/11034', '1', 'wf1'),
        Case('100156909563/RA/2024', '3', None),
        Case('PL3654810710', '4', None),
        Case('F/000895/23/RO', '5', None),
        Case('8492', '7', 'wf7'),
    ]
    cleanup_test_file(test_path)

def test_empty_lp_number_in_any_row_is_malformed_file():
    test_path = project_path("input_cases/fixture/inputCases.emptyLpNumber.xlsx")
    df = create_df_with_empty_Lp_number()
    create_excel_file(df, test_path)
    with raises(Exception) as exception_info:
        input_cases, _ = read_input_cases(test_path)
    assert str(exception_info.value) == 'Row #1 does not contain an LP number.'
    cleanup_test_file(test_path)


def test_reading_a_missing_file_raises_exception():
    with raises(Exception) as exception_info:
        input_cases, _ = read_input_cases(project_path('input_cases/fixture/missing-file'))
    assert str(exception_info.value) == 'Failed to open input cases file, file does not exist.'


def create_df_with_empty_Lp_number() -> DataFrame:
    data = {
        "Lp": [None],
        "Invoice_ID": ["FV/2025/21"],
        "WF": ["wf1"],
    }
    df = pd.DataFrame(data)
    return df


def create_df_with_empty_Invoice_number() -> DataFrame:
    data = {
        "Lp": ["1"],
        "Invoice_ID": [None],
        "WF": ["wf1"],
    }
    df = pd.DataFrame(data)
    return df


def create_complex_df() -> DataFrame:
    data = {
        "Lp": ["1", "2", "3", "4", "5", "6", "7"],
        "Invoice_ID": ["FV/2022/08/1253/3/11034", "eIC155687424", "100156909563/RA/2024", "PL3654810710", "F/000895/23/RO",
                  "26908/BR/2023", "8492"],
        "WF": ["wf1", "wf2", "", "", "", "", "wf7"],
    }
    df = pd.DataFrame(data)
    return df

def create_df_with_empty_Invoice_number_to_remove():
    data = {
        "Lp": ["1", "2", "3", "4", "5", "6", "7"],
        "Invoice_ID": ["FV/2022/08/1253/3/11034", None, "100156909563/RA/2024", "PL3654810710", "F/000895/23/RO",
                  None, "8492"],
        "WF": ["wf1", "wf2", "", "", "", "", "wf7"],
    }
    df = pd.DataFrame(data)
    return df

def create_excel_file(df: DataFrame, path: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False, engine="openpyxl")


def cleanup_test_file(path: Path) -> None:
    path = Path(path)
    if path.exists():
        path.unlink()
    parent_dir = path.parent
    while parent_dir != Path(__file__).parent and not any(parent_dir.iterdir()):
        parent_dir.rmdir()
        parent_dir = parent_dir.parent
