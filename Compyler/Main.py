#-*-   coding:   utf-8   -*-

from tkinter import *
import tkinter.font
import tkinter.messagebox
from tkinter import filedialog
import os
from Preprocessor import Preprocessor
from IDHolder import IDHolder
from LexAnalyzer import LexAnalyzer
from MidCoder import MidCoder
import Helper
import Types as Tp
from Dyad import Dyad

class Root:
    def __init__(self):
        self.root = Tk()
        self.root.title('New')
        self.file = None
        self.textChanged = False
        self.idh = IDHolder()
        self.pre = Preprocessor()
        self.lxa = LexAnalyzer(self.idh)
        self.mdc = MidCoder(self.idh)
        
    def Init(self):
        self.idh.Init()
        self.pre.Init()
        self.lxa.Init()
        self.mdc.Init()
        
    def LoadWidgets(self):
        self.xscr = Scrollbar(orient = HORIZONTAL)
        self.xscr.pack(side = BOTTOM, fill = X)
        
        self.yscr = Scrollbar()
        self.yscr.pack(side = RIGHT, fill = Y)
        
        self.text = Text(self.root, wrap='none', font = tkinter.font.Font(size = 12))
        self.text.pack(side = TOP, fill = X)
        self.text.bind('<Key>', self.CatchKey)
        
        
        self.xscr.config(command = self.text.xview)
        self.text.config(xscrollcommand = self.xscr.set)
        
        self.yscr.config(command = self.text.yview)
        self.text.config(yscrollcommand = self.yscr.set)
        
        self.men = Menu(self.root)
        
        self.fmen = Menu(self.men, tearoff = 0)
        self.fmen.add_command(label = 'New', command = self.NewFile)
        self.fmen.add_command(label = 'Open', command = self.OpenFile)
        self.fmen.add_command(label = 'Save', command = self.SaveFile)
        self.fmen.add_command(label = 'Save as', command = self.SaveAs)
        
        self.cmen = Menu(self.men, tearoff = 0)
        self.cmen.add_command(label = 'Intermediate Code', command = self.Compile)
        
        self.hmen = Menu(self.men, tearoff = 0)
        for each in ['Help']:
            self.hmen.add_command(label = each)
            
        self.men.add_cascade(label = 'File', menu = self.fmen)
        self.men.add_cascade(label = 'Compile', menu = self.cmen)
        self.men.add_cascade(label = 'About', menu = self.hmen)
        
        self.hmen = Menu(self.men)
        self.root['menu'] = self.men
                   
    def Show(self):
        self.root.mainloop()
    
    def NewFile(self):
        if self.textChanged == True:
            do = tkinter.messagebox.askyesno('!', 'Save current file?')
            if do == True:
                self.SaveFile()
                return
        
        self.text.delete(0.0, END)
        self.textChanged = False
        self.file = None
        self.root.title('New')
    
    def OpenFile(self):
        if self.textChanged == True:
            do = tkinter.messagebox.askyesno('!', 'Save current file?')
            if do == True:
                self.SaveFile()
                return
        
        path = filedialog.askopenfilename()
        if path == '':
            return
            
        self.text.delete(0.0, END)
        self.textChanged = False
        with open(path, encoding = 'utf-8') as self.file:
            self.root.title(self.file.name)
            line = self.file.readline()
            while line:
                self.text.insert(END, line)
                line = self.file.readline()
            
    def SaveFile(self):
        if self.file is None:
            self.SaveAs()
        else:
            if self.textChanged == True:
                self.textChanged = False
                self.root.title(self.file.name)
                with open(self.file.name, 'w', encoding = 'utf-8') as self.file:
                    self.file.write(self.text.get(0.0, END))
            
    def SaveAs(self):
        path = filedialog.asksaveasfilename(defaultextension = '.txt', filetypes = [('all files', '.*'), ('text files', '.txt')])
        if path == '':
            return
            
        self.textChanged = False
        with open(path, 'w', encoding = 'utf-8') as self.file:
            self.root.title(self.file.name)
            self.file.write(self.text.get(0.0, END))
    
    def Compile(self):
        self.SaveFile()
        self.Init()
        with open(self.file.name, 'r', encoding = 'utf-8') as self.file:
            line = ''
            count = 0
            for line in self.file:
                line = line.strip()
                sentences = self.pre.Do(line)
                for sen in sentences:
                    lex = self.lxa.Do(sen)
                    r = self.mdc.Do(Helper.lex2dyads(lex))
                    if r == Tp.ERR:
                        print('Error occured in line %d : %s'%(count, line))
                        return
                count += 1
            lex = self.lxa.Do(self.pre.GetTail())
            r = self.mdc.Do(Helper.lex2dyads(lex) + [Dyad(Tp.EOF, None)])
            if r != Tp.ACC:
                print('Error occured in line %d'%count)
                return
            else:
                print('Accepted!')
        quads = self.mdc.GetQuads()
        with open(os.path.join(os.path.dirname(self.file.name), 'o.txt'), 'w', encoding = 'utf-8') as ofile:
            for q in quads:
                ofile.write('%s\n'%q.ToStr())
    
    def CatchKey(self, event):
        if event.char == '':
            return
        self.textChanged = True
        if self.file is None:
            self.root.title('* New')
        else:
            self.root.title('* ' + self.file.name)
                
if __name__ == '__main__':
    r = Root()
    r.LoadWidgets()
    r.Show()