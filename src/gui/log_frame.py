import tkinter as tk
from tkinter import ttk

class LogFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.text_widget = tk.Text(self, state='disabled', wrap='word')
        self.text_widget.pack(fill=tk.BOTH, expand=True)

    def get_text_widget(self):
        return self.text_widget