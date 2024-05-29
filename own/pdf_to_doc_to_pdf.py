import os
import re
from io import BytesIO
import mammoth
import pdfkit
import pikepdf
from PyPDF2 import PdfReader
from docx import Document
from docx2pdf import convert
import pymupdf


def convert_pdf_file(filepath: str, password=None, pymupdf=None):
    document = Document()
    newpath = filepath.replace(".pdf", "docx")

    idata = open(filepath, "rb").read()
    ibuffer = BytesIO(idata)

    if password is None:
        try:
            return PdfReader(ibuffer)  # if this works: fine!
        except:
            pass

    doc = pymupdf.open("pdf", ibuffer)
    if password is not None:
        rc = doc.authenticate(password)
        if not rc > 0:
            raise ValueError("wrong password")
    c = doc.tobytes(garbage=3, deflate=True)
    del doc  # close & delete doc
    return PdfReader(BytesIO(c))
