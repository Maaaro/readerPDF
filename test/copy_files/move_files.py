import shutil

def copy_found_invoices_to_target_dir(files_to_move: dict[str, str]) -> None:
    for key, values in files_to_move.items():
        for value in values:
            shutil.copy2(key, value)
