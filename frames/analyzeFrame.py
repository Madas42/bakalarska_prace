import tkinter as tk
from tkinter import ttk

class AnalyzeFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        anll = ttk.Label(self, text="Analyze Community")
        anll.grid(row=0, column=0, sticky="nsew")