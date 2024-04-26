import pandas as pd

def invoice_numbers(excelpath: str, sheetname: str, invoice_number_columnname: str):
    try:
        df = pd.read_excel(excelpath, sheet_name=sheetname)
        if df.empty:
            return "data not found"
        if invoice_number_columnname not in df.columns:
            return "column not found"
    except:
        return "file not found"
    invoice_numbers = df[invoice_number_columnname].to_list()
    return invoice_numbers

def new_filenames(excelpath: str, sheetname: str, new_filename_column: str):
    try:
        df = pd.read_excel(excelpath, sheet_name=sheetname)
        if df.empty:
            return "data not found"
        if new_filename_column not in df.columns:
            return "column not found"
    except:
        return "file not found"

    new_filename = df[new_filename_column].to_list()
    new_filename = [str(int(i)) + ". fv" for i in new_filename]

    return new_filename
