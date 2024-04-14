# todo wejścia: folder z fakturami, folder z wyciągami, excel z wydatki,
#               ściezki do wszystkich folderów
# todo wyjścia: folder wynikowy

from pytest import raises

from own.move import move_files

import os.path

def test_standard():
    move_files('input', 'output')

def test_validate_non_empty_input_directory():
    with raises(Exception) as exp:
        move_files('', 'output')
    assert str(exp.value) == 'Empty input directory'

def test_validate_non_empty_output_directory():
    with raises(Exception) as exp:
        move_files('output', '')
    assert str(exp.value) == 'Empty output directory'

def test_creates_file_in_output_directory():
    remove_if_exists('../resource/tmp/file.pdf')
    move_files('irrelevant', '../resource/tmp/')
    assert os.path.isfile('../resource/tmp/file.pdf')

def remove_if_exists(filename: str) -> None:
    if os.path.isfile(filename):
        os.remove(filename)
