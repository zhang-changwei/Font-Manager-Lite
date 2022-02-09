from math import ceil
from tkinter import ttk
import tkinter as tk
import drawfontPIL
import config

class FontGroup(ttk.Frame):
    '''
    property: root, mode(normal,multichoose), 
              fontSize, fontText, fontFrame, fontLabels, fontTable, 
              pageNum页面数量, pageSize, fontnameListinPage, page
    '''

    def __init__(self, master=None, text='這是示例文字', size=20, pagesize=50):
        pass
        super().__init__(master)
        self.root = master # self.root = root window
        # self.pack()
        self.mode = 'normal'
        self.create_display(text=text, size=size, pagesize=pagesize)

    def create_display(self, width=550, text='這是示例文字', size=20, pagesize=50):
        self.fontSize = tk.IntVar(value=size)
        self.fontText = tk.StringVar(value=text)
        self.pageSize = pagesize
        self.pageVar = tk.IntVar(value=1)

        # fontSize, fontText
        upFrame = ttk.Frame(master=self)
        upFrame.grid(row=0, column=0, sticky='ew')

        sizeLabel = ttk.Label(master=upFrame, text='Font Size', anchor='w')
        sizeEntry = ttk.Entry(master=upFrame, textvariable=self.fontSize, width=20)
        textLabel = ttk.Label(master=upFrame, text='Font Text', anchor='w')
        textEntry = ttk.Entry(master=upFrame, textvariable=self.fontText, width=20)
        self.sizetextBtn = ttk.Button(master=upFrame, text='Confirm', command=self.__size_text_click)

        sizeLabel.grid(row=0, column=0, sticky='w', padx=(5,35), pady=(5,2))
        sizeEntry.grid(row=0, column=1, sticky='w', padx=(0,35), ipadx=20, pady=(5,2))
        textLabel.grid(row=1, column=0, sticky='w', padx=(5,35), pady=2)
        textEntry.grid(row=1, column=1, sticky='w', padx=(0,35), ipadx=20, pady=2)
        self.sizetextBtn.grid(row=0, column=2, rowspan=2, sticky='e', ipady=5, pady=(5,2))

        # font grid
        ftFrame = ttk.Frame(master=self)
        ftFrame.grid(row=1, column=0, sticky='news', padx=5, pady=2)
        self.__create_font_canvas_display(master=ftFrame, width=width)

        # multiChoose, page
        downFrame = ttk.Frame(master=self)
        downFrame.grid(row=2, column=0, sticky='ew')

        self.multiChooseBtn = ttk.Button(master=downFrame, text='Multi Select', command=self.__multichoosebtn_click)
        self.cancelMultiChooseBtn = ttk.Button(master=downFrame, text='Cancel Multi Select', command=self.__cancelmultichoosebtn_click)
        # multichoose options
        self.selAllBtn = ttk.Button(master=downFrame, text='Select All', width=9, command=self.__selall_click)
        self.cancelSelAllBtn = ttk.Button(master=downFrame, text='Cancel Select All', command=self.__cancelselall_click)
        self.setTagBtn = ttk.Button(master=downFrame, text='Set Tag', width=9)
        self.addTagBtn = ttk.Button(master=downFrame, text='Add Tag', width=9)
        self.delTagBtn = ttk.Button(master=downFrame, text='Del Tag', width=9)
        self.installBtn = ttk.Button(master=downFrame, text='Install', width=9, state='disabled')
        self.uninstallBtn = ttk.Button(master=downFrame, text='Uninstall', width=9, state='disabled')
        self.delfromsysBtn = ttk.Button(master=downFrame, text='Delete from System', state='disabled')
        # page
        pageLabel = ttk.Label(master=downFrame, text='Jump To Page', anchor='w')
        self.pageBox = ttk.Combobox(master=downFrame, textvariable=self.pageVar, state='readonly')
        
        self.multiChooseBtn.grid(row=0, column=0, sticky='w', padx=(5,5), pady=2)
        pageLabel.grid(row=1, column=0, sticky='w', padx=(5,5), pady=(2,8))
        self.pageBox.grid(row=1, column=1, columnspan=2,sticky='w', padx=(0,5), pady=(0,3))

        self.pageBox.bind("<<ComboboxSelected>>", self.__pagebox_sel)

    def __create_font_canvas_display(self, master=None, width=550, height=500):
        def wheel_y(event):
            a= int(-(event.delta)/60)
            self.canvas.yview_scroll(a,'units')

        def wheel_x(event):
            a= int(-(event.delta)/60)
            self.canvas.xview_scroll(a,'units')

        self.canvas=tk.Canvas(master, width=width, height=height, scrollregion=(0,0,1.5*width,2000)) #创建canvas

        self.fontFrame=ttk.Frame(self.canvas) #把frame放在canvas里
        self.fontFrame.pack(side='left', fill='both')

        vbar=ttk.Scrollbar(master,orient='vertical')
        vbar.grid(row=0, column=1, sticky='ns')
        vbar.configure(command=self.canvas.yview)
        hbar=ttk.Scrollbar(master,orient='horizontal')
        hbar.grid(row=1, column=0, sticky='ew')
        hbar.configure(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=vbar.set)
        self.canvas.config(xscrollcommand=hbar.set)
        self.canvas.create_window(0,0, window=self.fontFrame, anchor='nw')  #create_window
        self.canvas.grid(row=0, column=0, sticky='news')

        self.canvas.bind('<MouseWheel>', wheel_y)
        self.canvas.bind('<Shift-MouseWheel>', wheel_x)

    def create_font_display(self, page=0):
        self.page = page
        config.fontsize = self.fontSize.get()
        config.fonttext = self.fontText.get()
        for n,fontname in enumerate(self.fontnameListinPage[page]):
            fontProperty = self.fontTable[fontname]
            fontLabel = drawfontPIL.DrawFontPIL(master=self.fontFrame, # 实例化
                                                font=fontname,
                                                text=self.fontText.get(),
                                                size=self.fontSize.get(),
                                                path=fontProperty['Path'], 
                                                isInstalled=fontProperty['IsInstalled'],
                                                tag=fontProperty['Tag'])
            self.fontLabels[page].append(fontLabel)

    def destroy_font_display(self, page=0):
        for fontLabel in self.fontLabels[page]:
            fontLabel.destroy()
        self.fontLabels[page] = []

    def create_pages(self, fontnameList=[]):
        self.pageNum = ceil(len(fontnameList) / self.pageSize)
        if self.pageNum==0: self.pageNum = 1
        self.fontLabels = [[] for i in range(self.pageNum)]
        fontnameList.sort()
        self.fontnameListinPage = []
        for i in range(self.pageNum):
            self.fontnameListinPage.append(fontnameList[i*self.pageSize:(i+1)*self.pageSize])
        self.pageBox.config(values=tuple(range(1, self.pageNum+1)))

    def import_fontTable(self, fontTable): self.fontTable = fontTable

    # downFrame
    def __multichoosebtn_click(self):
        def font_sel(event):
            if event.widget.isSelected==True:
                event.widget.config(background='white')
                event.widget.isSelected = False
            else: 
                event.widget.config(background='lightblue')
                event.widget.isSelected = True

        self.mode = 'multichoose'
        for fontLabel in self.fontLabels[self.page]:
            fontLabel.bind('<ButtonRelease-1>', font_sel)
        self.multiChooseBtn.grid_remove()
        self.sizetextBtn.config(state='disabled')
        self.cancelMultiChooseBtn.grid(row=0, column=0, sticky='w', padx=(5,5), pady=2)
        self.selAllBtn.grid(row=0, column=1, sticky='w', padx=(0,5), pady=2)
        self.setTagBtn.grid(row=0, column=2, sticky='w', padx=(0,5), pady=2)
        self.addTagBtn.grid(row=0, column=3, sticky='w', padx=(0,5), pady=2)
        self.delTagBtn.grid(row=0, column=4, sticky='w', padx=(0,5), pady=2)
        self.installBtn.grid(row=1, column=3, sticky='w', padx=(0,5), pady=(0,2))
        self.uninstallBtn.grid(row=1, column=4, sticky='w', padx=(0,5), pady=(0,2))
        self.delfromsysBtn.grid(row=1, column=1, sticky='ew', columnspan=2, padx=(0,5), pady=(0,2))
        self.pageBox.grid_remove()

    def __cancelmultichoosebtn_click(self):
        self.mode = 'normal'
        self.multiChooseBtn.grid()
        self.pageBox.grid()
        self.sizetextBtn.config(state='normal')
        self.cancelMultiChooseBtn.grid_remove()
        self.selAllBtn.grid_remove()
        self.setTagBtn.grid_remove()
        self.addTagBtn.grid_remove()
        self.delTagBtn.grid_remove()
        self.installBtn.grid_remove()
        self.uninstallBtn.grid_remove()
        self.delfromsysBtn.grid_remove()
        for fontLabel in self.fontLabels[self.page]:
            fontLabel['background'] = 'white'
            fontLabel.isSelected = False
            fontLabel.unbind('<ButtonRelease-1>')

    def __selall_click(self):
        self.selAllBtn.grid_remove()
        self.cancelSelAllBtn.grid(row=0, column=1, sticky='w', padx=(0,5), pady=2)
        for fontLabel in self.fontLabels[self.page]:
            fontLabel['background'] = 'lightblue'
            fontLabel.isSelected = True

    def __cancelselall_click(self):
        self.selAllBtn.grid()
        self.cancelSelAllBtn.grid_remove()
        for fontLabel in self.fontLabels[self.page]:
            fontLabel['background'] = 'white'
            fontLabel.isSelected = False

    # pageBox
    def __pagebox_sel(self, event):
        # destory old ones
        self.destroy_font_display(self.page)
        self.page = self.pageVar.get() - 1
        self.create_font_display(self.page)

    # upFrame
    def __size_text_click(self):
        # destory old ones
        self.destroy_font_display(self.page)
        self.create_font_display(self.page)
