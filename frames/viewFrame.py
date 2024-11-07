import tkinter as tk
from tkinter import ttk
import graph_tool.all as gt

class ViewFrame(ttk.Frame):
    def __init__(self, parent, graph=None):
        super().__init__(parent)
        self.graph = graph
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        viel = ttk.Label(self, text="View Community")
        viel.grid(row=0, column=0, sticky="nsew")