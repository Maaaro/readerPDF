import glob

import PyPDF2
import pandas as pd

invoice_filepaths = glob.glob("resource/invoice/*.pdf")
print("Lista zrodel: ", invoice_filepaths)

df = pd.read_excel(r"resource/test.xlsx", sheet_name="Arkusz1")

df = df.astype(str)
list_of_id = df["NR faktury"].to_list()

print(list_of_id)

for filepath in invoice_filepaths:
    reader = PyPDF2.PdfReader(filepath)

    print("\nLiczba stron: ", len(reader.pages), filepath)
    textFromPDF = reader.pages[0].extract_text()
    for id in list_of_id:
        if id in textFromPDF:
            print("\n-------Tak znaleziono-------->  ", id)
            _match = 1
            break
        print("Nie znaleziono ->", id)
        _match = 0
