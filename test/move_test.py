# todo wejścia: folder z fakturami, folder z wyciągami, excel z wydatki,
#               ściezki do wszystkich folderów
# todo wyjścia: folder wynikowy

import os.path

from pytest import raises

from own.move import run_program

def test_standard():
    run_program('input', 'output', [])

def test_validate_non_empty_input_directory():
    with raises(Exception) as exp:
        run_program('', 'output', [])
    assert str(exp.value) == 'Empty input directory'

def test_validate_non_empty_output_directory():
    with raises(Exception) as exp:
        run_program('output', '', [])
    assert str(exp.value) == 'Empty output directory'

def test_copies_file_from_input_directory():
    create_file("../resource/bankStatements/a.pdf", 'car')
    run_program("../resource/bankStatements/", "../resource/tmp/", ['a.pdf'])
    assert read_file("../resource/tmp/a.pdf") == 'car'

def test_copies_two_files_from_input():
    create_file("../resource/bankStatements/a.pdf", 'car1')
    create_file("../resource/bankStatements/b.pdf", 'car2')
    run_program("../resource/bankStatements/", "../resource/tmp/", ['a.pdf', 'b.pdf'])
    assert read_file("../resource/tmp/b.pdf") == 'car2'

def test_rename_filename_from_output_directory():
    remove_if_exists("aaa.pdf")
    create_file("../resource/bankStatements/a.pdf",'car')
    run_program("../resource/bankStatements/","../resource/tmp/",['a.pdf'])
    rename_filename("../resource/tmp/","a.pdf","aaa.pdf")

def remove_if_exists(filename: str) -> None:
    if os.path.isfile(filename):
        os.remove(filename)

def read_file(filename: str) -> str:
    with open(filename) as file:
        return file.read()

def create_file(filename: str, body: str) -> None:
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    with open(filename, mode='w') as file:
        file.write(body)

def rename_filename(output_dir: str,filename: str,new_filename: str) -> None:
    if not os.path.isdir(os.path.dirname(output_dir+filename)):
        os.rename(output_dir+filename,new_filename)