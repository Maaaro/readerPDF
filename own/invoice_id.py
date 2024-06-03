import pandas as pd


def invoice_numbers(excelpath: str, sheetname: str, invoice_number_columnname: str):
    try:
        df = pd.read_excel(excelpath, sheet_name=sheetname, engine="openpyxl")
        if df.empty:
            return "data not found"
        if invoice_number_columnname not in df.columns:
            return "column not found"
    except:
        return "file not found"
    df = df.sort_values(["Lp"], ascending=True)
    invoice_numbers = df[invoice_number_columnname].to_list()
    return invoice_numbers


def new_filenames(excelpath: str, sheetname: str, new_filename_column: str, fileprefix: str):
    try:
        df = pd.read_excel(excelpath, sheet_name=sheetname, engine="openpyxl")
        if df.empty:
            return "data not found"
        if new_filename_column not in df.columns:
            return "column not found"
    except:
        return "file not found"

    df = df.sort_values("Lp", ascending=True)
    new_filename = df[new_filename_column].to_list()
    new_filename = [str(int(i)) + fileprefix for i in new_filename]

    return new_filename


def add_comment(excelpath: str, sheetname: str, status_invoice_list: list, fileprefix: str):
    try:
        df = pd.read_excel(excelpath, sheet_name=sheetname, engine="openpyxl")
        if df.empty:
            return "data not found"
    except:
        return "file not found"
    df = df.sort_values("Lp", ascending=True)
    df = df.assign(Komentarz=status_invoice_list)
    df.to_excel(excelpath)
