from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

class MenuGroup(tk.Menu):
    def __init__(self, master=None):
        def version():
            messagebox.showinfo('Version', 'Current Version: v0.0.1')
        def about():
            messagebox.showinfo('About', 'Version: v0.0.1\nAuthor: chaaaaang\nCopyright (c): MIT License')

        super().__init__(master, tearoff=False)
        master.config(menu=self)

        self.fileMenu = tk.Menu(master=self, tearoff=False)
        self.optionMenu = tk.Menu(master=self, tearoff=False)
        self.helpMenu = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label='File', menu=self.fileMenu)
        self.add_cascade(label='Option', menu=self.optionMenu)
        self.add_cascade(label='Help', menu=self.helpMenu)
        self.root = master

        self.helpMenu.add_command(label='Version', command=version)
        self.helpMenu.add_command(label='About', command=about)
