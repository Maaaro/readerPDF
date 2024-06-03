import codecs


def run_program(invoices_folder: str, invoice_found: str, output_dir: str, filenames: list[str],
                fileprefix: str) -> None:
    if len(invoices_folder) == 0:
        raise Exception('Empty input directory')
    if len(output_dir) == 0:
        raise Exception('Empty output directory')

    for i, filename in enumerate(filenames):
        # with open(invoices_folder+"/"+invoice_found, encoding="utf8") as file:
        with codecs.open(invoices_folder + "/" + invoice_found, encoding="latin-1") as file:
            foo = file.read()

        create_file(output_dir + str(filename) + fileprefix, foo)
        file.close()


def create_file(filepath: str, content: str) -> None:
    with codecs.open(filepath, encoding="latin-1", mode="w+") as file:
        file.write(content)
        file.close()
