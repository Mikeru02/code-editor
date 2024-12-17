from generator import *
from tkcode import CodeEditor
from tkinter import ttk

import tkinter as tk
import threading
import os

class App(tk.Tk):
    # Intitalization of tk
    def __init__(self) -> None:
        super().__init__()
        self.mutex = threading.Lock()
        self.code_name = "main"
        self.file = "samples/main.py"
        self.is_typing = False
        self.timer = None

        self.__configuration()
        self.__add_frames()
        self.__add_widgets()

        self.__check_updates()
        #self.log()

    # Configuration
    def __configuration(self) -> None:
        self.title("Code Editor")
        self.geometry("700x500")
        self.resizable(True, True)

    # Frames
    def __add_frames(self):
        self.main_frame = tk.Frame(self, background="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    # Widgets
    def __add_widgets(self) -> None:
        notebook = ttk.Notebook(self.main_frame)
        tab_1 = ttk.Frame(notebook)
        notebook.add(tab_1, text=self.code_name+'.py')
        notebook.pack(fill=tk.BOTH, expand=True)

        self.code_editor = CodeEditor(
            tab_1,
            language="python",
            highlighter="dracula",
            background="black",
            blockcursor=False,
        )
        
        self.code_editor.pack(fill=tk.BOTH, expand=True)
        self.code_editor.content= self.__load_file()
        self.code_editor.bind("<KeyRelease>", self.__on_key_release)

        termf = tk.Frame(self.main_frame, height=400, width=500)

        termf.pack(fill=tk.BOTH, expand=tk.YES)
        wid = termf.winfo_id()
        os.system('xterm -into %d -geometry 40x20 -sb &' % wid)

    def __load_file(self) -> str:
        try:
            with open(self.file, 'r') as code_file:
                content = code_file.read()
                print(f"{'-'*5}\n{repr(content)}\n{'-'*5}")
                return content
        except FileNotFoundError:
            print("File not found")
            return ""
        except Exception as err:
            print(f"Error reading file: {err}")
            return ""

    def __save_file(self, content:str) -> None:
        try:
            content = content.rstrip()
            with open(self.file, 'w') as code_file:
                code_file.write(content)
                #print("File Saved")
                self.is_typing = False
        except Exception as err:
            print(f"Error writing file: {err}")
    
    def __on_key_release(self,event=None) -> None:
        self.is_typing = True
        if self.timer:
            self.after_cancel(self.timer)
        
        self.timer = self.after(500, self.__change_text)

    def __change_text(self, event=None) -> None:
        self.__save_file(self.code_editor.content.rstrip())

    def __check_updates(self) -> None:
        if self.is_typing == False:
            self.code_editor.content = self.__load_file()
        self.after(1000, self.__check_updates)

    def log(self):
        print("DEBUG: ", self.is_typing)
        self.after(1000, self.log)

    # Main loop
    def run_app(self) -> None:
        self.mainloop()
