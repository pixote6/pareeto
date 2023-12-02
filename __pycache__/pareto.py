import statistics
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class pareto:
    def __init__(self, tab_control):
        self.tab_control = tab_control
        self.pareto1 = ttk.Frame(tab_control)

    def add_to_notebook(self):
        self.tab_control.add(self.pareto1, text="Análise de Pareto")
        self.tab_control.pack(expand=1, fill="both")  

        style = ttk.Style()
        style.configure("Custom.TLabel", background="#FFFF00")
        self.condition_label = ttk.Label(self.pareto1, text="                   Análise de Pareto:\n*Conforme: Preencher todos os parametros.\n*Não conforme: não digitar VALOR.\n                   Digite os valores:", style="Custom.TLabel", font=("Helvetica", 22, "bold"))
        self.condition_label.pack(pady=5)

        self.condition_label = tk.Label(self.pareto1, text="Condição:",font=("Helvetica", 14, "bold"), bg="#FFFF00")
        self.condition_label.pack(pady=5)
        self.condition_entry = tk.Entry(self.pareto1)
        self.condition_entry.pack(pady=5)

        self.occurrences_label = tk.Label(self.pareto1, text="Quantidade de ocorrencias:",font=("Helvetica", 14, "bold"), bg="#FFFF00")
        self.occurrences_label.pack(pady=5)
        self.occurrences_entry = tk.Entry(self.pareto1)
        self.occurrences_entry.pack(pady=5)

        self.value_label = tk.Label(self.pareto1, text="Valor da ocorrencia:",font=("Helvetica", 14, "bold"), bg="#FFFF00")
        self.value_label.pack(pady=5)
        self.value_entry = tk.Entry(self.pareto1)
        self.value_entry.pack(pady=5)

        self.pareto_button = tk.Button(self.pareto1, text="Adicionar Ocorrência", command=self.add_occurrence, width=20, height=2, bg="#FFFF00")
        self.pareto_button.pack(pady=10)

        self.occurrences_list = []

        self.load_button = tk.Button(self.pareto1, text="Carregar Dados", command=self.load_data, width=20, height=2, bg="#FFFF00")
        self.load_button.pack(pady=5)

        self.save_button = tk.Button(self.pareto1, text="Salvar Dados", command=self.save_data, width=20, height=2, bg="#FFFF00")
        self.save_button.pack(pady=5)

        self.analyze_button = tk.Button(self.pareto1, text="Realizar Análise de Pareto", command=self.perform_pareto_analysis, width=20, height=2, bg="#FFFF00")
        self.analyze_button.pack(pady=10)

        self.result_text = tk.Text(self.pareto1, width=80, height=25)
        self.result_text.pack(pady=10)

    def add_occurrence(self):
        condition = self.condition_entry.get()
        occurrences = self.occurrences_entry.get()
        value = self.value_entry.get()

        try:
            occurrences = int(occurrences)
        except ValueError:
            occurrences = 0  

        try:
            value = float(value)
        except ValueError:
            value = 0.0  

        self.occurrences_list.append((condition, occurrences, value))

        self.condition_entry.delete(0, tk.END)
        self.occurrences_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    self.occurrences_list = []
                    for line in lines[1:]: 
                        condition, occurrences, value = line.strip().split()
                        self.occurrences_list.append((condition, int(occurrences), float(value)))

                messagebox.showinfo("Sucesso", "Dados carregados com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write("Situação             Num Ocorrências       Valor da Ocorrência\n")
                for occurrence in self.occurrences_list:
                    condition, occurrences, value = occurrence
                    file.write(f"{condition.ljust(20)} {str(occurrences).ljust(20)} {str(value).ljust(20)}\n")

            messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")

    def perform_pareto_analysis(self):
        if not self.occurrences_list:
            messagebox.showwarning("Aviso", "Adicione pelo menos uma ocorrência para realizar a análise de Pareto.")
            return

        data = []
        total_occurrences = 0
        for occurrence in self.occurrences_list:
            condition, occurrences, _ = occurrence
            data.extend([condition] * occurrences)
            total_occurrences += occurrences

        pareto_data = pd.Series(data).value_counts().sort_values(ascending=False)
        pareto_data_percentage = pareto_data / total_occurrences * 100
        pareto_data_cumulative_percentage = pareto_data_percentage.cumsum()

        pareto_table = pd.DataFrame({
            'Situação': pareto_data.index,
            'Num Ocorrências': pareto_data.values,
            '% Contribuição': pareto_data_percentage.values,
            '% Contribuição Acumulada': pareto_data_cumulative_percentage.values
        })

        result_text_content = "Tabela de Análise de Pareto (Ordem Decrescente):\n"
        result_text_content += "{:<20} {:<15} {:<20} {:<25}\n".format(
            "Situação", "Num Ocorrências", "% Contribuição", "% Contribuição Acumulada"
        )

        for index, row in pareto_table.iterrows():
            result_text_content += "{:<20} {:<15} {:<20.2f} {:<25.2f}\n".format(
                row['Situação'], row['Num Ocorrências'], row['% Contribuição'], row['% Contribuição Acumulada']
            )

        result_text_content += "\nTotal de Ocorrências: {:<15}".format(total_occurrences)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text_content)

        fig = self.plot_pareto_chart(pareto_data)

        show_chart_button = tk.Button(self.pareto1, text="Exibir Gráfico ", command=lambda: self.show_pareto_chart_window(fig), width=30, height=2, bg="#FFFF00")
        show_chart_button.pack(pady=10)

    def show_pareto_chart_window(self, fig):
        chart_window = tk.Toplevel(self.pareto1)
        chart_window.title("Gráfico de Pareto")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, chart_window)
        toolbar.update()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_pareto_chart(self, pareto_data):
        fig, ax1 = plt.subplots()

        ax1.bar(pareto_data.index, pareto_data.values, color='blue', alpha=0.7, align='center')
        ax1.set_xlabel('Categorias')
        ax1.set_ylabel('Frequência', color='blue')
        ax1.tick_params('y', colors='blue')

        ax2 = ax1.twinx()
        ax2.plot(pareto_data.index, pareto_data.cumsum() / pareto_data.sum() * 100, color='red', marker='o')
        ax2.set_ylabel('% Acumulado', color='red')
        ax2.tick_params('y', colors='red')

        fig.tight_layout()

        return fig