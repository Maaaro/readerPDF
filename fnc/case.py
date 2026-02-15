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


def remove_empty_Invoice_ID_rows_from_df(df: DataFrame) -> DataFrame:
    df = df[df.Invoice_ID.notna() & (df.Invoice_ID != "")]
    return df


def read_input_cases(path: str) -> tuple[list[Case], DataFrame]:
    cases = []
    try:
        df = pd.read_excel(path, sheet_name=0, engine='openpyxl')
        df_without_None = remove_empty_Invoice_ID_rows_from_df(df)
    except FileNotFoundError:
        raise Exception('Failed to open input cases file, file does not exist.')
    for row_index, row_cells in df_without_None.iterrows():
        # if pd.isna(row_cells['Invoice_ID']):
        # raise Exception(f'Row #{row_index + 1} does not contain an invoice number.')
        if pd.isna(row_cells['Lp']):
            raise Exception(f'Row #{row_index + 1} does not contain an LP number.')
        cases.append(convert_row_to_case(row_cells))
    return cases, df_without_None


def convert_row_to_case(row: pd.Series) -> Case:
    return Case(
        providerInvoiceNumber=str(row['Invoice_ID']),
        filePrefix=str(row['Lp']),
        workflowNumber=get_cell_optional(row, 'WF'))


def get_cell_optional(row: pd.Series, column: str) -> Optional[str]:
    if pd.isna(row[column]):
        return None
    return row[column]


def update_excel_df(main_df: DataFrame, found_invoices: list[str], excel_path: str) -> None:
    main_df = main_df.drop(columns="Comments", errors="ignore")
    main_df["Comments"] = main_df["Invoice_ID"].apply(
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


def merge_df_with_found_invoices(found_invoices: list[str], main_df: DataFrame) -> DataFrame:
    found_invoices_df = change_list_to_df(found_invoices)
    inner_join = pd.merge(main_df, found_invoices_df[["invoice_number", "Comments"]], left_on="Invoice_ID",
                          right_on="invoice_number",
                          how="left").drop(columns="invoice_number")
    return inner_join


def change_list_to_df(found_invoices: list[str]) -> DataFrame:
    found_invoices_df = pd.DataFrame(found_invoices, columns=["invoice_number"])
    found_invoices_df["Comments"] = "File was found"
    return found_invoices_df
