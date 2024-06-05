import fnmatch
import os

import fitz

def find_invoice(invoices_folder: str, invoice_number: str) -> list[str]:
    filepaths: list[str] = pdf_files(invoices_folder)
    if len(invoice_number) == 0:
        raise Exception("empty invoice number")
    if len(filepaths) == 0:
        return []
    list_pdf_files = []
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

    # list_pdf_files = []
    # suma_komentarzy = []
    # poprawne_sciezki = []
    # filepath_list = []
    # for filepath in filepaths:
    #     # convert_pdf_file(filepath)
    #     file_content = pdf_page_content(filepath)
    #     if invoice_number in file_content:
    #         list_pdf_files.append(filepath)
    #         filepath_list.append("found")
    #     else:
    #         if file_content == 'malformed pdf file':
    #             list_pdf_files.append('malformed pdf file')
    #         else:
    #             list_pdf_files.append('no file found')
    # suma_komentarzy.append(list_pdf_files)
    # poprawne_sciezki.append(filepath_list)
    # # if list_pdf_files == []:
    # #     return ["no file found"]
    # # else:
    # #     return list_pdf_files
    # found_files = []
    # ffiles = []
    # for (komentarz, sciezka) in zip(suma_komentarzy, poprawne_sciezki):
    #     for (number, link) in zip(komentarz, sciezka):
    #         if "found" in number:
    #             ffiles.append(link)
    # if len(ffiles) == 0:
    #     return ['no file found']
    # else:
    #     return found_files.insert(0,link)

def pdf_page_content(filepath: str) -> str:
    try:
        with fitz.open(filepath, 'rb') as pdf_file:
            page_content = ""

            for page in pdf_file:
                page_content += page.get_text().strip()

            return page_content
    except:
        # raise Exception("malformed pdf file")
        return "malformed pdf file"

def pdf_files(folder: str) -> list[str]:
    list_of_pdf_files = []
    for root, subFolders, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, "*.pdf"):
            path = os.path.join(root + os.sep, filename).replace("\\", "/")
            list_of_pdf_files.append(path)

    return list_of_pdf_files
