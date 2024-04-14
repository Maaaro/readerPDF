# todo wejścia: folder z fakturami, folder z wyciągami, excel z wydatki,
#               ściezki do wszystkich folderów
# todo wyjścia: folder wynikowy

from pytest import raises

from own.move import run_program

import os.path

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

# zastanów się, jaką rzecz nową chcesz dodać do programu
# (np. kopiowanie plików)
# napisz test pod to:
#   - (test) stwórz pusty folder
#   - (test) wsadź tam jakiś plik
#   - (test) stwórz drugi pusty folder
#   - (test) odpal program, podając oba foldery jako parametry
#   - (test) move_file(): 'swoja logika'
#   - (test) przejdź tylko wtedy jak w tym drugim katalogu jest plik o takiej
#            nazwie i takiej treści
# napisz implementację:
#   - skopiuj plik, os.path.copy()

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
