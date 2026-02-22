import os


def is_there_any_pdf_files(path: str) -> bool:
    for root, subFolders, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".pdf"):
                return True
    return False


def directory_files(path: str) -> list[str]:
    files = []
    for root, subFolders, filenames in os.walk(path):
        for file in filenames:
            if file.endswith(".pdf"):
                rel_path = os.path.relpath(os.path.join(root, file), path)
                rel_path = rel_path.replace("\\", "/")
                files.append(rel_path)
    return files


def directory_file(path: str, root: str, file: str) -> str:
    if has_subfolder(path, root):
        return subfolder(path, root) + "/" + file
    return file


def subfolder(path: str, root: str) -> str:
    path = path.rstrip("\\/")
    return root.removeprefix(path).lstrip("\\/").replace("\\", "/")


def has_subfolder(path: str, root: str) -> bool:
    return path != root


def is_dir_empty(path: str) -> bool:
    return len(os.listdir(path)) == 0
