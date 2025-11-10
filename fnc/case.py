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


def read_input_cases(path: str) -> tuple[list[Case], DataFrame]:
    cases = []
    try:
        df = pd.read_excel(path, sheet_name=0, engine='openpyxl')
    except FileNotFoundError:
        raise Exception('Failed to open input cases file, file does not exist.')
    for row_index, row_cells in df.iterrows():
        if pd.isna(row_cells['Nr fv']):
            raise Exception(f'Row #{row_index + 1} does not contain an invoice number.')
        if pd.isna(row_cells['Lp']):
            raise Exception(f'Row #{row_index + 1} does not contain an LP number.')
        cases.append(convert_row_to_case(row_cells))
    return cases, df


def convert_row_to_case(row: pd.Series) -> Case:
    return Case(
        providerInvoiceNumber=str(row['Nr fv']),
        filePrefix=str(row['Lp']),
        workflowNumber=get_cell_optional(row, 'WF'))


def get_cell_optional(row: pd.Series, column: str) -> Optional[str]:
    if pd.isna(row[column]):
        return None
    return row[column]


def update_excel_df(main_df: DataFrame, found_invoices: list[str], excel_path: str) -> None:
    if "Comments" in main_df.columns:
        main_df = main_df.drop(columns="Comments")
    df = merge_df_with_found_invoices(found_invoices, main_df)
    df = df.fillna("File wasn't found")
    try:
        wb = load_workbook(excel_path)
        sheet_name = wb.sheetnames[0]
    except:
        sheet_name = "Sheet1"

    df.to_excel(excel_path, sheet_name=sheet_name, engine="openpyxl", index=False)


def merge_df_with_found_invoices(found_invoices: list[str], main_df: DataFrame) -> DataFrame:
    found_invoices_df = change_list_to_df(found_invoices)
    inner_join = pd.merge(main_df, found_invoices_df[["invoice_number", "Comments"]], left_on="Nr fv",
                          right_on="invoice_number",
                          how="left").drop(columns="invoice_number")
    return inner_join


def change_list_to_df(found_invoices: list[str]) -> DataFrame:
    found_invoices_df = pd.DataFrame(found_invoices, columns=["invoice_number"])
    found_invoices_df["Comments"] = "File was found"
    return found_invoices_df
