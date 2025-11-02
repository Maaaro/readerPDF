import shutil

def copy_found_invoices_to_target_dir(files_to_move: dict[str, str]) -> None:
    for key, value in files_to_move.items():
        shutil.copy2(key, value)
