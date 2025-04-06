import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable

from fnc.ui import SearchMode, SearchRequest

def show_window(powiadamiacz: Callable[[SearchRequest], None]):
    Window(powiadamiacz).mainloop()

class Window(tk.Tk):
    def __init__(self, powiadamiacz: Callable[[SearchRequest], None]):
        super().__init__()
        self.powiadamiacz = powiadamiacz
        self.title("Program do przenoszenia faktur i wyciągów bankowych")
        self.geometry("800x325")
        self.minsize(800, 325)
        self.layout = Layout(self, powiadamiacz)

class Layout(ttk.Frame):
    def __init__(self, parent, powiadamiacz: Callable[[SearchRequest], None]):
        super().__init__(parent)
        self.powiadamiacz = powiadamiacz
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.create_widgets()
        self.create_layout()

    def create_layout(self):
        self.create_grid()
        self.place_widgets()

    def create_widgets(self):
        text = (
                "\nPlik Excel, z którego mają zostać pobrane dane musi zawierać zakładkę 'Sheet1', która zawiera kolumny: \n" +
                "   - 'Lp' - na podstawie, której przypisze nową nazwę, \n" +
                "   - 'Nr fv' - numer faktury, który ma zostać znaleziony, \n" +
                "   - 'WF' - numer sprawy w WorkFlow - do ograniczenia wyszukiwania (dotyczy tylko fv).")

        self.invoices_folder = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.excelpath = tk.StringVar()
        self.document_type = tk.StringVar()
        self.search_option = tk.StringVar()
        self.search_option.set("Full search")

        self.instruction = ttk.Label(self, text=text)

        self.search_option_status = ttk.Checkbutton(self, text="Ogranicz wyszukiwanie", variable=self.search_option,
                                                    onvalue="Limited search", offvalue="Full search")

        self.invoices_folder_entry = ttk.Entry(self, textvariable=self.invoices_folder)
        self.output_dir_entry = ttk.Entry(self, textvariable=self.output_dir)
        self.excelpath_entry = ttk.Entry(self, textvariable=self.excelpath)

        self.invoice_dir_input_button = ttk.Button(self, text="Podaj folder z fakturami / WB",
                                                   command=lambda: self.search_for_directory("INVOICE_DIR"))
        self.invoice_output_dir_button = ttk.Button(self, text="Podaj folder docelowy",
                                                    command=lambda: self.search_for_directory("OUTPUT_DIR"))
        self.excel_filename_button = ttk.Button(self, text="Podaj plik Ecxel",
                                                command=lambda: self.search_for_directory("EXCEL_DIR"))
        self.initiate_program_button = ttk.Button(self, text="Przenieś", command=self.click)

    def create_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0, minsize=100)
        self.columnconfigure(2, weight=0, minsize=100)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

    def place_widgets(self):
        self.instruction.grid(column=0, row=0, sticky="W", columnspan=2, padx=5, pady=5)
        self.search_option_status.grid(column=1, row=1, sticky="W", padx=10, pady=10)
        self.invoices_folder_entry.grid(column=0, row=2, sticky="NSEW", padx=5, pady=5)
        self.output_dir_entry.grid(column=0, row=3, sticky="NSEW", padx=5, pady=5)
        self.excelpath_entry.grid(column=0, row=4, sticky="NSEW", padx=5, pady=5)
        self.invoice_dir_input_button.grid(column=1, row=2, sticky="W", padx=5, pady=5)
        self.invoice_output_dir_button.grid(column=1, row=3, sticky="W", padx=5, pady=5)
        self.excel_filename_button.grid(column=1, row=4, sticky="W", padx=5, pady=5)
        self.initiate_program_button.grid(column=2, row=7, sticky="NS", padx=10, pady=10)

    def click(self):
        if self.search_option.get() == 'Full search':
            mode = SearchMode.FULL
        else:
            mode = SearchMode.LIMITED

        empty_field_exist = self.check_empty_values()

        if empty_field_exist == "":
            request = SearchRequest(
                mode,
                self.invoices_folder.get(),
                self.output_dir.get(),
                self.excelpath.get()
            )
            self.powiadamiacz(request)
        else:
            messagebox.showinfo(master=self, title="Uwaga", message=empty_field_exist)

    def check_empty_values(self) -> str:
        message = ""
        if self.invoices_folder.get() == "":
            message = "Nie wskazano folderu z fakturami / wyciągami bankowymi" + "\n"
        if self.output_dir.get() == "":
            message = message + "Nie wskazano ściezki folderu docelowego" + "\n"
        if self.excelpath.get() == "":
            message = message + "Nie wskazano ściezki do pliku excel" + "\n"
        return message

    def search_for_directory(self, option: str):
        if option == "INVOICE_DIR":
            folder_path_string = filedialog.askdirectory()
            if folder_path_string:
                path = str(folder_path_string)
                self.invoices_folder.set(path)
        elif option == "OUTPUT_DIR":
            folder_path_string = filedialog.askdirectory()
            if folder_path_string:
                path = str(folder_path_string)
                self.output_dir.set(path)
        elif option == "EXCEL_DIR":
            folder_path_string = filedialog.askopenfilename()
            if folder_path_string:
                path = str(folder_path_string)
                self.excelpath.set(path)

