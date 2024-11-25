import threading
import tkinter as tk
import time
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from own.find_invoices import find_invoice, pdf_files
from own.get_data_from_excel import invoice_numbers, new_filenames, add_comment, list_of_WF_case
from own.copy_pdf import copy_pdf_file


def move_files(invoice_folder: str, output_dir: str, excelpath: str, fileprefix: str):
    if invoice_folder == "" or output_dir == "" or excelpath == "" or fileprefix == "":
        return gui_meseges(0)
    else:
        list_of_invoices = get_invoices(excelpath)
        list_of_newfilenames = get_new_filenames(excelpath, fileprefix)
        wf_cases = get_wf_cases(excelpath)

        files_exist_in_sourcepath = pdf_files(invoice_folder)
        if len(files_exist_in_sourcepath) == 0:
            gui_meseges(6)

        error_comment_invoice_list = ["malformed pdf file", "empty invoice number", "no file found"]
        index = 0
        #popup, progress, progress_step, progress_var = show_progressbar(len(list_of_invoices))

        progress_window = tk.Toplevel(frame)
        progress_window.title("Postęp")
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="determinate")
        progress_bar.pack(pady=20)
        progress_bar["maximum"] = len(list_of_invoices)

        # Wyśrodkuj okno Toplevel względem root
        root_x = frame.winfo_x()
        root_y = frame.winfo_y()
        root_width = frame.winfo_width()
        root_height = frame.winfo_height()
        progress_window.geometry(f"+{root_x + root_width // 2 - 150}+{root_y + root_height // 2 - 50}")


        status_invoice_list = []
        for (invoice, newfilename, wf_number) in zip(list_of_invoices, list_of_newfilenames, wf_cases):

            if fileprefix == "_fv.pdf":
                if wf_number == "empty":
                    status_invoice_list.append("no WF number")
                    continue
                else:
                    newpath = invoice_folder + '/' + str(wf_number) + '/'
                    invoice_found = find_invoice(newpath, str(invoice))
            else:
                invoice_found = find_invoice(invoice_folder, str(invoice))
            items_invoice_found = len(invoice_found)
            if items_invoice_found == 0 or 'no file found' in invoice_found:
                status_invoice_list.append("no file found")
                continue
            else:
                status_multiple_invoice_list = ""
                for i, match in enumerate(invoice_found):
                    if match in error_comment_invoice_list:
                        status_multiple_invoice_list = match
                    else:

                        if i == 0:
                            status_multiple_invoice_list = "OK"
                            copy_pdf_file(invoice_folder, match, output_dir, newfilename)
                        else:
                            newfilename_with_number = newfilename.replace('.pdf', "")
                            newfilename_with_number = newfilename_with_number + str(i) + '.pdf'
                            copy_pdf_file(invoice_folder, match, output_dir, newfilename_with_number)
                status_invoice_list.append(status_multiple_invoice_list)

            #threading.Timer(0.1, update_progressbar, args=(popup, progress, progress_step, progress_var)).start()
            #update_progressbar(popup, progress, progress_step, progress_var)
            #gui.root.after(100,update_progressbar, popup, progress, progress_step, progress_var)
            #gui.root.after(100, gui.root.update_progressbar, popup, progress, progress_step, progress_var)
            progress_window.update()
            time.sleep(0.1)
            progress_bar["value"] += 1



            index = index + 1

        add_comment(excelpath, "Sheet1", status_invoice_list, fileprefix)
        #destroy_progressbar(popup)
        progress_window.destroy()
        #gui.root.after(100, gui.root.destroy_progressbar, popup)
        if "ok" in status_invoice_list:
            gui_meseges(1)
        else:
            gui_meseges(5)


def gui_meseges(message: int):
    if message == 0:
        messagebox.showwarning(title="KOMUNIKAT",
                               message="Należy wypełnić wszystkie pola aby program działał poprawnie.")
    elif message == 1:
        messagebox.showinfo(title="KOMUNIKAT",
                            message="Przeniesiono.")
    elif message == 2:
        messagebox.showwarning(title="KOMUNIKAT",
                               message="Nie udało się pobrać listy z nazwami spraw w WF.")
    elif message == 3:
        messagebox.showwarning(title="KOMUNIKAT",
                               message="Nie udało się pobrać listy z nazwami plików.")
    elif message == 4:
        messagebox.showwarning(title="KOMUNIKAT",
                               message="Nie udało się pobrać listy fv.")
    elif message == 5:
        messagebox.showwarning(title="KOMUNIKAT",
                               message="Nie znaleziono żadnej fv.")
    elif message == 6:
        messagebox.showwarning(title="KOMUNIKAT",
                               message="Folder źródłowy jest pusty.")



