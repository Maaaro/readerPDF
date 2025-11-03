import os
import shutil


def copy_found_invoices_to_target_dir(files_to_move: dict[str, str]) -> None:
    for key, value in files_to_move.items():
        shutil.copy2(key, value)


def create_file(my_file_path: str, text_of_my_file: str) -> None:
    os.makedirs(os.path.dirname(my_file_path), exist_ok=True)
    with open(my_file_path, "w") as file:
        file.write(text_of_my_file)

def check_if_file_exist(my_file_exist: str) -> bool:
    if os.path.exists(my_file_exist):
        return True
    return False

def delete_if_exist(my_file_delete: str):
    if os.path.exists(my_file_delete):
        os.remove(my_file_delete)

def test_copy_one_file() -> None:
    filename = "test.txt"
    input_dir = "test/copy_files/input_dir"
    output_dir = "test/copy_files/output_dir"
    text = "foo"

    my_file_in_input_dir = os.path.join(input_dir, filename)
    my_file_in_output_dir = os.path.join(output_dir, filename)
    delete_if_exist(my_file_in_input_dir)
    delete_if_exist(my_file_in_output_dir)

    create_file(my_file_in_input_dir, text)
    copy_found_invoices_to_target_dir({my_file_in_input_dir: output_dir})
    result = check_if_file_exist(my_file_in_input_dir)
    assert result == True

def test_copy_two_file() -> None:
    filename1 = "test1.txt"
    filename2 = "test2.txt"
    input_dir = "test/copy_files/input_dir"
    output_dir = "test/copy_files/output_dir"
    text1 = "foo"
    text2 = "boo"
    my_file1 = os.path.join(input_dir, filename1)
    my_file2 = os.path.join(input_dir, filename2)
    delete_if_exist(my_file1)
    delete_if_exist(my_file2)
    create_file(my_file1, text1)
    create_file(my_file2, text2)
    copy_found_invoices_to_target_dir({my_file1: output_dir, my_file2: output_dir })
    result1 = check_if_file_exist(my_file1)
    result2 = check_if_file_exist(my_file2)
    assert result1 == True and result2 == True