from fnc.case import read_input_cases
from fnc.domain import which_files_to_move, InvoiceSearchMode

from fnc.view.values import SearchRequest, LimitedSearch
from fnc.view.view import View
from test.copy_files.move_files import copy_found_invoices_to_target_dir


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
    y = copy_found_invoices_to_target_dir(x)

    print(x)
    print(y)


if __name__ == '__main__':
    view = View(zostalem_powiadomiony)
    view.show_window()
