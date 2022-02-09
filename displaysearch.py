import re
import tkinter as tk
from tkinter import ttk
import drawfontPIL
import config

class SearchGroup(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.display()

    def display(self):
        # upFrame
        upFrame = ttk.Frame(master=self)
        upFrame.pack(anchor='center')

        self.searchText = tk.StringVar()
        searchEntry = ttk.Entry(master=upFrame, textvariable=self.searchText, width=30)
        searchEntry.pack(side='left', pady=(15,5), padx=(0,15), anchor='e')
        self.searchtBtn = ttk.Button(master=upFrame, text='Search', command=self.search)
        self.searchtBtn.pack(side='right', pady=(15,5), padx=(15,0), anchor='w')

        self.fontFrame = ttk.Frame(master=self)

    def create_search_display(self, size=25, text='這是示例文字', width=550, maxsearch=15):
        self.fontFrame = ttk.Frame(master=self)
        self.fontFrame.pack(side='top', padx=5, pady=2, fill='both', anchor='w')
        for fontname in self.matchList[:maxsearch]:
            fontProperty = self.fontTable[fontname]
            fontLabel = drawfontPIL.DrawFontPIL(master=self.fontFrame, # 实例化
                                                font=fontname,
                                                text=text,
                                                size=size,
                                                path=fontProperty['Path'], 
                                                isInstalled=fontProperty['IsInstalled'],
                                                tag=fontProperty['Tag'],
                                                maxwidth=width)
        if len(self.matchList)>maxsearch:
            tmp = ttk.Label(master=self.fontFrame, 
                            text='There is more... A total of {} matches were found'.format(len(self.matchList)), 
                            anchor='center')
            tmp.pack(pady=(5,2), fill='x', anchor='center')

    def destroy_search_display(self):
        self.fontFrame.destroy()

    def search(self, tags=None):
        def match(pattern, text):
            judge = True
            for i in pattern:
                judge = judge and (i in text)
            return judge

        self.destroy_search_display()
        self.matchList = []
        if self.searchText.get()!='':
            sTextList = re.split(' +', self.searchText.get())
            sTextList = list(map(str.lower, sTextList))
            for k in self.fontTable.keys():
                if match(sTextList, k.lower())==True:
                    self.matchList.append(k)
            self.matchList.sort()
        self.create_search_display(size=int(config.fontsize*1.25),
                                   text=config.fonttext,
                                   maxsearch=config.maxsearch)
        
    def import_fontTable(self, fontTable):
        self.fontTable = fontTable