import tkinter as tk

class ButtonGenerator(tk.Button):
    def __init__(self, root) -> None:
        self.root = root
        self.button = None
    
    def add_text(self, text:str) -> object:
        self.text = text
        return self

    def add_command(self, command:str) -> object:
        self.command = command
        return self
    
    def set_position(self, row:int, column:int) -> object:
        self.row = row
        self.column = column
        return self
    
    def build(self) -> object:
        self.button = tk.Button(self.root, text=self.text, command=self.command)
        self.button.grid(row=self.row, column=self.column)
        return self.button