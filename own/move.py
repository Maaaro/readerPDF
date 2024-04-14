def run_program(input_dir: str, output_dir: str, filenames: list[str]) -> None:
    if len(input_dir) == 0:
        raise Exception('Empty input directory')
    if len(output_dir) == 0:
        raise Exception('Empty output directory')

    for filename in filenames:
        with open(input_dir + filename) as file:
            foo = file.read()
        create_file(output_dir + filename, foo)

def create_file(filepath: str, content: str) -> None:
    file = open(filepath, 'w')
    file.write(content)
    file.close()
