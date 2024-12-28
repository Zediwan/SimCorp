from src.gui.simulation_gui import SimulationGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()