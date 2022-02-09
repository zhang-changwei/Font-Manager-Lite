import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter.messagebox as messagebox
import win32con
import win32clipboard

class DrawFontPIL(ttk.Label):
    '''
    将字体嵌入Label
    property: path, isInstalled, tag, font字体名, tkImage, isSelected
    '''
    isSelected = False
    def __init__(self, master=None, font='楷体', text='這是示例文字', path='C:/Windows/Fonts/simkai.ttf', isInstalled=False, tag=None, size=20, maxwidth=550):
        self.path = path
        self.isInstalled = isInstalled
        self.tag = tag
        self.font = font
        self.draw_font(path, text=font+' '+text, size=size, maxwidth=maxwidth)
        super().__init__(master, image=self.tkImage, background='white', relief='flat')
        self.pack(fill='x', anchor='w')

        self.bind('<ButtonRelease-3>', self.__right_click)
        self.bind('<Enter>', self.__enter)
        self.bind('<Leave>', self.__leave)

    def draw_font(self, fontpath, text, size=20, maxwidth=550*1.5):
        ft = ImageFont.truetype(font=fontpath, size=size)
        width, height = ft.getsize(text=text)

        canvas = Image.new('L', size=(min(maxwidth,width), height), color=255)
        draw = ImageDraw.Draw(canvas)
        draw.text((0,0), text=text, fill=0, font=ft)

        self.tkImage = ImageTk.PhotoImage(canvas)

    def __enter(self, event): 
        self.config(relief='groove')
    def __leave(self, event): 
        self.config(relief='flat')

    def __copy(self):
        tmp = self.font.split(' ')[:-1]
        win32clipboard.OpenClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, ' '.join(tmp))
        win32clipboard.CloseClipboard()
        self.popup.destroy()

    def __copy_path(self):
        tmp = self.path
        win32clipboard.OpenClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, tmp)
        win32clipboard.CloseClipboard()
        self.popup.destroy()

    def __tag_install(self):
        self.event_generate('<<TagInstall>>')
        self.popup.destroy()

    def __tag_management(self):
        self.event_generate('<<TagManagement>>')
        self.popup.destroy()

    def __property(self):
        self.popup.destroy()
        messagebox.showinfo('Property',
            'Name:        {}\nPath:          {}\nIsInstalled: {}\nTags:          {}'.format(self.font, self.path, self.isInstalled, ', '.join(self.tag)))

    def __right_click(self, event):
        '''右键菜单'''
        self.popup=tk.Menu(self,tearoff=0)
        self.popup.add_command(label='Copy', command=self.__copy)
        self.popup.add_command(label='Copy Path', command=self.__copy_path)
        self.popup.add_separator()
        self.popup.add_command(label='Tag Management', command=self.__tag_management)
        if self.isInstalled==True:
            self.popup.add_command(label='Tag → uninstalled', command=self.__tag_install)
            self.popup.add_separator()
            self.popup.add_command(label='Uninstall') # install, uninstall
        else:
            self.popup.add_command(label='Tag → installed', command=self.__tag_install)
            self.popup.add_separator()
            self.popup.add_command(label='Install') 
        self.popup.add_command(label='Delete from System')
        self.popup.add_separator()
        self.popup.add_command(label='Property', command=self.__property)
        self.popup.post(event.x_root, event.y_root)

# root = tk.Tk()
# root.geometry('500x100')
# tmp = DrawFontPIL(root)
# root.mainloop()