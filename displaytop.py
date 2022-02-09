import tkinter as tk
from tkinter import ttk
from pyautogui import hotkey

class TopUniversialGroup(tk.Toplevel):
    def __init__(self, master=None, title='TopLevel'):
        super().__init__(master)
        self.root = master
        self.title(title)
        self.withdraw()

    def middle_display(self):
        def del_win(): pass
        self.protocol('WM_DELETE_WINDOW', del_win) # 禁用右上角关闭
        self.update() # 刷新后，下面代码才能得到正确的宽和高尺寸
        a, b = self.winfo_width(), self.winfo_height() # 得到弹出窗体的宽和高
        c = self.root.winfo_x()+((self.root.winfo_width()-a)/2) # 左边距=主窗口左边距+[(主窗口宽－弹出窗体宽)/2]
        d = self.root.winfo_y()+((self.root.winfo_height()-b)/2) # 上边距=主窗口上边距+[(主窗口高－弹出窗体高)/2]
        self.geometry('%dx%d+%d+%d' % (a,b,c,d)) # 弹出窗体相对主窗体居中显示
        self.attributes("-toolwindow", 1) # 无最大化，最小化
        self.attributes('-topmost',1) # 窗口置顶其它窗体之上
        self.transient(self.root) # 窗口只置顶root之上
        self.resizable(False,False) # 不可调节窗体大小
        self.grab_set() # 转化模式，不关闭弹窗就不能进行别的操作
        self.deiconify() # 窗口再显现

class TopYesNoGroup(TopUniversialGroup):
    def __init__(self, master=None, title='TopLevel'):
        super().__init__(master, title)
        # yesno
        frame = ttk.Frame(master=self)
        frame.pack(side='bottom', fill='x')
        self.yesBtn = ttk.Button(master=frame, text='OK', width=9, command=self.__yes_click)
        self.noBtn = ttk.Button(master=frame, text='Cancel', width=9, command=self.__no_click)
        self.yesBtn.pack( side='left',  padx=(10,4), pady=(0,8))
        self.noBtn.pack(side='right', padx=(4,10), pady=(0,8))
        self.noBtn.focus_force()  # 文本框得到焦点

    def __no_click(self):
        self.grab_release()
        try:
            self.root.attributes('-topmost',1)
        except:
            pass
        self.root.focus_force()
        self.clicked = 'no'
        hotkey('ctrl', 'shift', 'y')
    def __yes_click(self):
        self.grab_release()
        try:
            self.root.attributes('-topmost',1)
        except:
            pass
        self.root.focus_force()
        self.clicked = 'yes'
        hotkey('ctrl', 'shift', 'y')

class TopTagGroup(TopYesNoGroup):

    def __init__(self, master=None, title='TopLevel', tagList=[]):
        super().__init__(master, title)
        self.btnList = []
        # checkboxs
        frame = ttk.Frame(master=self)
        frame.pack(side='top', pady=(15,10))
        for tag in tagList:
            cbVar = tk.IntVar()
            cbBtn = ttk.Checkbutton(master=frame, variable=cbVar, text=tag)
            cbBtn.pack(side='top', anchor='w', fill='x', padx=(35,35), pady=(0,3))
            self.btnList.append([cbBtn, cbVar])
            
        self.middle_display()

class TopEntryGroup(TopYesNoGroup):

    def __init__(self, master=None, title='TopLevel', text='Please Enter '):
        super().__init__(master, title)

        self.var = tk.StringVar()
        lbl = ttk.Label(master=self, text=text, anchor='center')
        lbl.pack(side='top', fill='x', pady=(15,0))
        ent = ttk.Entry(master=self, textvariable=self.var, width=20)
        ent.pack(side='top', fill='y', pady=(15,25))
        ent.focus_force()

        self.middle_display()