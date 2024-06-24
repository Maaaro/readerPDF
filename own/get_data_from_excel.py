import pandas as pd
from own.copy_pdf import create_file

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
    list_of_new_filenames = df[new_filename_column].to_list()
    list_of_new_filenames_with_prefix = [str(int(i)) + fileprefix for i in list_of_new_filenames]

    return list_of_new_filenames_with_prefix

def add_comment(excelpath: str, sheetname: str, status_invoice_list: list, fileprefix: str):
    try:
        df = pd.read_excel(excelpath, sheet_name=sheetname, engine="openpyxl")
        if df.empty:
            return "data not found"
    except:
        return "file not found"
    create_file("C:/Users/m.mrowka/PycharmProjects/readerPDF/resource/tmp/temporary_page_content.txt", str(status_invoice_list))
    df = df.sort_values("Lp", ascending=True)
    df = df.assign(**{"Komentarz do " + fileprefix: status_invoice_list})
    with pd.ExcelWriter(excelpath, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
        df.to_excel(writer, sheet_name=sheetname, index=False)
    return list(df)

def remove_comment(excelpath, sheetname, columnname):
    try:
        df = pd.read_excel(excelpath, sheet_name=sheetname, engine="openpyxl")
        df = df.drop(columns=[columnname])
        if df.empty:
            return "data not found"
    except:
        return "file not found"

def list_of_WF_case(excelpath: str, sheetname: str, wf_number_columnname: str):
    try:
        df = pd.read_excel(excelpath, sheet_name=sheetname, engine="openpyxl")
        if df.empty:
            return "data not found"
        if wf_number_columnname not in df.columns:
            return "column not found"
    except:
        return "file not found"
    df = df.sort_values(["Lp"], ascending=True)
    df = df.replace("", "empty")
    wf_cases = df[wf_number_columnname].to_list()
    return wf_cases
