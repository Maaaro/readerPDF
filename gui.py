import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
from typing import Callable

# from converter import feet_to_meters, ConversionError, meter_to_feet

root = Tk()
root.title("FileMatch")
def p(left, up, right, bottom):
    return f"{left} {up} {right} {bottom}"

frame = ttk.Frame(root, padding=p(40, 10, 80, 150))
frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

source_wf = tkinter.StringVar(value="Wklej lokalizację pliku z fakturami z WF:  ")
source_entry_wf = ttk.Entry(frame, width=50, textvariable=source_wf)
source_entry_wf.grid(column=3, row=1, sticky=(W, E))

source_wb = tkinter.StringVar(value="Wklej lokalizację folderu z WB:  ")
source_entry_wb = ttk.Entry(frame, width=50, textvariable=source_wb)
source_entry_wb.grid(column=3, row=2, sticky=(W, E))

source_excel = tkinter.StringVar(value="Wklej lokalizację pliku excel:  ")
source_entry_excel = ttk.Entry(frame, width=50, textvariable=source_excel)
source_entry_excel.grid(column=3, row=3, sticky=(W, E))

direction = tkinter.StringVar(value="Wskaż folder do zapisu:  ")
direction_entry = ttk.Entry(frame, width=50, textvariable=source_excel)
direction_entry.grid(column=3, row=4, sticky=(W, E))

ttk.Label(frame, text="Lokalizacja FV z WF:  ").grid(column=1, row=1, sticky=W)
ttk.Label(frame, text="Lokalizacja WB:  ").grid(column=1, row=2, sticky=W)
ttk.Label(frame, text="Lokalizacja pliku excel z numerem spraw i fv do znalezienia:  ").grid(column=1, row=3, sticky=W)
ttk.Label(frame, text="Folder, do którego mają zostać skopiowane pliki:  ").grid(column=1, row=4, sticky=W)

button = ttk.Button(root, text="TEST",  command=lambda : showinfo(title="Wynik", message=source_wf))
button.grid(column=3, row=5, sticky=W)


exit_button = ttk.Button(root, text="Wyjdź", command=lambda : root.quit())
exit_button.grid(column=3, row=6, sticky=W)
root.mainloop()

