import tkinter as tk
from tkinter import ttk
from frames.generateFrame import GenerateFrame
from frames.analyzeFrame import AnalyzeFrame
from frames.viewFrame import ViewFrame

class mainApp:
    def __init__(self, root):
        root.title("Hierarchical communities")
        root.geometry("1050x650")

        # Configure the grid to expand with the window
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        notebook = ttk.Notebook(root)

        gen = GenerateFrame(notebook)
        anl = AnalyzeFrame(notebook)
        vie = ViewFrame(notebook)

        notebook.add(gen, text="Generate")
        notebook.add(anl, text="Analyze")
        notebook.add(vie, text="View")

        # Add the notebook to the root window using grid
        notebook.grid(row=0, column=0, sticky="nsew")

        root.bind("<Configure>", lambda event: self.adjust_tab_widths(notebook, event.width))

        style = ttk.Style()
        style.configure('TNotebook.Tab', anchor='center')

    def adjust_tab_widths(self, notebook, width):
        tab_width = width // 3
        style = ttk.Style()
        style.configure('TNotebook.Tab', width=tab_width)