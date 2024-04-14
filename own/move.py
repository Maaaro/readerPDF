def move_files(input_dir: str, output_dir: str):
    if len(input_dir) == 0:
        raise Exception('Empty input directory')
    if len(output_dir) == 0:
        raise Exception('Empty output directory')
    create_file(output_dir + 'file.pdf')

def create_file(filename: str) -> None:
    open(filename, 'w').close()
