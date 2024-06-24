# import glob
#
# import pandas as pd
# from PyPDF2 import PdfReader
#
# invoice_filepaths = glob.glob("resource/invoice/*.pdf")
# print("Lista zrodel: ", invoice_filepaths)
#
# df = pd.read_excel(r"resource/tests.xlsx", sheet_name="Arkusz1")
#
# df = df.astype(str)
# list_of_id = df["NR faktury"].to_list()
#
# print(list_of_id)
#
# for filepath in invoice_filepaths:
#     reader = PdfReader(filepath)
#
#     print("\nLiczba stron: ", len(reader.pages), filepath)
#     first_page = reader.pages[0]
#     textFromPDF = first_page.extract_text()
#     for id in list_of_id:
#         if id in textFromPDF:
#             print("\n-------Tak znaleziono-------->  ", id)
#             _match = 1
#             break
#         print("Nie znaleziono ->", id)
#         _match = 0
