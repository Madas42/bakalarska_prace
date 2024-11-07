import tkinter as tk
from tkinter import ttk, BooleanVar
import matplotlib.pyplot as plt
import networkx as nx
import threading
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import generation.generate_hierarchical_LFR as gen

class hierarchical_LFR_frame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_frames()

        self.parameters_unweighted_frame()

    def on_combobox_select(self, event):
        selected_value = self.graph_type_combobox.get()
        if selected_value in ["Weighted Undirected", "Weighted Directed"]:
            self.parameters_weighted_frame()
        if selected_value in ["Unweighted Undirected", "Unweighted Directed"]:
            self.parameters_unweighted_frame()

    def base_frames(self):
        # Frames
        self.param_widget = ttk.LabelFrame(self, text="Parameters")
        self.param_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.file_widget = ttk.LabelFrame(self, text="File")
        self.file_widget.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.gen_widget = ttk.LabelFrame(self, text="Generation")
        self.gen_widget.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # File frame
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

        # Generate frame
        self.graph_type_label = ttk.Label(self.gen_widget, text="LFR Graph type:")
        self.graph_type_label.grid(row=7, column=0, sticky="e")
        self.graph_type_combobox = ttk.Combobox(self.gen_widget, values=[
            "Weighted Undirected",
            "Weighted Directed",
            "Unweighted Undirected",
            "Unweighted Directed"
        ])
        self.graph_type_combobox.grid(row=8, column=0, sticky="w")
        self.graph_type_combobox.current(3)
        self.graph_type_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        self.generate_button = ttk.Button(self.gen_widget, text="Generate", command=self.start_generation)
        self.generate_button.grid(row=9, column=0, sticky="nsew")

        # Draw canvas
        self.graph_canvas = tk.Canvas(self, width=200, height=200)
        self.graph_canvas.grid(row=0, column=4, rowspan=8, columnspan=2)

    def parameters_weighted_frame(self):
        print("Prameters for weighted frame")
        for widget in self.param_widget.winfo_children():
            widget.destroy()
        self.graph_canvas.destroy()
        self.canvas_agg = None

        self.num_nodes_label = ttk.Label(self.param_widget, text="Number of nodes (n):")
        self.num_nodes_label.grid(row=0, column=0, sticky="e")
        self.num_nodes_entry = ttk.Entry(self.param_widget)
        self.num_nodes_entry.grid(row=0, column=1, sticky="w")
        self.num_nodes_entry.insert(0, "1000")

        self.average_k_label = ttk.Label(self.param_widget, text="Average degree (k):")
        self.average_k_label.grid(row=1, column=0, sticky="e")
        self.average_k_entry = ttk.Entry(self.param_widget)
        self.average_k_entry.grid(row=1, column=1, sticky="w")
        self.average_k_entry.insert(0, "10")

        self.max_degree_label = ttk.Label(self.param_widget, text="Maximal degree:")
        self.max_degree_label.grid(row=2, column=0, sticky="e")
        self.max_degree_entry = ttk.Entry(self.param_widget)
        self.max_degree_entry.grid(row=2, column=1, sticky="w")
        self.max_degree_entry.insert(0, "20")

        self.mut_label = ttk.Label(self.param_widget, text="MUT:")
        self.mut_label.grid(row=3, column=0, sticky="e")
        self.mut_entry = ttk.Entry(self.param_widget)
        self.mut_entry.grid(row=3, column=1, sticky="w")
        self.mut_entry.insert(0, "0.3")

        self.muw_label = ttk.Label(self.param_widget, text="MUW:")
        self.muw_label.grid(row=4, column=0, sticky="e")
        self.muw_entry = ttk.Entry(self.param_widget)
        self.muw_entry.grid(row=4, column=1, sticky="w")
        self.muw_entry.insert(0, "0.1")

        self.com_size_min_label = ttk.Label(self.param_widget, text="Minimum community size:")
        self.com_size_min_label.grid(row=5, column=0, sticky="e")
        self.com_size_min_entry = ttk.Entry(self.param_widget)
        self.com_size_min_entry.grid(row=5, column=1, sticky="w")
        self.com_size_min_entry.insert(0, "10")

        self.com_size_max_label = ttk.Label(self.param_widget, text="Maximum community size:")
        self.com_size_max_label.grid(row=6, column=0, sticky="e")
        self.com_size_max_entry = ttk.Entry(self.param_widget)
        self.com_size_max_entry.grid(row=6, column=1, sticky="w")
        self.com_size_max_entry.insert(0, "30")

        self.seed_label = ttk.Label(self.param_widget, text="Seed:")
        self.seed_label.grid(row=7, column=0, sticky="e")
        self.seed_entry = ttk.Entry(self.param_widget)
        self.seed_entry.grid(row=7, column=1, sticky="w")
        self.seed_entry.insert(0, "42")

        # Draw canvas
        self.graph_canvas = tk.Canvas(self, width=550, height=550)
        self.graph_canvas.grid(row=0, column=4, rowspan=8, columnspan=2, sticky="nsew")

    def parameters_unweighted_frame(self):
        for widget in self.param_widget.winfo_children():
            widget.destroy()
        self.graph_canvas.destroy()
        self.canvas_agg = None

        self.num_nodes_label = ttk.Label(self.param_widget, text="Number of nodes (n):")
        self.num_nodes_label.grid(row=0, column=0, sticky="e")
        self.num_nodes_entry = ttk.Entry(self.param_widget)
        self.num_nodes_entry.grid(row=0, column=1, sticky="w")
        self.num_nodes_entry.insert(0, "1000")

        self.average_k_label = ttk.Label(self.param_widget, text="Average degree (k):")
        self.average_k_label.grid(row=1, column=0, sticky="e")
        self.average_k_entry = ttk.Entry(self.param_widget)
        self.average_k_entry.grid(row=1, column=1, sticky="w")
        self.average_k_entry.insert(0, "10")

        self.max_degree_label = ttk.Label(self.param_widget, text="Maximal degree:")
        self.max_degree_label.grid(row=2, column=0, sticky="e")
        self.max_degree_entry = ttk.Entry(self.param_widget)
        self.max_degree_entry.grid(row=2, column=1, sticky="w")
        self.max_degree_entry.insert(0, "20")

        self.mu_label = ttk.Label(self.param_widget, text="MU:")
        self.mu_label.grid(row=3, column=0, sticky="e")
        self.mu_entry = ttk.Entry(self.param_widget)
        self.mu_entry.grid(row=3, column=1, sticky="w")
        self.mu_entry.insert(0, "0.1")

        self.com_size_min_label = ttk.Label(self.param_widget, text="Minimum community size:")
        self.com_size_min_label.grid(row=4, column=0, sticky="e")
        self.com_size_min_entry = ttk.Entry(self.param_widget)
        self.com_size_min_entry.grid(row=4, column=1, sticky="w")
        self.com_size_min_entry.insert(0, "10")

        self.com_size_max_label = ttk.Label(self.param_widget, text="Maximum community size:")
        self.com_size_max_label.grid(row=5, column=0, sticky="e")
        self.com_size_max_entry = ttk.Entry(self.param_widget)
        self.com_size_max_entry.grid(row=5, column=1, sticky="w")
        self.com_size_max_entry.insert(0, "30")

        self.seed_label = ttk.Label(self.param_widget, text="Seed:")
        self.seed_label.grid(row=6, column=0, sticky="e")
        self.seed_entry = ttk.Entry(self.param_widget)
        self.seed_entry.grid(row=6, column=1, sticky="w")
        self.seed_entry.insert(0, "42")

        # Draw canvas
        self.graph_canvas = tk.Canvas(self, width=550, height=550)
        self.graph_canvas.grid(row=0, column=4, rowspan=8, columnspan=2, sticky="nsew")

    def start_generation(self):
        threading.Thread(target=self.generate_network).start()

    def generate_network(self):
        num_nodes = int(self.num_nodes_entry.get())
        average_k = float(self.average_k_entry.get())
        max_degree = int(self.max_degree_entry.get())
        com_size_min = int(self.com_size_min_entry.get())
        com_size_max = int(self.com_size_max_entry.get())
        seed = int(self.seed_entry.get())

        try:
            if self.graph_type_combobox.get() == "Weighted Undirected":
                mut = float(self.mut_entry.get())
                muw = float(self.muw_entry.get())
                g = gen.generate_weighted_undirected_lfr(num_nodes, average_k, max_degree, mut, muw, com_size_min, com_size_max, seed)
            if self.graph_type_combobox.get() == "Weighted Directed":
                mut = float(self.mut_entry.get())
                muw = float(self.muw_entry.get())
                g = gen.generate_weighted_directed_lfr(num_nodes, average_k, max_degree, mut, muw, com_size_min, com_size_max, seed)
            if self.graph_type_combobox.get() == "Unweighted Undirected":
                mu = float(self.mu_entry.get())
                g = gen.generate_unweighted_undirected_lfr(num_nodes, average_k, max_degree, mu, com_size_min, com_size_max, seed)
            if self.graph_type_combobox.get() == "Unweighted Directed":
                mu = float(self.mu_entry.get())
                g = gen.generate_unweighted_directed_lfr(num_nodes, average_k, max_degree, mu, com_size_min, com_size_max, seed)

            #Graph draw
            pos = nx.kamada_kawai_layout(g)

            # Extract community information
            communities = nx.get_node_attributes(g, 'communities')
            unique_communities = set(communities.values())
            community_colors = {community: plt.cm.tab20(i / len(unique_communities)) for i, community in
                                enumerate(unique_communities)}
            node_colors = [community_colors[communities[node]] for node in g.nodes()]

            fig, ax = plt.subplots(figsize=(5.5, 5.5))
            nx.draw(g, pos, ax=ax, with_labels=False, node_color=node_colors, edge_color="gray")
            self.canvas_agg = FigureCanvasTkAgg(fig, self.graph_canvas)
            self.canvas_agg.draw()
            self.canvas_agg.get_tk_widget().grid(row=0, column=4, rowspan=8, columnspan=2, sticky="nsew")


            # Save graph
            csv_file = "gen_graph_csv/" + self.file_entry.get() + ".csv" if self.file_entry.get() else "gen_graph_csv/lfr_graph.csv"
            graphml_file = self.file_entry.get() + ".graphml" if self.file_entry.get() else "graph.graphml"

            if self.save_csv.get():
                nx.write_edgelist(g, csv_file, delimiter=",", data=False)
                print(f"Network saved to {csv_file}")

            if self.save_graphml.get():
                nx.write_graphml(g, "gen_graph_graphml/" + graphml_file)
                print(f"Network saved to {graphml_file}")


        except nx.ExceededMaxIterations as e:
            print(f"Error during network generation: {e}")
            print("Error: Could not generate network due to maximum number of iterations reached")
