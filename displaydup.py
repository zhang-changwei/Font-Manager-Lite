import tkinter as tk
from tkinter import ttk

class DupGroup(ttk.Frame):
    '''
    property: dupTable, dupTableinPage, pageNum
    '''

    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.display()
    
    def display(self):
        # top label
        upFrame = ttk.Label(master=self, text='Select the path you want to preserve. The other(s) will be removed.', anchor='center')
        upFrame.pack(pady=(5,2), fill='x', anchor='center')

        # bottom buttons
        downFrame = ttk.Frame(master=self)
        downFrame.pack(side='bottom', padx=5, pady=(2,5), anchor='w')

        self.okBtn = ttk.Button(master=downFrame, text='Confirm', state='disabled')
        self.okBtn.pack(side='left', padx=(5,5), pady=2, anchor='w')

        self.pageVar = tk.IntVar(value=1)
        pageLabel = ttk.Label(master=downFrame, text='Jump To Page', anchor='w')
        self.pageBox = ttk.Combobox(master=downFrame, textvariable=self.pageVar, state='readonly')
        pageLabel.pack(side='left', padx=(0,5), pady=2, anchor='w')
        self.pageBox.pack(side='left', padx=(0,5), pady=2, anchor='w')

        self.pageBox.bind("<<ComboboxSelected>>", self.__pagebox_sel)

    def create_display(self, page=0):
        self.midFrame = ttk.Frame(master=self)
        self.midFrame.pack(fill='x', anchor='w')

        self.dupVars = []
        dupT = self.dupTableinPage[page]
        for ftname, paths in dupT.items():
            tmp = lambda i: {True:'installed', False:'uninstalled'}[i]

            fr = ttk.Labelframe(master=self.midFrame, text=ftname)
            fr.pack(side='top', padx=5, pady=2, fill='x', anchor='w')

            var = tk.StringVar(value='Both')
            bothBtn = ttk.Radiobutton(master=fr, text='Both', variable=var, value='Both')
            bothBtn.grid(row=0, column=0, padx=(5,5), pady=2, sticky='w')
            for i, path in enumerate(paths):
                btn = ttk.Radiobutton(master=fr, text=path['Path'], variable=var, value=path['Path'])
                btn.grid(row=i, column=1, padx=(0,10), pady=2, sticky='w')
                ttk.Label(master=fr, text=tmp(path['IsInstalled'])).grid(row=i, column=2, pady=2, sticky='w')

            self.dupVars.append([ftname, var])

    def destroy_display(self):
        self.midFrame.destroy()

    def create_pages(self, dupTable={}, pageSize=5):
        def iterdup(dupTable):
            tmp = {}
            i = 1
            for k,v in dupTable.items():
                tmp[k] = v
                if i%pageSize==0:
                    yield tmp
                    tmp = {}
                i += 1
            if tmp!={}: yield tmp

        self.dupTable = dupTable
        self.dupTableinPage = []
        for i in iterdup(dupTable):
            self.dupTableinPage.append(i)
        if self.dupTableinPage==[]: self.dupTableinPage = [{}]

        self.pageNum = len(self.dupTableinPage)
        if self.pageNum==0: self.pageNum = 1
        self.pageBox.config(values=tuple(range(1, self.pageNum+1)))

    # pageBox
    def __pagebox_sel(self, event):
        self.destroy_display()
        self.create_display(self.pageVar.get() - 1)