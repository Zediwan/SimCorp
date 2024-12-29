import tkinter as tk
from tkinter import ttk
from ..simulation import Simulation
from ..helper.logger import Logger
from .company_frame import CompanyFrame
from .log_frame import LogFrame

class SimulationGUI:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Simulation GUI")
        
        self.create_widgets()
        self.update_gui()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.company_frame = ttk.Frame(self.main_frame, padding="10")
        self.company_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.log_frame = LogFrame(self.main_frame)
        self.log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.logger = Logger(__name__, self.log_frame.get_text_widget())
        self.simulation = Simulation(logger=self.logger)

        # Create a canvas and a scrollbar for the company frames
        self.canvas = tk.Canvas(self.company_frame)
        self.scrollbar = ttk.Scrollbar(self.company_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.company_frames: list[CompanyFrame] = []
        for company in self.simulation.companies:
            company_frame = CompanyFrame(self.scrollable_frame, company)
            company_frame.pack(fill=tk.BOTH, expand=True)
            self.company_frames.append(company_frame)

    def update_gui(self):
        self.simulation.run()
        
        for company in self.simulation.new_companies:
            company_frame = CompanyFrame(self.scrollable_frame, company)
            company_frame.pack(fill=tk.BOTH, expand=True)
            self.company_frames.append(company_frame)
            self.simulation.new_companies.remove(company)

        for company_frame in self.company_frames:
            if company_frame.company.money <= 0:
                self.company_frames.remove(company_frame)
                company_frame.destroy()
            else:
                company_frame.update()
        
        self.root.after(1, self.update_gui)
