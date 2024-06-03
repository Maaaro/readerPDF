import fnmatch
import os

import PyPDF2


def find_invoice(invoices_folder: str, invoice_number: str) -> str:
    filepaths: list[str] = pdf_files(invoices_folder)
    if len(invoice_number) == 0:
        raise Exception("empty invoice number")
    if len(filepaths) == 0:
        return "no file found"

    for filepath in filepaths:
        # convert_pdf_file(filepath)
        if invoice_number in pdf_page_content(filepath):
            return os.path.basename(filepath)
    return "no file found"


def pdf_page_content(filepath: str, page=0):
    # if page is None:
    #     args = ["pdftotext", "-layout", "-q", filepath, "-"]
    # else:
    #     args = ["pdftotext", "-f", str(page), "-l", str(page), "-layout"]

    try:
        # pdfcontent = StringIO(filepath).encoding("ascii", "ignore")
        # pdfcontent = textract.process(filepath, method="pdfminer")
        # return pdfcontent

        #     with open(filepath, "rb") as f:
        #         reader = PyPDF2.PdfReader(f)
        #         if reader.is_encrypted:
        #             reader.decrypt("")
        #         page = reader.pages[page]
        #         return page.extract_text()
        reader = PyPDF2.PdfReader(open(filepath, 'rb'), strict=False)
        return reader.pages[0].extract_text()

    # txt = subprocess.check_output(args, universal_newlines=True)
    # return txt.splitlines()

    except:
        raise Exception("malformed pdf file")


def pdf_files(folder: str) -> list[str]:
    list_of_pdf_files = []
    for root, subFolders, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, "*.pdf"):
            list_of_pdf_files.append(os.path.join(root + os.sep, filename).replace("\\", "/"))

    return list_of_pdf_files
