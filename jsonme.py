'''
Source: https://gist.github.com/jul/e9132abe8b5aeea573917191591fb90b
Credits: https://gist.github.com/jul
I migrated the code to python 3.6 and created a class!
'''

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from GUIClasses import JsonEditor

if __name__ == "__main__":
    pref = dict(padx=5, pady=5)
    root = tk.Tk(className="Minimal customized JSON editor")
    upper = tk.Frame(root, relief=tk.GROOVE)
    bottom = tk.Frame(root, relief=tk.GROOVE)

    text= JsonEditor(upper, width=100, height=40)
    #text= ScrolledText(upper, width=100, height=40)
    #text.bind("<Tab>", tab)
    res= ScrolledText(bottom, width=100,height=10)
    text.setError(res)

    validate = tk.Button(upper, text = "Validate", command=text.validate_json)
    indent = tk.Button(upper, text = "Indent", command=text.indent_json)


    res.pack(side=tk.LEFT,**pref)
    upper.pack(side=tk.TOP,**pref)
    bottom.pack(side=tk.BOTTOM, **pref)
    text.pack(side=tk.TOP,fill="y",**pref)
    validate.pack(side=tk.LEFT)
    indent.pack(side=tk.LEFT)
    text.init()
    root.mainloop()
