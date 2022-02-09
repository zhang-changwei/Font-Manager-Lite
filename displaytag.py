import pickle
from tkinter import ttk
import tkinter as tk
import displaytop
from tkinter import messagebox

class TagGroup(ttk.Frame):
    '''
    property: tagBtns, tagList, insTagList, uninsTagList, tagTable
    '''
    def __init__(self, master=None):
        # Frame
        super().__init__(master)
        self.root = master

        self.tagBtns = []

    def create_display(self):
        self.upFrame = ttk.Frame(master=self)
        self.upFrame.pack(fill='x', side='top', anchor='nw')
        self.create_tag_display(master=self.upFrame)

        # Buttons
        downFrame = ttk.Frame(master=self)
        downFrame.pack(fill='x', side='bottom', anchor='center')
        self.create_btn_display(master=downFrame)
        
    def create_tag_display(self, master):
        self.insVar = tk.IntVar(value=1)
        self.uninsVar=tk.IntVar(value=1)
        self.insBtn = ttk.Checkbutton(master, text='installed', variable=self.insVar)
        self.uninsBtn = ttk.Checkbutton(master, text='uninstalled', variable=self.uninsVar)
        self.insBtn.grid(row=0, column=0, sticky='w', padx=(5,0), pady=(5,0))
        self.uninsBtn.grid(row=1, column=0, sticky='w', padx=(5,0))

        self.insCVar = tk.IntVar(value=len(self.insTagList))
        self.uninsCVar=tk.IntVar(value=len(self.uninsTagList))
        self.insCLabel = TagCount(master, var=self.insCVar)
        self.uninsCLabel = TagCount(master, var=self.uninsCVar)
        self.insCLabel.grid(row=0, column=1, sticky='ew', ipadx=15, pady=(5,0))
        self.uninsCLabel.grid(row=1, column=1, sticky='ew', ipadx=15)

        self.insCLabel.bind('<ButtonRelease-1>', self.__tag_sel)
        self.uninsCLabel.bind('<ButtonRelease-1>', self.__tag_sel)

        for i,tag in enumerate(self.tagList):
            tagVar  = tk.IntVar()
            tagCVar = tk.IntVar(value=len(self.tagTable[tag]))
            tagBtn = ttk.Checkbutton(master, text=tag, variable=tagVar)
            tagCLabel = TagCount(master, var=tagCVar)

            tagCLabel.bind('<ButtonRelease-1>', self.__tag_sel)

            tagBtn.grid(row=i+2, column=0, sticky='w', padx=(5,0))
            tagCLabel.grid(row=i+2, column=1, sticky='ew', ipadx=15)
            self.tagBtns.append([tagBtn, tagVar, tagCLabel, tagCVar])

    def create_btn_display(self, master):
        self.upBtn = ttk.Button(master, text='Up', width=8, command=self.__tag_up)
        self.downBtn=ttk.Button(master, text='Down', width=8, command=self.__tag_down)
        self.upBtn.grid(row=0, column=0, sticky='NEWS', pady=2, padx=(10,2))
        self.downBtn.grid(row=0, column=1, sticky='NEWs', pady=2)
        self.addBtn = ttk.Button(master, text='Add', width=8, command=self.__append_tag)
        self.delBtn=ttk.Button(master, text='Delete', width=8)
        self.addBtn.grid(row=1, column=0, sticky='NEWS', pady=2, padx=(10,2))
        self.delBtn.grid(row=1, column=1, sticky='NEWS', pady=2)

        self.updateBtn = ttk.Button(master, text='Update', command=self.__tag_up)
        self.updateBtn.grid(row=2, column=0, columnspan=2,sticky='NEWS', padx=(10,0), pady=2)

        self.progBar = ttk.Label(master, text='Success!', anchor='center', background='#06B025')
        self.progBar.grid(row=3, column=0, columnspan=2,sticky='NEWS', padx=(10,0), pady=(2,10))

    def generate_tag_info(self, fontTable, init=False):
        def judge_ins(name, judge):
            if judge==True: self.insTagList.append(name)
            else: self.uninsTagList.append(name)

        if init==False: # tagList 不变
            pass
        elif init==None:
            self.tagList = {'new'} # init
            for v in fontTable.values():
                self.tagList = self.tagList.union(v['Tag'])
            self.tagList = list(self.tagList)
        else:
            self.tagList = init # 传入 init tagList
            

        self.insTagList = []
        self.uninsTagList = []
        
        if init==None: self.tagList.sort()

        self.tagTable = {k: [] for k in self.tagList}
        for k,v in fontTable.items():
            judge_ins(k, v['IsInstalled'])
            for tag in v['Tag']:
                self.tagTable[tag].append(k)

    def generate_fontnameList(self):
        fontnameList = set()
        if self.insVar.get()==1: fontnameList = fontnameList.union(self.insTagList)
        if self.uninsVar.get()==1: fontnameList = fontnameList.union(self.uninsTagList)
        for tag in self.tagBtns:
            if tag[1].get()==1:
                t = tag[0].cget('text')
                fontnameList = fontnameList.union(self.tagTable[t])
        return list(fontnameList)

    def recount_fontnum_in_tag(self):
        self.insCVar.set(len(self.insTagList))
        self.uninsCVar.set(len(self.uninsTagList))
        for tag in self.tagBtns:
            t = tag[0].cget('text')
            tag[3].set(len(self.tagTable[t]))

    # methods
    def __append_tag(self):
        # Entry Window
        self.topGroup = displaytop.TopEntryGroup(master=self.root, title='Add')
        self.root.bind('<Control-Shift-Y>', self.__append_toplevel)

    def __append_toplevel(self, event):
        clicked = self.topGroup.clicked
        if clicked=='yes':
            tag = self.topGroup.var.get()
            if tag not in self.tagList and tag!='uninstalled' and tag!='installed':
                self.tagList.append(tag)
                self.tagTable[tag] = []

                # add buttons
                tagVar  = tk.IntVar()
                tagCVar = tk.IntVar(value=0)
                tagBtn = ttk.Checkbutton(master=self.upFrame, text=tag,variable=tagVar)
                tagCLabel = TagCount(master=self.upFrame, var=tagCVar)

                i = len(self.tagList) + 1
                tagBtn.grid(row=i, column=0, sticky='w', padx=(5,0))
                tagCLabel.grid(row=i, column=1, sticky='ew', ipadx=15)
                self.tagBtns.append([tagBtn, tagVar, tagCLabel, tagCVar])

                tagCLabel.bind('<ButtonRelease-1>', self.__tag_sel)
            else:
                messagebox.showwarning('Add Tag', 'Cannot Add Tag \'{}\'.'.format(tag))
        self.topGroup.destroy()
        self.root.unbind('<Control-Shift-Y>')

    def __tag_sel(self, event):
        if self.insCLabel.isSelected==True:
            self.insCLabel.isSelected = False
            self.insCLabel.config(background='SystemButtonFace')
        elif self.uninsCLabel.isSelected==True:
            self.uninsCLabel.isSelected = False
            self.uninsCLabel.config(background='SystemButtonFace')
        else:
            for tag in self.tagBtns:
                if tag[2].isSelected==True:
                    tag[2].isSelected = False
                    tag[2].config(background='SystemButtonFace')
                    break
        event.widget.config(background='lightblue')
        event.widget.isSelected = True

    def __tag_up(self):
        i = 1
        for n,tag in enumerate(self.tagBtns):
            i = i + 1
            if n==0 and tag[2].isSelected==True: break
            if tag[2].isSelected==True:
                tagup, tagdown = self.tagBtns[n-1], self.tagBtns[n]
                self.tagBtns.pop(n)
                self.tagBtns.insert(n-1, tagdown)
                tagup[0].grid_forget()
                tagup[2].grid_forget()
                tagdown[0].grid_forget()
                tagdown[2].grid_forget()
                tagup[0].grid(row=i, column=0, sticky='w', padx=(5,0))
                tagup[2].grid(row=i, column=1, sticky='ew', ipadx=15)
                tagdown[0].grid(row=i-1, column=0, sticky='w', padx=(5,0))
                tagdown[2].grid(row=i-1, column=1, sticky='ew', ipadx=15)
                break
    def __tag_down(self):
        i = 1
        for n,tag in enumerate(self.tagBtns):
            i = i + 1
            if n==len(self.tagBtns) and tag[2].isSelected==True: break
            if tag[2].isSelected==True:
                tagup, tagdown = self.tagBtns[n], self.tagBtns[n+1]
                self.tagBtns.pop(n)
                self.tagBtns.insert(n+1, tagup)
                tagup[0].grid_forget()
                tagup[2].grid_forget()
                tagdown[0].grid_forget()
                tagdown[2].grid_forget()
                tagup[0].grid(row=i+1, column=0, sticky='w', padx=(5,0))
                tagup[2].grid(row=i+1, column=1, sticky='ew', ipadx=15)
                tagdown[0].grid(row=i, column=0, sticky='w', padx=(5,0))
                tagdown[2].grid(row=i, column=1, sticky='ew', ipadx=15)
                break 

    def import_from_conf(self):
        with open('data/taglist.pickle', 'rb') as f:
            return pickle.load(f)

    def export_taglist(self):
        with open('data/taglist.pickle', 'wb') as f:
            pickle.dump(self.tagList, f)

class TagCount(ttk.Label):
    isSelected = False
    def __init__(self, master, var):
        super().__init__(master, textvariable=var, background=None, anchor='e')



