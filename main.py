import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análise de Dados")

        self.tabControl = ttk.Notebook(root)
        self.pareto_tab = ttk.Frame(self.tabControl)
        self.central_tendency_tab = ttk.Frame(self.tabControl)
        self.binomial_tab = ttk.Frame(self.tabControl)
        self.normal_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.pareto_tab, text="Análise de Pareto")
        self.tabControl.add(self.central_tendency_tab, text="Medidas de Tendência Central")
        self.tabControl.add(self.binomial_tab, text="Calculadora Binomial")
        self.tabControl.add(self.normal_tab, text="Calculadora Normal")

        self.tabControl.pack(expand=1, fill="both")

        # Configurar widgets para a aba de Análise de Pareto
        self.condition_label = tk.Label(self.pareto_tab, text="Condição:")
        self.condition_label.pack(pady=5)
        self.condition_entry = tk.Entry(self.pareto_tab)
        self.condition_entry.pack(pady=5)

        self.occurrences_label = tk.Label(self.pareto_tab, text="Quantidade de Ocorrências:")
        self.occurrences_label.pack(pady=5)
        self.occurrences_entry = tk.Entry(self.pareto_tab)
        self.occurrences_entry.pack(pady=5)

        self.value_label = tk.Label(self.pareto_tab, text="Valor da Ocorrência:")
        self.value_label.pack(pady=5)
        self.value_entry = tk.Entry(self.pareto_tab)
        self.value_entry.pack(pady=5)

        self.pareto_button = tk.Button(self.pareto_tab, text="Adicionar Ocorrência", command=self.add_occurrence)
        self.pareto_button.pack(pady=10)

        self.occurrences_list = []

        self.analyze_button = tk.Button(self.pareto_tab, text="Realizar Análise de Pareto", command=self.perform_pareto_analysis)
        self.analyze_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(self.pareto_tab, width=80, height=20)
        self.result_text.pack(pady=10)

        self.pareto_chart_frame = ttk.Frame(self.pareto_tab)
        self.pareto_chart_frame.pack(pady=10)

    def add_occurrence(self):
        # Obter as condições, quantidade de ocorrências e valor da ocorrência
        condition = self.condition_entry.get()
        occurrences = self.occurrences_entry.get()
        value = self.value_entry.get()

        # Verificar se todos os campos estão preenchidos
        if not condition or not occurrences or not value:
            messagebox.showwarning("Aviso", "Preencha todos os campos para adicionar a ocorrência.")
            return

        # Converter a quantidade de ocorrências e valor para números
        try:
            occurrences = int(occurrences)
            value = float(value)
        except ValueError:
            messagebox.showwarning("Aviso", "A quantidade de ocorrências e o valor da ocorrência devem ser números.")
            return

        # Adicionar a ocorrência à lista
        self.occurrences_list.append((condition, occurrences, value))

        # Limpar os campos de entrada
        self.condition_entry.delete(0, tk.END)
        self.occurrences_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def perform_pareto_analysis(self):
        # Verificar se há ocorrências para análise
        if not self.occurrences_list:
            messagebox.showwarning("Aviso", "Adicione pelo menos uma ocorrência para realizar a análise de Pareto.")
            return

        # Gerar dados com base nas informações inseridas
        data = []
        total_occurrences = 0
        for occurrence in self.occurrences_list:
            condition, occurrences, _ = occurrence
            data.extend([condition] * occurrences)
            total_occurrences += occurrences

        pareto_data = pd.Series(data).value_counts().sort_values(ascending=False)
        pareto_data_percentage = pareto_data / total_occurrences * 100
        pareto_data_cumulative_percentage = pareto_data_percentage.cumsum()

        # Criar tabela de análise de Pareto
        pareto_table = pd.DataFrame({
            'Situação': pareto_data.index,
            'Num Ocorrências': pareto_data.values,
            '% Contribuição': pareto_data_percentage.values,
            '% Contribuição Acumulada': pareto_data_cumulative_percentage.values
        })

        # Exibir os resultados na janela de rolagem de texto
        self.result_text.delete(1.0, tk.END)  # Limpar o conteúdo anterior
        self.result_text.insert(tk.END, "Tabela de Análise de Pareto (Ordem Decrescente):\n")
        self.result_text.insert(tk.END, "{:<20} {:<15} {:<15} {:<15}\n".format(
            "Situação", "Num Ocorrências", "% Contribuição", "% Contribuição Acumulada"
        ))

        for index, row in pareto_table.iterrows():
            self.result_text.insert(tk.END, "{:<20} {:<15} {:<20.2f} {:<25.2f}\n".format(
                row['Situação'], row['Num Ocorrências'], row['% Contribuição'], row['% Contribuição Acumulada']
            ))

        self.result_text.insert(tk.END, "\nTotal de Ocorrências: {:<15}".format(total_occurrences))

        # Opcional: Gráfico de Pareto
        self.plot_pareto_chart(pareto_data)

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

        # Adicionar o gráfico à interface gráfica
        canvas = FigureCanvasTkAgg(fig, master=self.pareto_chart_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()