def old_gui():
    root = tk.Tk()
    root.title("Program do przenoszenia faktur i wyciągów bankowych")
    root.geometry("800x325")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    textframe = ttk.Frame(root, padding=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    textframe.grid(column=0, row=0, sticky="NSEW")

    frame = ttk.Frame(root, padding=15)
    frame.grid(column=0, row=1, sticky="NSEW")
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=1)
    frame.rowconfigure(5, weight=1)
    frame.rowconfigure(6, weight=1)
    frame.rowconfigure(7, weight=1)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)

    text = (
            "\nPlik Excel, z którego mają zostać pobrane dane musi zawierać zakładkę 'Sheet1', która zawiera kolumny: \n" +
            "   - 'Lp' - na podstawie, której przypisze nową nazwę, \n" +
            "   - 'Nr fv' - numer faktury, który ma zostać znaleziony, \n" +
            "   - 'WF' - numer sprawy w WorkFlow - do ograniczenia wyszukiwania (dotyczy tylko fv).")
    ttk.Label(textframe, text=text).grid(column=0, row=0, sticky="NSEW", padx=5, pady=5)

    ttk.Label(frame, text="Folder z fakturami / WB").grid(column=0, row=2, sticky="W", padx=5, pady=5)
    invoices_folder = tk.StringVar()
    invoices_folder_entry = ttk.Entry(frame, textvariable=invoices_folder, state="disable")
    invoices_folder_entry.grid(column=1, row=2, sticky="NSEW", padx=5, pady=5)

    ttk.Label(frame, text="Folder docelowy").grid(column=0, row=3, sticky="W", padx=5, pady=5)
    output_dir = tk.StringVar()
    output_dir_entry = ttk.Entry(frame, textvariable=output_dir, state="disable")
    output_dir_entry.grid(column=1, row=3, sticky="NSEW", padx=5, pady=5)

    ttk.Label(frame, text="Plik Excel z fakturami").grid(column=0, row=4, sticky="W", padx=5, pady=5)
    excelpath = tk.StringVar()
    excelpath_entry = ttk.Entry(frame, textvariable=excelpath, state="disable")
    excelpath_entry.grid(column=1, row=4, sticky="NSEW", padx=5, pady=5)

    # ttk.Button(frame, text="Podaj folder z fakturami / WB", command=lambda: file_to_search("Invoices")).grid(
    #     column=2, row=2, sticky="W", padx=5, pady=5)
    # ttk.Button(frame, text="Podaj folder docelowy", command=lambda: file_to_search("Output")).grid(
    #     column=2, row=3, sticky="W", padx=5, pady=5)
    # ttk.Button(frame, text="Podaj plik Ecxel", command=lambda: file_to_search("Excel")).grid(column=2, row=4,
    #                                                                                          sticky="W",
    #                                                                                          padx=5, pady=5)
    # ttk.Button(frame, text="Przenieś",
    #            command=lambda: selected_radiobutton()).grid(column=2, row=7, sticky="NS", padx=10, pady=10)
    # ttk.Button(frame, text="Zamknij program", command=lambda: exit_program()).grid(column=3, row=7, sticky="W", padx=10,
    #                                                                                pady=10)
    #
    # document_type = StringVar()
    # ttk.Radiobutton(frame, text="Szukaj faktur", variable=document_type, value="Invoice").grid(column=2, row=1,
    #                                                                                            sticky="NSEW", padx=10,
    #                                                                                            pady=10)
    # ttk.Radiobutton(frame, text="Szukaj wyciągów bankowych", variable=document_type, value="WB").grid(column=3, row=1,
    #                                                                                                   sticky="W")

    # def exit_program():
    #     sys.exit("Użytkownik zamknął program.")
    #
    # def selected_radiobutton():
    #     if document_type.get() == "Invoice" or document_type.get() == "WB":
    #         if document_type.get() == "Invoice":
    #             move_files(invoices_folder.get(), output_dir.get() + "/", excelpath.get(), "_fv.pdf")
    #
    #         elif document_type.get() == "WB":
    #             move_files(invoices_folder.get(), output_dir.get() + "/", excelpath.get(), "_wb.pdf")
    #     else:
    #         messagebox.showinfo(title="Uwaga", message="Wybierz 'Szukaj faktur' lub 'wyciągów bankowych'")
    #
    # def file_to_search(option: str):
    #     tk.Tk().withdraw()
    #
    #     if option == "Invoices" or option == "Output":
    #         folder_path_string = filedialog.askdirectory()
    #         if folder_path_string:
    #             path = str(folder_path_string)
    #             set_path_into_field(option, path)
    #         else:
    #             messagebox.showinfo(title="Uwaga", message="Nie wskazano ściezki folderu")
    #     elif option == "Excel":
    #         folder_path_string = filedialog.askopenfilename()
    #         if folder_path_string:
    #             path = str(folder_path_string)
    #             set_path_into_field(option, path)
    #         else:
    #             messagebox.showinfo(title="Uwaga", message="Nie wskazano ścieżki pliku")
    #     else:
    #         messagebox.showinfo(title="Uwaga", message="error")
    #
    # def set_path_into_field(option: str, path: str):
    #     if option == "Invoices":
    #         invoices_folder_entry.config(state="enable")
    #         invoices_folder_entry.delete(0, END)
    #         invoices_folder_entry.insert(0, path)
    #         invoices_folder_entry.config(state="disable")
    #     elif option == "Output":
    #         output_dir_entry.config(state="enable")
    #         output_dir_entry.delete(0, END)
    #         output_dir_entry.insert(0, path)
    #         output_dir_entry.config(state="disable")
    #     else:
    #         excelpath_entry.config(state="enable")
    #         excelpath_entry.delete(0, END)
    #         excelpath_entry.insert(0, path)
    #         excelpath_entry.config(state="disable")
    #         padx = 10, pady = 10)
