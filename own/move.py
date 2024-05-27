def run_program(invoices_folder: str, output_dir: str, filenames: list[str], fileprefix: str) -> None:
    if len(invoices_folder) == 0:
        raise Exception('Empty input directory')
    if len(output_dir) == 0:
        raise Exception('Empty output directory')

    for i, filename in enumerate(filenames):
        with open(invoices_folder + "/" + filename) as file:
            foo = file.read()

        create_file(output_dir + str(i + 1) + fileprefix, foo)


def create_file(filepath: str, content: str) -> None:
    file = open(filepath, 'w')
    file.write(content)
    file.close()
