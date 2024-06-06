import os
import tkinter
from tkinter import *
from tkinter import ttk, messagebox, filedialog

from own.invoice import find_invoice
from own.invoice_id import invoice_numbers, new_filenames, add_comment, list_of_WF_case
from own.move import run_program


def move_files(invoice_folder: str, output_dir: str, excelpath: str, fileprefix: str):
    if invoice_folder == "" or output_dir == "" or excelpath == "" or fileprefix == "":
        messagebox.showinfo(title="KOMUNIKAT",
                            message="Należy wypełnić wszystkie pola aby program działał poprawnie")
    else:
        try:
            list_of_invoices = invoice_numbers(excelpath, "Sheet1",
                                               "Nr fv")
        except:
            messagebox.showinfo(title="KOMUNIKAT",
                                message="Nie udało się pobrać listy fv")

        try:
            list_of_newfilenames = new_filenames(excelpath, "Sheet1", "Lp", fileprefix)
        except:
            messagebox.showinfo(title="KOMUNIKAT",
                                message="Nie udało się pobrać listy z nazwami plików")

        try:
            wf_cases = list_of_WF_case(excelpath, "Sheet1", "WF")
            # wf_cases = [x for x in wf_cases_with_nan if x==x]
        except:
            messagebox.showinfo(title="KOMUNIKAT",
                                message="Nie udało się pobrać listy z nazwami spraw w WF")

        comment_invoice_list = ["malformed pdf file", "empty invoice number", "no file found"]
        index = 0

        popup = tkinter.Toplevel()
        popup.title("Progress bar")
        progress = 0
        ttk.Label(popup, text="          Wyszukiwanie    ").grid(row=0, column=0)
        progress_var = tkinter.DoubleVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=len(list_of_invoices))
        progress_bar.grid(row=1, column=0)
        popup.pack_slaves()
        progress_step = int(1)
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
                    if match in comment_invoice_list:
                        status_multiple_invoice_list= match
                    else:

                        if i == 0:
                            status_multiple_invoice_list = "OK"
                            run_program(invoice_folder, match, output_dir, newfilename)
                        else:
                            # newnewfilename = newfilename.replace('.pdf', str(i) + '.pdf')
                            newnewfilename = newfilename.replace('.pdf', "")
                            newnewfilename = newnewfilename + str(i) + '.pdf'
                            run_program(invoice_folder, match, output_dir, newnewfilename)
                status_invoice_list.append(status_multiple_invoice_list)
            popup.update()
            progress += progress_step
            progress_var.set(progress)

            index = index + 1

        add_comment(excelpath, "Sheet1", status_invoice_list, fileprefix)
        popup.destroy()
        messagebox.showinfo(title="KOMUNIKAT",
                            message="Przeniesiono")

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
    ttk.Radiobutton(frame, text="Szukaj wyciągów bankowych", variable=document_type, value="WB").grid(column=4, row=1)

    def selected_radiobutton():
        if document_type.get() == "Invoice" or document_type.get() == "WB":
            if document_type.get() == "Invoice":
                move_files(invoices_folder.get(), output_dir.get() + "/", excelpath.get(), "_fv.pdf")

            elif document_type.get() == "WB":
                move_files(invoices_folder.get(), output_dir.get() + "/", excelpath.get(), "_wb.pdf")
        else:
            messagebox.showinfo(title="Uwaga", message="Wybierz 'Szukaj faktur' lub 'wyciągów bankowych'")

    def switch_methode_of_filedialog(option: str):
        tkinter.Tk().withdraw()

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

gui()
