# importing all the required modules
import glob
import PyPDF2
from svgwrite import data

# creating a list with a directions of .pdf
def listOfLinks():
    try:
        sourceList = glob.glob("C:/Users/mrowk/Downloads/*.pdf")
        print("Lista zrodel: ", sourceList)
    except:
        print("Brak plików PDF w katalogu!")

def searchingTrougthTheList(sourceList=None):
    iterate = 0
    for i in sourceList[:20]:
        # creating a pdf reader object
        iterate = iterate + 1
        reader = PyPDF2.PdfReader(sourceList[iterate])

        # print the number of pages in pdf file
        print("Liczba stron: ", len(reader.pages))

        # print the text of the first page
        textFromPDF = reader.pages[0].extract_text()
        # print(texttosearch)

        searchString = "PG/1253/3/373/118"

        if searchString not in textFromPDF:
            print("Nie znaleziono", searchString)
            _match = 0
        else:
            print("-------Tak znaleziono-------- ", searchString)
            _match = 1