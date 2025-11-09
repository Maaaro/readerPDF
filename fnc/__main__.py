import shutil

from fnc.case import read_input_cases
from fnc.domain import which_files_to_move, InvoiceSearchMode
from fnc.view.values import SearchRequest, LimitedSearch
from fnc.view.view import View


def zostalem_powiadomiony(request: SearchRequest):
    print("----")
    print("Jestem kodem z maina, ktory dostal info z widoku, a widok dostał info z gui")
    print("Sciezka: " + request.invoice_folder)
    print("Docelowy: " + request.target_folder)
    print("Ścieżka excela: " + request.excel_path)
    print("Syrcz mołd: " + str(request.limited_search))

    list_of_cases = read_input_cases(request.excel_path)
    if request.limited_search == LimitedSearch.LIMITED:
        mold = InvoiceSearchMode.BY_WORKFLOW_NUMBER
    else:
        mold = InvoiceSearchMode.FULL

    x = which_files_to_move(list_of_cases, mold, request.invoice_folder, request.target_folder)
    copy_found_invoices_to_target_dir(x)
    z = open_comments("comments.txt")

    print(x)
    print(z)

def open_comments(filename: str) -> list[str]:
    with open(filename, "r") as f:
        list_of_comments = [line.strip("\n") for line in f]

    return list_of_comments
if __name__ == '__main__':
    view = View(zostalem_powiadomiony)
    view.show_window()


def copy_found_invoices_to_target_dir(files_to_move: dict[str, str]) -> None:
    for key, value in files_to_move.items():
        shutil.copy2(key, value)
