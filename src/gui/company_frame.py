import tkinter as tk
from tkinter import ttk
from ..company import Company

class CompanyFrame(ttk.Frame):
    def __init__(self, parent, company: Company):
        super().__init__(parent, padding="10")
        self.company = company

        self.name_label = ttk.Label(self, text=f"Name: {self.company.name}")
        self.name_label.pack(anchor=tk.W)
        
        if self.company.founder:
            self.founder_label = ttk.Label(self, text=f"Founder: {self.company.founder.name}")
            self.founder_label.pack(anchor=tk.W)
        else:
            self.founder_label = ttk.Label(self, text="Founder: None")
            self.founder_label.pack(anchor=tk.W)

        self.employees_label = ttk.Label(self, text=f"Employees: {len(self.company.employees)}")
        self.employees_label.pack(anchor=tk.W)
        
        self.money_label = ttk.Label(self, text=f"Money: ${self.company.money:.2f}")
        self.money_label.pack(anchor=tk.W)
        
        self.products_label = ttk.Label(self, text=f"Products: {self.company.num_products}")
        self.products_label.pack(anchor=tk.W)

    def update(self):
        self.name_label.config(text=f"Name: {self.company.name}")
        self.employees_label.config(text=f"Employees: {len(self.company.employees)}")
        self.money_label.config(text=f"Money: ${self.company.money:.2f}")
        self.products_label.config(text=f"Products: {self.company.num_products}")