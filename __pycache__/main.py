import tkinter as tk
from tkinter import ttk
from pareto import pareto
from mtc import mtc
from binomial import binomial

class WelcomeTab:
    def __init__(self, tab_control):
        self.tab_control = tab_control
        self.bemvindo_tab = ttk.Frame(tab_control)

    def add_to_notebook(self):
        
        self.tab_control.add(self.bemvindo_tab, text="Boas-vindas")
        benvendo_label = tk.Label(self.bemvindo_tab, text="Calculadora estátistica\n\n\n\n\n\nProjeto de estátistica aplicada.\n\n\n\n\n\n\n\n Desenvolvido por:\nLarissa Matssuda\nSuellen Donato\nRoger Santos.\n\n\n\n\n\n\n\n\n\n", font=("Helvetica", 22, "bold"), bg="#FFFF00")
        benvendo_label.pack(pady=10)

class Programa:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Análise de Dados")
        self.root.configure(bg="#FFFFCC")
        self.root.geometry("800x1000")
        style = ttk.Style()
        style.configure("TFrame", background='#FFFFCC')
        style.configure("TNotebook.Tab", background="#FFFFCC")

        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.pack(expand=1, fill="both")

        welcome_tab = WelcomeTab(self.tabControl)
        welcome_tab.add_to_notebook()
        
        pareto1 = pareto(self.tabControl)
        pareto1.add_to_notebook()

        mtc1 = mtc(self.tabControl)
        mtc1.add_to_notebook()

        binomial1 = binomial(self.tabControl)
        binomial1.add_to_notebook()

    def run(self):
        self.root.mainloop()
app_instance = Programa()
app_instance.run()