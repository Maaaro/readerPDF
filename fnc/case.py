from dataclasses import dataclass
from typing import Optional

import pandas as pd
from openpyxl import load_workbook
from pandas import DataFrame


@dataclass
class Case:
    providerInvoiceNumber: str
    filePrefix: str
    workflowNumber: Optional[str]


def remove_empty_invoice_id_rows_from_df(df: DataFrame) -> DataFrame:
    return df[df.Invoice_ID.notna() & (df.Invoice_ID != "")]


def read_input_cases(path: str) -> tuple[list[Case], DataFrame]:
    cases = []
    try:
        df = pd.read_excel(path, sheet_name=0, engine='openpyxl')
        df_without_none = remove_empty_invoice_id_rows_from_df(df)
    except FileNotFoundError:
        raise Exception('Failed to open input cases file, file does not exist.')
    for i, (row_index, row_cells) in enumerate(df_without_none.iterrows()):
        if pd.isna(row_cells['Lp']):
            raise Exception(f'Row #{i + 1} does not contain an LP number.')
        cases.append(convert_row_to_case(row_cells))
    return cases, df_without_none


def convert_row_to_case(row: pd.Series) -> Case:
    return Case(
        providerInvoiceNumber=str(row['Invoice_ID']),
        filePrefix=str(row['Lp']),
        workflowNumber=get_cell_optional(row, 'WF'))


def get_cell_optional(row: pd.Series, column: str) -> Optional[str]:
    if pd.isna(row[column]):
        return None
    return str(row[column])


def update_excel_df(main_df: DataFrame, found_invoices: list[str], excel_path: str):
    df = main_df.copy()

    df["Comments"] = df["Invoice_ID"].apply(
        lambda x: "File was found" if x in found_invoices else "File wasn't found")
    try:
        sheet_name = load_workbook(excel_path).sheetnames[0]
    except Exception as e:
        print(f"Could not load workbook: {e}")
        sheet_name = "Sheet1"
    try:
        main_df.to_excel(excel_path, sheet_name=sheet_name, engine="openpyxl", index=False)
    except Exception as e:
        raise Exception(f"Failed to save excel file {e}")
