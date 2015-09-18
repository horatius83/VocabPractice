from tkinter import *
from tkinter import ttk

def Ui():
    root = Tk()
    root.title("Test")

    mainframe = ttk.Frame(root,padding="3 3 12 12")
    mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
    mainframe.columnconfigure(0,weight=1)
    mainframe.rowconfigure(0,weight=1)
    ttk.Label(mainframe,text="This is a label").grid(column=2,row=2, sticky=(W,E))
    ttk.Button(mainframe,text="This is a button").grid(column=2,row=3, sticky=(S))

    root.mainloop()
