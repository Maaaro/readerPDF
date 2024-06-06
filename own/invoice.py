import fnmatch
import os
import fitz


def find_invoice(invoices_folder: str, invoice_number: str) -> list[str]:
    filepaths: list[str] = pdf_files(invoices_folder)
    if len(invoice_number) == 0:
        raise Exception("empty invoice number")
    if len(filepaths) == 0:
        return ["no file found"]
    lista_komentarzy = []
    lista_sciezek = []
    for filepath in filepaths:
        list_pdf_files = []
        komentarz = []
        with fitz.open(filepath) as pdf_file:
            file_content = ""

            for page in pdf_file:
                file_content += page.get_text().strip()
            if invoice_number in file_content:
                list_pdf_files.append(filepath)
                komentarz.append("ok")
            # print(list_pdf_files)
            lista_sciezek.append(list_pdf_files)
            lista_komentarzy.append(komentarz)
    # print("suma wyników " + str(lista_sciezek))
    total = []
    for list, koment in zip(lista_sciezek, lista_komentarzy):
        for number, ko in zip(list, koment):
            if 'ok' in ko:
                total.append(number)
    return total

def pdf_page_content(filepath: str) -> str:
    try:
        with fitz.open(filepath, 'rb') as pdf_file:
            page_content = ""

            for page in pdf_file:
                page_content += page.get_text().strip()

            return page_content
    except:
        return "malformed pdf file"

def pdf_files(folder: str) -> list[str]:
    list_of_pdf_files = []
    for root, subFolders, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, "*.pdf"):
            path = os.path.join(root + os.sep, filename).replace("\\", "/")
            list_of_pdf_files.append(path)

    return list_of_pdf_files
