import tkinter
from tkinter import *
from tkinter import ttk, messagebox




def move_files(message: str):
    messagebox.showinfo(title="Test", message="WIP")

def gui():
    root = Tk()
    root.title("Program do przenoszenia faktur i wyciągów bankowych")

    frame = ttk.Frame(root, padding=100)
    frame.grid()

    ttk.Label(frame, text="Folder z fakturami").grid(column=1, row=2)
    invoices_folder = tkinter.StringVar()
    invoices_folder_entry = ttk.Entry(frame, width=40, textvariable=invoices_folder)
    invoices_folder_entry.grid(column=2, row=2)

    ttk.Label(frame, text="Folder docelowy").grid(column=1, row=3)
    output_dir = tkinter.StringVar()
    output_dir_entry = ttk.Entry(frame, width=40, textvariable=output_dir)
    output_dir_entry.grid(column=2, row=3)

    ttk.Label(frame, text="Plik excel z fakturami").grid(column=1, row=4)
    excelpath = tkinter.StringVar()
    excelpath_entry = ttk.Entry(frame, width=40, textvariable=excelpath)
    excelpath_entry.grid(column=2, row=4)

    message="WIP"
    ttk.Button(frame, text="Przenieś", command=lambda: move_files(message)).grid(column=3, row=5)

    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=3, row=1)
    root.mainloop()


gui()