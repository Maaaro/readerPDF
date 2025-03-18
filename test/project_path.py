from pathlib import Path

def project_path(path: str):
    absolute_path = str(Path(__file__).parent / path)
    return absolute_path.replace("\\", "/")
