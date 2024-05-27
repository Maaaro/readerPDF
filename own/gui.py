import tkinter
from pathlib import Path
from tkinter import *
from tkinter import ttk, messagebox, filedialog

from own.invoice_id import invoice_numbers, new_filenames


def move_files(invoice_folder: str, output_dir: str, excelpath: str, fileprefix: str):
    # messagebox.showinfo(title="Test",
    #                     message="Invoice folder: " + invoice_folder + "\n Output_dir: " + output_dir + "\n Excelpath: " + excelpath)

    if invoice_folder == "" or output_dir == "" or excelpath == "" or fileprefix == "":
        messagebox.showinfo(title="KOMUNIKAT bla bla bla",
                            message="Należy wypełnić wszystkie pola aby program działał poprawnie")
    else:
        try:
            list_of_invoices = invoice_numbers(
                excelpath, "Sheet1",
                "Nr fv")
        except:
            messagebox.showinfo(title="KOMUNIKAT",
                                message="Nie udało się pobrać listy fv")

        try:
            list_of_newfilenames = new_filenames(
                excelpath, "Sheet1", "Lp")
        except:
            messagebox.showinfo(title="KOMUNIKAT",
                                message="Nie udało się pobrać listy z nazwami plików")

        for (invoice, newfilename) in zip(list_of_invoices, list_of_newfilenames):
            return True
            # find_invoice(invoice_folder, invoice)
            # run_program(r"C:/Users/m.mrowka/OneDrive - Napollo Management sp. z o.o/Pulpit/Test/scripts/", r"C:/Users/m.mrowka/OneDrive - Napollo Management sp. z o.o/Pulpit/Test/Output", newfilename , " fv")

    # invoice_numbers(invoice_folder, "Sheet1", invoice):


def gui():
    root = Tk()
    root.title("Program do przenoszenia faktur i wyciągów bankowych")

    frame = ttk.Frame(root, padding=100)
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(frame, text="Folder z fakturami/WB").grid(column=1, row=3)
    invoices_folder = tkinter.StringVar()
    invoices_folder_entry = ttk.Entry(frame, width=80, textvariable=invoices_folder, state="disable")
    invoices_folder_entry.grid(column=2, row=3)

    ttk.Label(frame, text="Folder docelowy").grid(column=1, row=4)
    output_dir = tkinter.StringVar()
    output_dir_entry = ttk.Entry(frame, width=80, textvariable=output_dir, state="disable")
    output_dir_entry.grid(column=2, row=4)

    ttk.Label(frame, text="Plik excel z fakturami").grid(column=1, row=5)
    excelpath = tkinter.StringVar()
    excelpath_entry = ttk.Entry(frame, width=80, textvariable=excelpath, state="disable")
    excelpath_entry.grid(column=2, row=5)

    ttk.Button(root, text="Podaj folder z fakturami/WB", command=lambda: switch_methode_of_filedialog("Invoices")).grid(
        column=3, row=3, sticky=W)
    ttk.Button(root, text="Podaj folder docelowy", command=lambda: switch_methode_of_filedialog("Output")).grid(
        column=3, row=4, sticky=W)
    ttk.Button(root, text="Podaj plik ecxel", command=lambda: switch_methode_of_filedialog("Excel")).grid(column=3,
                                                                                                          row=5,
                                                                                                          sticky=W)
    ttk.Button(frame, text="Przenieś",
               command=lambda: selected_radiobutton()).grid(column=3, row=7)
    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=4, row=7)

    document_type = StringVar()
    ttk.Radiobutton(frame, text="Szukaj faktur", variable=document_type, value="Invoice").grid(column=3, row=1)
    ttk.Radiobutton(frame, text="Szukaj wyciągów bankowych", variable=document_type , value="WB").grid(column=4, row=1)

    def selected_radiobutton():
        if document_type.get() == "Invoice" or document_type.get() == "WB":
            if document_type.get() == "Invoice":
                fileprefix = ". fv"
            elif document_type.get() == "WB":
                fileprefix = ". wb"
            move_files(invoices_folder.get(), output_dir.get(), excelpath.get(), fileprefix)
        else:
            messagebox.showinfo(title="Uwaga", message="Wybierz 'Szukaj faktur' lub 'wyciągów bankowych'")

    def switch_methode_of_filedialog(option: str):
        tkinter.Tk().withdraw()

        if option == "Invoices" or option == "Output":
            folder_path_string = filedialog.askdirectory()
            if folder_path_string:
                path = str(Path(folder_path_string))
                set_path_into_field(option, path)
            else:
                messagebox.showinfo(title="Uwaga", message="Nie wskazano ściezki folderu")
        elif option == "Excel":
            folder_path_string = filedialog.askopenfilename()
            if folder_path_string:
                path = str(Path(folder_path_string))
                set_path_into_field(option, path)
            else:
                messagebox.showinfo(title="Uwaga", message="NIe wskazano ścieżki pliku")
        else:
            messagebox.showinfo(title="Uwaga", message="error")

    def set_path_into_field(option: str, path: str):
        if option == "Invoices":
            invoices_folder_entry.config(state="enable")
            invoices_folder_entry.delete(0, END)
            invoices_folder_entry.insert(0, path)
            invoices_folder_entry.config(state="disable")
        elif option == "Output":
            output_dir_entry.config(state="enable")
            output_dir_entry.delete(0, END)
            output_dir_entry.insert(0, path)
            output_dir_entry.config(state="disable")
        else:
            excelpath_entry.config(state="enable")
            excelpath_entry.delete(0, END)
            excelpath_entry.insert(0, path)
            excelpath_entry.config(state="disable")

    root.mainloop()


gui()
