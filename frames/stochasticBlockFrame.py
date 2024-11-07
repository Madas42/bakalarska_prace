import tkinter as tk
from tkinter import ttk, BooleanVar
import threading
import networkx as nx
# from generation.generateStochasticBlock import generate_stochastic_block

#TODO repair generation of stochastic block model

class stochasticBlockFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Frames
        self.param_widget = ttk.LabelFrame(self, text="Parameters")
        self.param_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.file_widget = ttk.LabelFrame(self, text="File")
        self.file_widget.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.gen_widget = ttk.LabelFrame(self, text="Generation")
        self.gen_widget.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Create input fields for LFR parameters
        self.num_nodes_label = ttk.Label(self.param_widget, text="Number of nodes (n):")
        self.num_nodes_label.grid(row=0, column=0, sticky="e")
        self.num_nodes_entry = ttk.Entry(self.param_widget)
        self.num_nodes_entry.grid(row=0, column=1, sticky="w")

        self.num_groups_label = ttk.Label(self.param_widget, text="Number of groups:")
        self.num_groups_label.grid(row=1, column=0, sticky="e")
        self.num_groups_entry = ttk.Entry(self.param_widget)
        self.num_groups_entry.grid(row=1, column=1, sticky="w")

        self.seed_label = ttk.Label(self.param_widget, text="Hierarchical levels:")
        self.seed_label.grid(row=2, column=0, sticky="e")
        self.seed_entry = ttk.Entry(self.param_widget)
        self.seed_entry.grid(row=2, column=1, sticky="w")

        self.file_label = ttk.Label(self.file_widget, text="File name:")
        self.file_label.grid(row=5, column=0, sticky="e")
        self.file_entry = ttk.Entry(self.file_widget)
        self.file_entry.grid(row=5, column=1, sticky="w")

        self.save_csv = BooleanVar()
        self.save_graphml = BooleanVar()
        self.csv_checkbutton = ttk.Checkbutton(self.file_widget, text="Save as CSV", variable=self.save_csv)
        self.csv_checkbutton.grid(row=5, column=2, padx=10, sticky="w")
        self.graphml_checkbutton = ttk.Checkbutton(self.file_widget, text="Save as GraphML", variable=self.save_graphml)
        self.graphml_checkbutton.grid(row=6, column=2, padx=10, sticky="w")

        # self.generate_button = ttk.Button(self.gen_widget, text="Generate", command=self.start_generation)
        # self.generate_button.pack(ipadx=10, ipady=5)

    def start_generation(self):
        threading.Thread(target=self.generate_network).start()

    def generate_network(self):
        num_nodes = int(self.num_nodes_entry.get()) if self.num_nodes_entry.get() else 1000
        num_groups = int(self.num_groups_entry.get()) if self.num_groups_entry.get() else 3
        seed = int(self.seed_entry.get()) if self.seed_entry.get() else 42

        csv_file = "gen_graph_csv/" + self.file_entry.get() + ".csv" if self.file_entry.get() else "gen_graph_csv/lfr_graph.csv"
        graphml_file = self.file_entry.get() + ".graphml" if self.file_entry.get() else "graph.graphml"

        try:
            g = generate_stochastic_block(num_nodes, num_groups, seed)
            print("Network generation completed successfully")

            if self.save_csv.get():
                nx.write_edgelist(g, csv_file, delimiter=",", data=False)
                print(f"Network saved to {csv_file}")

            if self.save_graphml.get():
                nx.write_graphml(g, "gen_graph_graphml/" + graphml_file)
                print(f"Network saved to {graphml_file}")

        except nx.ExceededMaxIterations as e:
            print(f"Error during network generation: {e}")
            print("Error: Could not generate network due to maximum number of iterations reached")
