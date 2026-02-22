import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable

from fnc.view.values import LimitedSearch


class GraphicalUserInterface:
    def __init__(self, view):
        self.__progressbar_label = None
        self.__progressbar_window = None
        self.__progressbar = None
        self.__view = view
        self.__root = tk.Tk()
        self.__fields = [
            ('Wejściowy arkusz kalkulacyjny:', 'file'),
            ('Katalog z fakturami / WB:', 'directory'),
            ('Katalog wyjściowy:', 'directory'),
        ]
        self.__file_field_vars = []
        self.__search_mode_limited_var = tk.BooleanVar()

    def excel_filename(self) -> str:
        return self.__file_field_vars[0].get()

    def invoice_directory(self) -> str:
        return self.__file_field_vars[1].get()

    def target_directory(self) -> str:
        return self.__file_field_vars[2].get()

    def limited_search(self) -> LimitedSearch:
        if self.__search_mode_limited_var.get():
            return LimitedSearch.LIMITED
        return LimitedSearch.FULL

    def browse_file(self, entry: tk.StringVar, directory: bool) -> None:
        if directory:
            filename = filedialog.askdirectory()
        else:
            filename = filedialog.askopenfilename()
        if filename:
            entry.set(filename)

    def display_error(self, error_message: str) -> None:
        messagebox.showinfo(master=self.__root, title='Uwaga', message=error_message)

    def show_window(self):
        self.__root.title("Program do przenoszenia faktur i wyciągów bankowych")
        self.__root.minsize(500, 385)
        self.__root.geometry("800x425")
        self.__root.grid_columnconfigure(0, weight=1)

        main_frame = ttk.LabelFrame(self.__root, text="Ustawienia początkowe", padding=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        text = 'Wejściowy arkusz musi zawierać zakładkę "Sheet1", która zawiera kolumny: \n' + \
               ' - "Lp" - na podstawie, której przypisze nową nazwę,\n' + \
               ' - "Nr fv" - numer faktury, który ma zostać znaleziony,\n' + \
               ' - "WF" - numer sprawy w WorkFlow - do ograniczenia wyszukiwania (dotyczy tylko fv).'

        top_label = tk.Label(main_frame, justify='left', text=text)
        top_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        row_index = 1
        for i in range(3):
            (label, file_type) = self.__fields[i]
            field_label = ttk.Label(main_frame, text=label)
            field_label.grid(row=row_index, column=0, columnspan=3, sticky="w", pady=(5, 0))
            row_index += 1

            field_var = tk.StringVar()
            field_entry = ttk.Entry(main_frame, textvariable=field_var)
            field_entry.grid(row=row_index, column=0, columnspan=2, sticky="ew", padx=(0, 5), pady=2)
            self.__file_field_vars.append(field_var)

            browse_button = ttk.Button(
                main_frame,
                text="Przeglądaj...",
                command=lambda fe=field_var, t=file_type: self.browse_file(fe, t == 'directory'))
            browse_button.grid(row=row_index, column=2, pady=2)

            row_index += 1

        checkbox = ttk.Checkbutton(main_frame, text="Ogranicz wyszukiwanie", variable=self.__search_mode_limited_var)
        checkbox.grid(row=row_index, column=0, columnspan=3, sticky="w", pady=(10, 10))
        row_index += 1

        proceed_button = ttk.Button(self.__root, text="Przenieś", command=lambda: self.__view.proceed())
        proceed_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

        self.__root.mainloop()

    def show_progressbar_window(self, total: int, on_close: Callable):

        self.__progressbar_window = tk.Toplevel(self.__root)
        self.__progressbar_window.title("Progress...")
        self.__progressbar_window.resizable(False, False)
        self.__progressbar_window.grab_set()
        self.__center_on_main_window(self.__progressbar_window, 400, 100)
        self.__progressbar_window.protocol("WM_DELETE_WINDOW", on_close)

        self.__progressbar_label = ttk.Label(self.__progressbar_window, text=f"0 / {total}")
        self.__progressbar_label.pack(pady=(15, 5))

        self.__progressbar = ttk.Progressbar(
            self.__progressbar_window,
            orient="horizontal",
            length=350,
            mode="determinate",
            maximum=total
        )
        self.__progressbar.pack(pady=5)

    def __center_on_main_window(self, window: tk.Toplevel, width: int, height: int):
        self.__root.update_idletasks()
        x = self.__root.winfo_rootx() + (self.__root.winfo_width() // 2) - (width // 2)
        y = self.__root.winfo_rooty() + (self.__root.winfo_height() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def update_progressbar(self, current: int, total: int):
        self.__progressbar["value"] = current
        self.__progressbar_label.config(text=f"{current} / {total}")
        self.__root.update_idletasks()

    def close_progressbar_window(self):
        self.__progressbar_window.grab_release()
        self.__progressbar_window.destroy()

    def run_on_main_thread(self, func: Callable, *args):
        self.__root.after(0, func, *args)

    def show_message(self, message: str):
        tk.messagebox.showinfo(title="Status", message=message)
