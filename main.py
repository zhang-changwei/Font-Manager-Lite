import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import displaytag
import displaymenu
import displaynotebook
import displaytop
import myfont
import config
import re
import os

class App:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title('Font Manager Lite')
        self.root.protocol('WM_DELETE_WINDOW', self.__exit)
        # self.root.geometry('800x700')
        
        # menu
        self.menuGroup = displaymenu.MenuGroup(self.root)
        self.menu_commands()

        # tagGroup
        self.tagGroup = displaytag.TagGroup(self.root)

        # my font
        self.myFont = myfont.MyFontGroup()
        inittagList = self.init_import() # 数据导入 -> MyFontGroup & TagGroup
        fontnameList = list(self.myFont.fontTable.keys())
        
        # tagGroup
        self.tagGroup.generate_tag_info(self.myFont.fontTable, init=inittagList) # tagTable, tagList
        self.tagGroup.create_display()
        self.tag_commands()

        # noteGroup
        self.noteGroup = displaynotebook.NoteGroup(self.root)

        # fontGroup
        self.noteGroup.fontGroup.import_fontTable(self.myFont.fontTable) # copy fontTable
        self.noteGroup.fontGroup.create_pages(fontnameList)
        self.noteGroup.fontGroup.create_font_display(page=0)
        self.font_commands()

        # searchGroup
        self.noteGroup.searchGroup.import_fontTable(self.myFont.fontTable) # copy fontTable 共享内存

        # dupGroup
        self.noteGroup.dupGroup.create_pages(self.myFont.dupTable, pageSize=config.dupeperpage)
        self.noteGroup.dupGroup.create_display(page=0)
        self.dup_commands()

        self.root.bind('<<NotebookTabChanged>>', self.notebook_tab_changed)
        self.root.bind('<<TagInstall>>', self.pil_tag_install)
        self.root.bind('<<TagManagement>>', self.pil_tag_management)


    def display(self):
        sep = ttk.Separator(self.root, orient='vertical')
        self.tagGroup.pack(side='left', fill='y')
        sep.pack(side='left', fill='y', padx=10, pady=10)
        self.noteGroup.pack(side='left', fill='y', pady=(5,8), padx=(0,8))
        self.root.mainloop()

    def menu_commands(self):
        self.menuGroup.fileMenu.add_command(label='Open Font Files', command=self.import_from_files)
        self.menuGroup.fileMenu.add_command(label='Open Font Files from Folder', command=self.import_from_folder)
        self.menuGroup.fileMenu.add_separator()
        self.menuGroup.fileMenu.add_command(label='Save Font Config', command=self.__save)
        self.menuGroup.fileMenu.add_command(label='Exit', command=self.__destroy)

        self.menuGroup.optionMenu.add_command(label='Rescan', command=self.scan)
        self.menuGroup.optionMenu.add_separator()
        self.menuStyleVar = tk.StringVar(value='Tall')
        self.menuGroup.optionMenu.add_radiobutton(label='Style: Tall', command=self.canvas_style, value='Tall', variable=self.menuStyleVar)
        self.menuGroup.optionMenu.add_radiobutton(label='Style: Short', command=self.canvas_style, value='Short', variable=self.menuStyleVar)
    def tag_commands(self):
        self.tagGroup.delBtn.config(command=self.remove_tag)
        self.tagGroup.updateBtn.config(command=self.update)
    def font_commands(self):
        self.noteGroup.fontGroup.setTagBtn.config(command=lambda s=self,arg='Set Tag': s.font_settag(arg))
        self.noteGroup.fontGroup.addTagBtn.config(command=lambda s=self,arg='Add Tag': s.font_settag(arg))
        self.noteGroup.fontGroup.delTagBtn.config(command=lambda s=self,arg='Del Tag': s.font_settag(arg))
    def dup_commands(self):
        self.noteGroup.dupGroup.okBtn.config(command=self.dup)
    # notebook
    def notebook_tab_changed(self, event):
        notePage = self.noteGroup.index(self.noteGroup.select()) # 当前选项卡序号
        if notePage==0: # Main
            self.tagGroup.delBtn.config(state='normal')
            self.tagGroup.updateBtn.config(state='normal')
        if notePage==1: # search
            self.tagGroup.delBtn.config(state='disabled')
            self.tagGroup.updateBtn.config(state='disabled')
            # self.noteGroup.searchGroup.import_fontTable(self.myFont.fontTable) # copy fontTable
        elif notePage==2: # dup
            self.tagGroup.delBtn.config(state='disabled')
            self.tagGroup.updateBtn.config(state='disabled')


    def __refresh_tagGroup(self, a=True, b=True, c=True):
        '''
        a: generate_tag_info, # tagTable, tagList
        b: recount_fontnum_in_tag, 
        c: generate_fontnameList
        '''
        if a: self.tagGroup.generate_tag_info(self.myFont.fontTable) # tagTable, tagList
        if b: self.tagGroup.recount_fontnum_in_tag()
        if c: 
            fontnameList = self.tagGroup.generate_fontnameList() # fontnameList
            return fontnameList
    def __refresh_fontGroup(self, a=True, b=True, c=True, fontnameList=None, page=None):
        '''
        a: multichoose, # close multichoose
        b: destroy_font_display, 
        c: import_fontTable # copy fontTable
        '''
        if a and self.noteGroup.fontGroup.mode=='multichoose': self.noteGroup.fontGroup.cancelMultiChooseBtn.invoke()
        if b: self.noteGroup.fontGroup.destroy_font_display(page=self.noteGroup.fontGroup.page)
        if c: self.noteGroup.fontGroup.import_fontTable(self.myFont.fontTable) # copy fontTable
        if fontnameList!=None: self.noteGroup.fontGroup.create_pages(fontnameList)
        if page!=None:
            page = min(page, self.noteGroup.fontGroup.pageNum-1)
            self.noteGroup.fontGroup.create_font_display(page=page)
            self.noteGroup.fontGroup.pageVar.set(page+1) # start from 1

    # Font methods
    # Set/Add/Del Tag
    def font_settag(self, arg):
        if arg=='Set Tag':
            self.topGroup = displaytop.TopTagGroup(master=self.root, title=arg, tagList=self.tagGroup.tagList)
        elif arg=='Add Tag':
            self.topGroup = displaytop.TopTagGroup(master=self.root, title=arg, tagList=self.tagGroup.tagList)
        elif arg=='Del Tag':
            self.topGroup = displaytop.TopTagGroup(master=self.root, title=arg, tagList=self.tagGroup.tagList)
        else:
            print('Error')

        self.root.bind('<Control-Shift-Y>', self.__font_settag2)
    def __font_settag2(self, event):
        # prog
        self.tagGroup.progBar.config(text='Wait for it...', background='yellow')
        self.tagGroup.progBar.update()
        
        clicked = self.topGroup.clicked
        if clicked=='yes':
            tags, fonts = [],[]
            for tag in self.topGroup.btnList:
                if tag[1].get()==1: tags.append(tag[0].cget('text'))
            page = self.noteGroup.fontGroup.page
            for ftlbl in self.noteGroup.fontGroup.fontLabels[page]:
                if ftlbl.isSelected==True:
                    fonts.append(ftlbl.font)
            if tags!=[] and fonts!=[]:
                # refresh myFont
                if self.topGroup.title()=='Set Tag':
                    self.myFont.set_tag(fonts=fonts, tags=tags)
                elif self.topGroup.title()=='Add Tag':
                    self.myFont.add_tag(fonts=fonts, tags=tags)
                elif self.topGroup.title()=='Del Tag':
                    self.myFont.remove_tag(fonts=fonts, tags=tags)
                else:
                    print('Error')
                # tagGroup
                fontnameList = self.__refresh_tagGroup(True, True, True)
                # fontGroup
                self.__refresh_fontGroup(True, True, True, fontnameList, page)
        
        self.topGroup.destroy()
        self.root.unbind('<Control-Shift-Y>')
        # prog
        self.tagGroup.progBar.config(text='Success!', background='#06B025')
        self.tagGroup.progBar.update()

    # PIL methods # ins & unins
    def pil_tag_install(self, event):
        # prog
        self.tagGroup.progBar.config(text='Wait for it...', background='yellow')
        self.tagGroup.progBar.update()

        ins = event.widget.isInstalled
        ft = event.widget.font
        if ins==True: # installed -> uninstalled
            # PIL
            event.widget.isInstalled = False
            # fontGroup
            font = self.noteGroup.fontGroup.fontTable[ft]
            font['Forced'] = True
            font['IsInstalled'] = False
            self.noteGroup.fontGroup.fontTable[ft] = font
            # tagGroup
            self.tagGroup.insTagList.remove(ft)
            self.tagGroup.uninsTagList.append(ft)
            self.tagGroup.insCVar.set(self.tagGroup.insCVar.get()-1)
            self.tagGroup.uninsCVar.set(self.tagGroup.uninsCVar.get()+1)
            # myFont
            font = self.myFont.fontTable[ft]
            font['Forced'] = True
            font['IsInstalled'] = False
            self.myFont.fontTable[ft] = font
        else: # uninstalled -> installed
            # PIL
            event.widget.isInstalled = True
            # fontGroup
            font = self.noteGroup.fontGroup.fontTable[ft]
            font['Forced'] = True
            font['IsInstalled'] = True
            self.noteGroup.fontGroup.fontTable[ft] = font
            # tagGroup
            self.tagGroup.insTagList.append(ft)
            self.tagGroup.uninsTagList.remove(ft)
            self.tagGroup.insCVar.set(self.tagGroup.insCVar.get()+1)
            self.tagGroup.uninsCVar.set(self.tagGroup.uninsCVar.get()-1)
            # myFont
            font = self.myFont.fontTable[ft]
            font['Forced'] = True
            font['IsInstalled'] = True
            self.myFont.fontTable[ft] = font
        # prog
        self.tagGroup.progBar.config(text='Success!', background='#06B025')
        self.tagGroup.progBar.update()

    def pil_tag_management(self, event):
        oldTags = event.widget.tag
        self.topGroup = displaytop.TopTagGroup(master=event.widget, title='Tag Management', tagList=self.tagGroup.tagList)
        for tag in self.topGroup.btnList:
            if tag[0].cget('text') in oldTags: tag[1].set(1)
        event.widget.bind('<Control-Shift-Y>', self.__pil_tag_management2)
    def __pil_tag_management2(self, event):
        # prog
        self.tagGroup.progBar.config(text='Wait for it...', background='yellow')
        self.tagGroup.progBar.update()

        oldTags = event.widget.tag
        ft = event.widget.font
        clicked = self.topGroup.clicked
        if clicked=='yes':
            tags = []
            for tag in self.topGroup.btnList:
                if tag[1].get()==1: tags.append(tag[0].cget('text'))
            # PIL
            event.widget.tag = tags
            # fontGroup
            font = self.noteGroup.fontGroup.fontTable[ft]
            font['Tag'] = tags
            self.noteGroup.fontGroup.fontTable[ft] = font
            # tagGroup tagTable & Btns
            # del old tags
            for v in oldTags:
                self.tagGroup.tagTable[v].remove(ft)
            for v in self.tagGroup.tagBtns:
                if v[0].cget('text') in oldTags: v[3].set(v[3].get()-1)
            # add new tags
            for k,v in self.tagGroup.tagTable.items():
                if k in tags: self.tagGroup.tagTable[k].append(ft)
            for v in self.tagGroup.tagBtns:
                if v[0].cget('text') in tags: v[3].set(v[3].get()+1)
            # myFont
            font = self.myFont.fontTable[ft]
            font['Tag'] = tags
            self.myFont.fontTable[ft] = font
            # lightred
            event.widget['background'] = 'lightpink'
        self.topGroup.destroy()
        self.root.focus_force()
        event.widget.unbind('<Control-Shift-Y>')
        # prog
        self.tagGroup.progBar.config(text='Success!', background='#06B025')
        self.tagGroup.progBar.update()

    # Tag methods
    def remove_tag(self):
        # prog
        self.tagGroup.progBar.config(text='Wait for it...', background='yellow')
        self.tagGroup.progBar.update()
        
        trigger = -1
        for i,tag in enumerate(self.tagGroup.tagBtns):
            if tag[2].isSelected==True:
                trigger = i
                tagname = tag[0].cget('text')
                if tagname=='new':
                    messagebox.showwarning(title='Delete Tag', message='Cannot Delete Tag \'new\'.')
                    # prog
                    self.tagGroup.progBar.config(text='Success!', background='#06B025')
                    self.tagGroup.progBar.update()
                    return
                tag[0].destroy()
                tag[2].destroy()
            elif trigger!=-1:
                tag[0].grid_forget()
                tag[2].grid_forget()
                tag[0].grid(row=i+1, column=0, sticky='w', padx=(5,0))
                tag[2].grid(row=i+1, column=1, sticky='ew', ipadx=15)
        if trigger!=-1:
            self.tagGroup.tagBtns.pop(trigger)
            self.tagGroup.tagList.remove(tagname)
            self.tagGroup.tagTable.pop(tagname)

            # refresh myFont
            self.myFont.remove_tag(list(self.myFont.fontTable.keys()), [tagname])
            # tagGroup
            fontnameList = self.tagGroup.generate_fontnameList() # fontnameList
            # fontGroup
            self.__refresh_fontGroup(True, True, True, fontnameList, page=0)
        # prog
        self.tagGroup.progBar.config(text='Success!', background='#06B025')
        self.tagGroup.progBar.update()

    def update(self):
        # prog
        self.tagGroup.progBar.config(text='Wait for it...', background='yellow')
        self.tagGroup.progBar.update()
        # tagGroup
        fontnameList = self.tagGroup.generate_fontnameList() # fontnameList
        # fontGroup
        self.__refresh_fontGroup(True, True, True, fontnameList, page=0)
        # prog
        self.tagGroup.progBar.config(text='Success!', background='#06B025')
        self.tagGroup.progBar.update()
        
    # dup methods
    def dup(self):
        # prog
        self.tagGroup.progBar.config(text='Wait for it...', background='yellow')
        self.tagGroup.progBar.update()

        page = self.noteGroup.dupGroup.pageVar.get()-1
        # myFont fontTable & dupTable
        for i in self.noteGroup.dupGroup.dupVars:
            if i[1].get()=='Both': continue
            elif i[0] in self.myFont.fontTable.keys():
                self.myFont.fontTable[i[0]]['Path'] = i[1].get()
                # del font
                paths = self.myFont.dupTable[i[0]]
                paths.remove(i[1].get())

                delList = []
                for j, path in enumerate(paths):
                    judge = self.delete_font(path, checksysfont=True)
                if judge==True: # so wrong!
                    del self.myFont.dupTable[i[0]]
        self.noteGroup.dupGroup.destroy_display()
        self.noteGroup.dupGroup.create_pages(self.myFont.dupTable, pageSize=config.dupeperpage)
        self.noteGroup.dupGroup.create_display(page=min(page, self.noteGroup.dupGroup.pageNum-1))
        # prog
        self.tagGroup.progBar.config(text='Success!', background='#06B025')
        self.tagGroup.progBar.update()

    # Menu methods
    def scan(self):
        self.myFont.scan()
        # tagGroup
        fontnameList = self.__refresh_tagGroup(True, True, True)
        # fontGroup
        self.__refresh_fontGroup(True, True, True, fontnameList, page=0)
        # dupGroup
        self.noteGroup.dupGroup.destroy_display()
        self.noteGroup.dupGroup.create_pages(self.myFont.dupTable, pageSize=config.dupeperpage)
        self.noteGroup.dupGroup.create_display(page=0)

    def canvas_style(self):
        if self.menuStyleVar.get()=='Tall':
            self.noteGroup.fontGroup.canvas.config(height=500)
            self.noteGroup.fontGroup.canvas.update()
            config.maxsearch = 15
            config.dupeperpage = 5
        else:
            self.noteGroup.fontGroup.canvas.config(height=300)
            self.noteGroup.fontGroup.canvas.update()
            config.maxsearch = 10
            config.dupeperpage = 3
            self.noteGroup.searchGroup.searchText.set('')
            self.noteGroup.searchGroup.searchtBtn.invoke()
            self.noteGroup.dupGroup.destroy_display()
            self.noteGroup.dupGroup.create_pages(self.myFont.dupTable, pageSize=config.dupeperpage)
            self.noteGroup.dupGroup.create_display(page=0)
            self.noteGroup.select(0)

    def import_from_files(self):
        paths = filedialog.askopenfilenames(title='Open Font Files',
                                            filetypes=[('font file', ['*.ttf','*.ttc','*.otf','*.fon','*.afm','*.eof','*.woff'])] )
        if paths!='':
            self.myFont.import_from_files(paths) # fontTable
            # tagGroup
            fontnameList = self.__refresh_tagGroup(True, True, True)
            # fontGroup
            self.__refresh_fontGroup(True, True, True, fontnameList, page=0)

            messagebox.showinfo('Open Font Files from Folder', 'Success!')

    def import_from_folder(self):
        folder = filedialog.askdirectory(title='Open Font Files from Folder')
        if folder!='':
            self.myFont.import_from_folder(folder)
            # tagGroup
            fontnameList = self.__refresh_tagGroup(True, True, True)
            # fontGroup
            self.__refresh_fontGroup(True, True, True, fontnameList, page=0)

            messagebox.showinfo('Open Font Files from Folder', 'Success!')

    def init_import(self):
        if os.path.exists('data')==False: os.mkdir('data')
        if os.path.exists('data/uninstalled')==False: os.mkdir('data/uninstalled')
        if os.path.exists('data/fonttable.pickle')==False:
            self.myFont.import_from_folder('C:/Windows/Fonts')
        else:
            self.myFont.import_from_conf()
            return self.tagGroup.import_from_conf()

    def delete_font(self, path, checksysfont=False):
        if checksysfont==True and re.match('C:\\\\Windows\\\\Fonts\\\\', path, flags=re.I)!=None:
            print('Skip: {}'.format(path))
            return # wrong
        try:
            os.remove(path)
        except:
            print('Error: Cannot remove font')

    def __exit(self):
        tmp = messagebox.askyesnocancel(title='关闭程序', message='保存字体数据并离开')
        if tmp==True:
            self.__save(exit=True)
            self.__destroy()
        elif tmp==False:
            self.__destroy()        

    def __save(self, exit=False):
        self.myFont.export_fonttable()
        self.myFont.export_duptable()
        self.myFont.export_ignList()
        self.tagGroup.export_taglist()
        if exit==True: return 
        messagebox.showinfo('Save Font Config', 'Success!')

    def __destroy(self): self.root.destroy()

if __name__=='__main__':
    app = App()
    app.display()