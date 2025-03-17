from dataclasses import dataclass
from typing import Optional

import pandas as pd

@dataclass
class Case:
    providerInvoiceNumber: str
    filePrefix: str
    workflowNumber: Optional[str]

def read_input_cases(path: str) -> list[Case]:
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
    return cases

def convert_row_to_case(row: pd.Series) -> Case:
    return Case(
        providerInvoiceNumber=str(row['Nr fv']),
        filePrefix=str(row['Lp']),
        workflowNumber=get_cell_optional(row, 'WF'))

def get_cell_optional(row: pd.Series, column: str) -> Optional[str]:
    if pd.isna(row[column]):
        return None
    return row[column]
