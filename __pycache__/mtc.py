import statistics
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class mtc:
    def __init__(self, tab_control):
        self.tab_control = tab_control
        self.mtc1 = ttk.Frame(tab_control)

    def add_to_notebook(self):
        self.tab_control.add(self.mtc1, text="Medidas de Tendência Central")
        self.tab_control.pack(expand=1, fill="both")  

        style = ttk.Style()
        style.configure("Custom.TLabel", background="#FFFF00")
        self.condition_label = ttk.Label(self.mtc1, text="Medidas de Tendência Central:\n\n\n            Digite os valores:", style="Custom.TLabel", font=("Helvetica", 22, "bold"))
        self.condition_label.pack(pady=5)

        self.condition_label = ttk.Label(self.mtc1, text="Dados da amostra:", style="Custom.TLabel", font=("Helvetica", 14, "bold"))
        self.condition_label.pack(pady=5)

        self.condition_entry = tk.Entry(self.mtc1)
        self.condition_entry.pack(pady=5)

        self.insert_number_button = tk.Button(self.mtc1, text="Inserir Número", command=self.insert_number, width=20, height=2, bg="#FFFF00")
        self.insert_number_button.pack(pady=10)
    
        self.load_button = tk.Button(self.mtc1, text="Carregar Dados", command=self.load_data, width=20, height=2, bg="#FFFF00")
        self.load_button.pack(pady=5)

        self.save_button = tk.Button(self.mtc1, text="Salvar Dados", command=self.save_data, width=20, height=2, bg="#FFFF00")
        self.save_button.pack(pady=5)

        self.calculate_button = tk.Button(self.mtc1, text="Realizar Cálculo", command=self.calculate_measures, width=20, height=2, bg="#FFFF00")
        self.calculate_button.pack(pady=10)

        self.result_table_text = tk.Text(self.mtc1, width=80, height=25)
        self.result_table_text.pack(pady=10)

        self.inserted_numbers = []

    def insert_number(self):
        number_str = self.condition_entry.get()
        try:
            number = float(number_str)
            self.inserted_numbers.append(number)
        except ValueError:
            messagebox.showerror("Erro", "Insira um número válido.")
        self.condition_entry.delete(0, tk.END)

    def calculate_measures(self):
        if not self.inserted_numbers:
            messagebox.showwarning("Aviso", "Insira pelo menos um número para realizar os cálculos.")
            return

        mean = statistics.mean(self.inserted_numbers)
        mode = statistics.mode(self.inserted_numbers)
        median = statistics.median(self.inserted_numbers)
        quartiles = [np.percentile(self.inserted_numbers, q) for q in [25, 50, 75]]
        std_deviation = statistics.stdev(self.inserted_numbers)

        measures_table = f"""
        Tabela de Medidas de Tendência Central e Dispersão:
        Medida          Valor
        Média           {mean:.2f}
        Moda            {mode:.2f}
        Mediana         {median:.2f}
        1º Quartil      {quartiles[0]:.2f}
        2º Quartil      {quartiles[1]:.2f}
        3º Quartil      {quartiles[2]:.2f}
        Desvio Padrão   {std_deviation:.2f}
        """

        frequency_table = self.calculate_frequency_table()
        measures_table += "\n\nTabela de Distribuição de Frequência:\n"
        measures_table += frequency_table.to_string(index=False, float_format='%.2f')

        self.result_table_text.delete(1.0, tk.END)
        self.result_table_text.insert(tk.END, measures_table)

    def calculate_frequency_table(self):
        frequency_table = pd.DataFrame({
            'Intervalo': pd.cut(self.inserted_numbers, bins=10),
            'Ponto Médio': [(interval.left + interval.right) / 2 for interval in pd.cut(self.inserted_numbers, bins=10)],
            'Fi': 1
        })

        frequency_table = frequency_table.groupby('Intervalo').agg({'Ponto Médio': 'mean', 'Fi': 'count'}).reset_index()

        frequency_table['Fr'] = frequency_table['Fi'] / len(self.inserted_numbers)
        frequency_table['Fr(%)'] = frequency_table['Fr'] * 100
        frequency_table['Fr acumulado'] = frequency_table['Fr'].cumsum()

        return frequency_table

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                for number in self.inserted_numbers:
                    file.write(f"{number}\n")
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    self.inserted_numbers = [float(line.strip()) for line in lines]
                messagebox.showinfo("Sucesso", "Dados carregados com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
