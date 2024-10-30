import queue
from tkinter import ttk, BooleanVar
from GenerateHierarchicalNetwork import ravasz_barabasi_generator
import networkx as nx
import threading

class GenerateFrame(ttk.Frame):
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
        self.n_label = ttk.Label(self.param_widget, text="Number of nodes (n):")
        self.n_label.grid(row=0, column=0, sticky="e")
        self.n_entry = ttk.Entry(self.param_widget)
        self.n_entry.grid(row=0, column=1, sticky="w")

        self.m_label = ttk.Label(self.param_widget, text="Number of edges:")
        self.m_label.grid(row=1, column=0, sticky="e")
        self.m_entry = ttk.Entry(self.param_widget)
        self.m_entry.grid(row=1, column=1, sticky="w")

        self.levels_label = ttk.Label(self.param_widget, text="Hierarchical levels:")
        self.levels_label.grid(row=2, column=0, sticky="e")
        self.levels_entry = ttk.Entry(self.param_widget)
        self.levels_entry.grid(row=2, column=1, sticky="w")

        self.mu_label = ttk.Label(self.param_widget, text="Mixing parameter (mu):")
        self.mu_label.grid(row=3, column=0, sticky="e")
        self.mu_entry = ttk.Entry(self.param_widget)
        self.mu_entry.grid(row=3, column=1, sticky="w")

        self.tau1_label = ttk.Label(self.param_widget, text="Tau1 (degree distribution):")
        self.tau1_label.grid(row=1, column=2, sticky="e")
        self.tau1_entry = ttk.Entry(self.param_widget)
        self.tau1_entry.grid(row=1, column=3, sticky="w")

        self.tau2_label = ttk.Label(self.param_widget, text="Tau2 (community size distribution):")
        self.tau2_label.grid(row=2, column=2, sticky="e")
        self.tau2_entry = ttk.Entry(self.param_widget)
        self.tau2_entry.grid(row=2, column=3, sticky="w")

        self.min_clu_size_label = ttk.Label(self.param_widget, text="Minimum cluster size:")
        self.min_clu_size_label.grid(row=3, column=2, sticky="e")
        self.min_clu_size_entry = ttk.Entry(self.param_widget)
        self.min_clu_size_entry.grid(row=3, column=3, sticky="w")

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

        self.generate_button = ttk.Button(self.gen_widget, text="Generate", command=self.start_generation)
        self.generate_button.pack(ipadx=10, ipady=5)

        self.progress = ttk.Progressbar(self.gen_widget, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=5, ipadx=10, ipady=5)

        self.progress_queue = queue.Queue()
        self.after(100, self.process_queue)

    def start_generation(self):
        threading.Thread(target=self.generate_network).start()

    def update_progress(self, value):
        self.progress_queue.put(value)

    def process_queue(self):
        try:
            while True:
                value = self.progress_queue.get_nowait()
                self.progress['value'] = value
                self.update_idletasks()
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def generate_network(self):
        n = int(self.n_entry.get()) if self.n_entry.get() else 1000
        m = int(self.m_entry.get()) if self.m_entry.get() else 3
        levels = int(self.levels_entry.get()) if self.levels_entry.get() else 4
        mu = float(self.mu_entry.get()) if self.mu_entry.get() else 0.5
        tau1 = float(self.tau1_entry.get()) if self.tau1_entry.get() else 1.5
        tau2 = float(self.tau2_entry.get()) if self.tau2_entry.get() else 2.0
        min_cluster_size = int(self.min_clu_size_entry.get()) if self.min_clu_size_entry.get() else 2

        csv_file = "gen_graph_csv/" + self.file_entry.get() + ".csv" if self.file_entry.get() else "gen_graph_csv/lfr_graph.csv"
        graphml_file = self.file_entry.get() + ".graphml" if self.file_entry.get() else "graph.graphml"

        try:
            g = ravasz_barabasi_generator(n, m, levels, mu, tau1, tau2, min_cluster_size, progress_callback=self.update_progress)
            print("Network generation completed successfully")

            if self.save_csv.get():
                nx.write_edgelist(g, csv_file, delimiter=",", data=False)
                print(f"Network saved to {csv_file}")

            if self.save_graphml.get():
                nx.set_node_attributes(g, {n: ','.join(map(str, g.nodes[n]['community'])) for n in g.nodes()}, 'community')
                nx.write_graphml(g, "gen_graph_graphml/" + graphml_file)
                print(f"Network saved to {graphml_file}")

        except nx.ExceededMaxIterations as e:
            print(f"Error during network generation: {e}")
            print("Error: Could not assign communities; try increasing min_community or max_iters")