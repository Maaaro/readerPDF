def move_files(input_dir: str, output_dir: str):
    if len(input_dir) == 0:
        raise Exception('Empty input directory')
    if len(output_dir) == 0:
        raise Exception('Empty output directory')
