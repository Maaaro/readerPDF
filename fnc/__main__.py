from fnc.gui import show_window
from fnc.ui import SearchRequest

def zostalem_powiadomiony(request: SearchRequest):
    print("----")
    print("Jestem kodem z maina, ktory dostal info z gui")
    print("Sciezka: " + request.invoice_folder)
    print("Docelowy: " + request.target_folder)
    print("Ścieżka excela: " + request.excel_path)
    print("Syrcz mołd: " + str(request.search_mode))

if __name__ == '__main__':
    show_window(zostalem_powiadomiony)
