import pandas as pd

# column_name: str,

def extract_invoice_number(excelpath: str, sheetname: str, invoice_number_columnname: str):


        try:
                df = pd.read_excel(excelpath, sheet_name=sheetname)
                if df.empty:
                        return "data not found"
                if invoice_number_columnname not in df.columns:
                        return "column not found"
        except:
                df = "file not found"

        return df


# def test():
#         df2 = pd.read_excel(r"../test/get_invoice_id_tests_folder/faktury_id.xlsx", "Empty")
#         df3 = pd.read_excel(r"../test/get_invoice_id_tests_folder/faktury_id.xlsx", "One")
#         print("df2 :" + df2)
#         df2 = df2.empty
#         print("df2 " + str(df2))
#         print("df3 :" + df3)
#         df3 = df3.empty
#         print("df3 " + str(df3))
#
#
#         df = pd.read_excel(r"../test/get_invoice_id_tests_folder/faktury_id.xlsx", "Empty")
#         print(df)