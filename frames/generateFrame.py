import tkinter as tk
from tkinter import ttk, BooleanVar
from frames.stochasticBlockFrame import stochasticBlockFrame
from frames.hierarchical_LFR_frame import hierarchical_LFR_frame

class GenerateFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        genNotebook = ttk.Notebook(self)

        LFR_frame = hierarchical_LFR_frame(genNotebook)
        stochasticFrame = stochasticBlockFrame(genNotebook)

        genNotebook.add(LFR_frame, text="Hierarchical LFR")
        genNotebook.add(stochasticFrame, text="Stochastic Block")

        genNotebook.pack(expand=1, fill="both")

        parent.bind("<Configure>", lambda event: self.adjust_tab_widths(genNotebook, event.width))

        style = ttk.Style()
        style.configure('TNotebook.Tab', anchor='center')

    def adjust_tab_widths(self, notebook, width):
        tab_width = width // 2
        style = ttk.Style()
        style.configure('TNotebook.Tab', width=tab_width)