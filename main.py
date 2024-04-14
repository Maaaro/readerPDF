# importing all the required modules
import glob
import PyPDF2
import pandas as pd

# creating a list with a directions of .pdf
# def listOfLinks():
# try:
sourceList = glob.glob("resource/invoice/*.pdf")
print("Lista zrodel: ", sourceList)
# except:
#     print("Brak plików PDF w katalogu!")

# def listofstringtosearch():

df = pd.read_excel(r"resource/test.xlsx", sheet_name="Arkusz1")
# print(df)

df = df.astype(str)
list_of_id = df["NR faktury"].to_list()

print(list_of_id)

# def searchingTrougthTheList(sourceList=None):
iterate = 1
for i in sourceList:
    # creating a pdf reader object

    reader = PyPDF2.PdfReader(sourceList[iterate])
    iterate = iterate + 1
    # print("reader: ",reader)
    # print the number of pages in pdf file
    print("\nLiczba stron: ", len(reader.pages), i)

    # print the text of the first page
    textFromPDF = reader.pages[0].extract_text()
    # print(texttosearch)

    # searchString = "PG/1253/3/373/118"
    for id in list_of_id:
        if id in textFromPDF:
            print("\n-------Tak znaleziono-------->  ", id)
            _match = 1
            break
        else:
            print("Nie znaleziono ->", id)
            _match = 0
