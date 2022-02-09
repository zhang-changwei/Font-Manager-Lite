import tkinter as tk
from tkinter import ttk
import displayfont
import displaysearch
import displaydup
import config

class NoteGroup(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master

        # fontGroup
        self.fontGroup = displayfont.FontGroup(master=self, 
                                               text=config.fonttext, 
                                               size=config.fontsize,
                                               pagesize=config.fontperpage)
        self.fontGroup.config(relief='sunken', border=2)
        self.fontGroup.pack(side='left', fill='y')

        self.add(child=self.fontGroup, text='  Main  ', padding=0)

        # searchFroup
        self.searchGroup = displaysearch.SearchGroup(master=self)
        self.searchGroup.config(relief='sunken', border=2)
        self.searchGroup.pack(side='left', fill='y')

        self.add(child=self.searchGroup, text='  Search  ', padding=0)

        # dupGroup
        self.dupGroup = displaydup.DupGroup(master=self)
        self.dupGroup.config(relief='sunken', border=2)
        self.dupGroup.pack(side='left', fill='y')

        self.add(child=self.dupGroup, text='  Dupe  ', padding=0)

        self.select(0)
