from typing import Callable

from fnc.view.gui import GraphicalUserInterface
from fnc.view.values import SearchRequest

class View:
    def __init__(self, perform_search: Callable[[SearchRequest], None]):
        self.__gui = GraphicalUserInterface(self)
        self.__perform_search = perform_search

    def show_window(self):
        self.__gui.show_window()

    def proceed(self):
        message = ""
        if self.__gui.excel_filename() == "":
            message += "Nie wskazano wejściowego arkusza kalkulacyjnego.\n"
        if self.__gui.invoice_directory() == "":
            message += "Nie wskazano katalogu z fakturami / wyciągami bankowymi." + "\n"
        if self.__gui.target_directory() == "":
            message += "Nie wskazano katalogu docelowego." + "\n"
        if message != '':
            self.__gui.display_error(message)
            return

        self.__perform_search(SearchRequest(
            self.__gui.limited_search(),
            self.__gui.invoice_directory(),
            self.__gui.target_directory(),
            self.__gui.excel_filename()
        ))
