import codecs

def copy_pdf_file(invoices_folder: str, invoice_found: str, output_dir: str, filenames: str) -> None:
    if len(invoices_folder) == 0:
        raise Exception('Empty input directory')
    if len(output_dir) == 0:
        raise Exception('Empty output directory')

    with codecs.open(invoice_found, encoding="latin-1") as file:
        foo = file.read()
        file.close()
        create_file(output_dir + str(filenames), foo)


def create_file(filepath: str, content: str) -> None:
    with codecs.open(filepath, encoding="latin-1", mode="w+") as file:
        file.write(content)
        file.close()
