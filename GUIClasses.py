import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import re
from json import dumps, loads

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder_color = ("#000000")
        self.default_fg_color = self['fg']
        self.placeholder = ''
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

    def setPlaceholder(self,placeholder):
        self.placeholder = placeholder
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

def clear(text_stuff):
    text_stuff.delete("1.0", tk.END)
    
class JsonEditor(ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<FocusOut>", self.indent_json)
        self.bind("<Tab>", self.tab)
        self.delim_re = re.compile(
        '''
        line\s(?P<line>\d+)\s
        column\s(?P<col>\d+)\s
        \(
            char\s(?P<before>\d+)
            (\s\-\s(?P<after>\d+))? # optionally followed by a range
        \)''', re.VERBOSE)
        self.ErrorText = None
    
    def init(self):
        self.insert("1.0", """{ "id" : 10}""")
        self.indent_json(LOG=False)
    def setError(self,scroll):
        self.ErrorText=scroll

    def indent_json(self,*args,LOG=True):
        if self.get("1.0",tk.END).strip() == "":
            if LOG:self.log("Indentation not needed")
            return True
        if self.validate_json(LOG=LOG):
            str_json = self.get("1.0",tk.END)
            clear(self)
            if LOG:clear(self.ErrorText)
            self.insert('1.0', dumps(loads(str_json), indent=4))
            if LOG:self.log("Indentation done")
            return True
        else: 
            if LOG:self.log("please correct errors first")
            return False

    def validate_json(self,*args,LOG=True):
        if LOG:clear(self.ErrorText)
        str_json = self.get("1.0",tk.END)
        self.tag_delete("error")
        try:
            loads(str_json)
        except ValueError as e:
            clear(self.ErrorText)
            msg = str(e.args)
            if LOG:self.log(msg)
            mark = self.delim_re.search(msg)
            if not mark:
                mark = dict(before = "0", after = "end", line = "0", col = "0")
            else:
                mark = mark.groupdict()
                mark["after"] =  "1.0 +%sc" % (mark["after"] or (int(mark["before"]) +1))
            
            before = "1.0 +%(before)sc" % mark
            has_delim = re.search("Expecting '(?P<delim>.)'", msg)
            if has_delim:
                after = mark["after"] = "1.0 +%dc" % (int(mark["before"]) +1)
            
                self.insert(before,has_delim.groupdict()["delim"])
                #text.delete(after)
            after = "%s" % mark["after"]
            self.tag_add("error", before, after)
            self.tag_config("error", background="yellow", foreground="red")
            return False
        except Exception as e:
            if LOG:self.log(e)
            return False
        if LOG:self.log("JSON is valid")
        return True

    def insertJson(self,jsonData):
        clear(self)
        self.insert("1.0", jsonData)
        self.indent_json()

    def getActualJson(self):
        return loads(self.get("1.0",tk.END))
    
    def clear(self):
        clear(self)

    def tab(self,arg):
        self.insert(tk.INSERT, " " * 4)
        return 'break'
    def log(self,msg):
        self.ErrorText.insert("1.0", (type(msg) is str and msg or repr(msg))+ "\n")
