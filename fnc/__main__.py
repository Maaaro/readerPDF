from fnc.view.values import SearchRequest
from fnc.view.view import View

def zostalem_powiadomiony(request: SearchRequest):
    print("----")
    print("Jestem kodem z maina, ktory dostal info z widoku, a widok dostał info z gui")
    print("Sciezka: " + request.invoice_folder)
    print("Docelowy: " + request.target_folder)
    print("Ścieżka excela: " + request.excel_path)
    print("Syrcz mołd: " + str(request.limited_search))

if __name__ == '__main__':
    view = View(zostalem_powiadomiony)
    view.show_window()