def destroy_progressbar(popup):
    popup.destroy()


def update_progressbar(popup, progress: int, progress_step: int, progress_var: DoubleVar):
    popup.update()
    progress += progress_step
    progress_var.set(progress)
    root.update_idletasks()


def show_progressbar(list_of_invoices: int):
    popup = tk.Toplevel()
    popup.title("Progress bar")
    progress = 0
    ttk.Label(popup, text="          Wyszukiwanie    ").grid(row=0, column=0)
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=list_of_invoices)
    progress_bar.grid(row=1, column=0)
    popup.pack_slaves()
    progress_step = int(1)

    return popup, progress, progress_step, progress_var


def get_wf_cases(excelpath: str):
    try:
        wf_cases = list_of_WF_case(excelpath, "Sheet1", "WF")
    except:
        return gui_meseges(2)
    return wf_cases


def get_new_filenames(excelpath: str, fileprefix: str):
    try:
        list_of_newfilenames = new_filenames(excelpath, "Sheet1", "Lp", fileprefix)
    except:
        return gui_meseges(3)

    return list_of_newfilenames


def get_invoices(excelpath: str):
    try:
        list_of_invoices = invoice_numbers(excelpath, "Sheet1",
                                           "Nr fv")
    except:
        return gui_meseges(4)

    return list_of_invoices


def gui():
    global root, frame
    root = Tk()
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
            "   - 'WF' - numer sprawy w WorkFlow - do ograniczenia wyszukiwania (dotyczy tylko fv). Jeśli to pole będzie puste to program pominie tą pozycję.\n")
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

    ttk.Button(frame, text="Podaj folder z fakturami / WB", command=lambda: file_to_search("Invoices")).grid(
        column=2, row=2, sticky="W", padx=5, pady=5)
    ttk.Button(frame, text="Podaj folder docelowy", command=lambda: file_to_search("Output")).grid(
        column=2, row=3, sticky="W", padx=5, pady=5)
    ttk.Button(frame, text="Podaj plik Ecxel", command=lambda: file_to_search("Excel")).grid(column=2, row=4,
                                                                                             sticky="W",
                                                                                             padx=5, pady=5)
    ttk.Button(frame, text="Przenieś",
               command=lambda: selected_radiobutton()).grid(column=2, row=7, sticky="NS", padx=10, pady=10)
    ttk.Button(frame, text="Zamknij program", command=root.destroy).grid(column=3, row=7, sticky="W", padx=10, pady=10)

    document_type = StringVar()
    ttk.Radiobutton(frame, text="Szukaj faktur", variable=document_type, value="Invoice").grid(column=2, row=1,
                                                                                               sticky="NSEW", padx=10,
                                                                                               pady=10)
    ttk.Radiobutton(frame, text="Szukaj wyciągów bankowych", variable=document_type, value="WB").grid(column=3, row=1,
                                                                                                      sticky="W",
                                                                                                      padx=10, pady=10)

    def selected_radiobutton():
        if document_type.get() == "Invoice" or document_type.get() == "WB":
            if document_type.get() == "Invoice":
                move_files(invoices_folder.get(), output_dir.get() + "/", excelpath.get(), "_fv.pdf")

            elif document_type.get() == "WB":
                move_files(invoices_folder.get(), output_dir.get() + "/", excelpath.get(), "_wb.pdf")
        else:
            messagebox.showinfo(title="Uwaga", message="Wybierz 'Szukaj faktur' lub 'wyciągów bankowych'")

    def file_to_search(option: str):
        tk.Tk().withdraw()

        if option == "Invoices" or option == "Output":
            folder_path_string = filedialog.askdirectory()
            if folder_path_string:
                path = str((folder_path_string))
                set_path_into_field(option, path)
            else:
                messagebox.showinfo(title="Uwaga", message="Nie wskazano ściezki folderu")
        elif option == "Excel":
            folder_path_string = filedialog.askopenfilename()
            if folder_path_string:
                path = str((folder_path_string))
                set_path_into_field(option, path)
            else:
                messagebox.showinfo(title="Uwaga", message="Nie wskazano ścieżki pliku")
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

