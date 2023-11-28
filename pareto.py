import statistics
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análise de Dados")
        self.root.configure(bg="#FFFFCC") 
        style = ttk.Style()
        style.configure("TFrame", background='#FFFFCC')
        style.configure("TNotebook", background="#FFFFCC")  # Cor de fundo da aba
        style.configure("TNotebook.Tab", background="#FFFFCC")  # Cor de fundo do texto da aba




        self.tabControl = ttk.Notebook(root)
        self.pareto_tab = ttk.Frame(self.tabControl)
        self.central_tendency_tab = ttk.Frame(self.tabControl)
        self.binomial_tab = ttk.Frame(self.tabControl)
        self.normal_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.pareto_tab, text="Análise de Pareto")
        self.tabControl.add(self.central_tendency_tab, text="Medidas de Tendência Central")
        self.tabControl.add(self.binomial_tab, text="Calculadora Binomial")
        

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

        self.pareto_button = tk.Button(self.pareto_tab, text="Adicionar Ocorrência", command=self.add_occurrence, width=20, height=2, bg="#FFFF00")
        self.pareto_button.pack(pady=10)

        self.occurrences_list = []

        self.load_button = tk.Button(self.pareto_tab, text="Carregar Dados", command=self.load_data, width=20, height=2, bg="#FFFF00")
        self.load_button.pack(pady=5)

        self.save_button = tk.Button(self.pareto_tab, text="Salvar Dados", command=self.save_data, width=20, height=2, bg="#FFFF00")
        self.save_button.pack(pady=5)

        self.analyze_button = tk.Button(self.pareto_tab, text="Realizar Análise de Pareto", command=self.perform_pareto_analysis, width=20, height=2, bg="#FFFF00")
        self.analyze_button.pack(pady=10)

        self.result_text = tk.Text(self.pareto_tab, width=80, height=10)
        self.result_text.pack(pady=10)

        self.pareto_chart_frame = ttk.Frame(self.pareto_tab)
        self.pareto_chart_frame.pack(pady=10)
#        


        self.condition_label = tk.Label(self.central_tendency_tab, text="Digite os números:")
        self.condition_label.pack(pady=5)

        self.condition_entry = tk.Entry(self.central_tendency_tab)
        self.condition_entry.pack(pady=5)

        self.insert_number_button = tk.Button(self.central_tendency_tab, text="Inserir Número", command=self.insert_number, width=20, height=2, bg="#FFFF00")
        self.insert_number_button.pack(pady=10)

        self.calculate_button = tk.Button(self.central_tendency_tab, text="Realizar Cálculo", command=self.calculate_measures, width=20, height=2, bg="#FFFF00")
        self.calculate_button.pack(pady=10)

        self.result_table_text = tk.Text(self.central_tendency_tab, width=80, height=10)
        self.result_table_text.pack(pady=10)

        # Lista para armazenar os números inseridos
        self.inserted_numbers = []





    def insert_number(self):
        # Obter o número inserido
        number_str = self.quantitative_data_entry.get()

        # Converter o número para float
        try:
            number = float(number_str)
            # Adicionar o número à lista
            self.inserted_numbers.append(number)
        except ValueError:
            messagebox.showerror("Erro", "Insira um número válido.")

        # Limpar o campo de entrada
        self.quantitative_data_entry.delete(0, tk.END)

    def calculate_measures(self):
        # Verificar se há números para calcular
        if not self.inserted_numbers:
            messagebox.showwarning("Aviso", "Insira pelo menos um número para realizar os cálculos.")
            return

        # Calcular medidas de tendência central e dispersão
        mean = statistics.mean(self.inserted_numbers)
        mode = statistics.mode(self.inserted_numbers)
        median = statistics.median(self.inserted_numbers)
        
        # Calcular quartis
        quartiles = [statistics.quantiles(self.inserted_numbers, n) for n in [0.25, 0.5, 0.75]]

        # Calcular desvio padrão
        std_deviation = statistics.stdev(self.inserted_numbers)

        # Criar tabela de medidas
        measures_table = pd.DataFrame({
            'Medida': ['Média', 'Moda', 'Mediana', '1º Quartil', '2º Quartil', '3º Quartil', 'Desvio Padrão'],
            'Valor': [mean, mode, median] + quartiles + [std_deviation]
        })

        # Exibir os resultados na janela de rolagem de texto
        result_text_content = "Tabela de Medidas de Tendência Central e Dispersão:\n"
        result_text_content += "{:<15} {:<15}\n".format("Medida", "Valor")

        for index, row in measures_table.iterrows():
            result_text_content += "{:<15} {:<15.2f}\n".format(row['Medida'], row['Valor'])

        self.result_table_text.delete(1.0, tk.END)
        self.result_table_text.insert(tk.END, result_text_content)    
       
    def add_occurrence(self):
        # Obter as condições, quantidade de ocorrências e valor da ocorrência
        condition = self.condition_entry.get()
        occurrences = self.occurrences_entry.get()
        value = self.value_entry.get()

        # Converter a quantidade de ocorrências e valor para números
        try:
            occurrences = int(occurrences)
        except ValueError:
            occurrences = 0  # Defina para 0 se não for um número

        try:
            value = float(value)
        except ValueError:
            value = 0.0  # Defina para 0.0 se não for um número

        # Adicionar a ocorrência à lista
        self.occurrences_list.append((condition, occurrences, value))

        # Limpar os campos de entrada
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
                    for line in lines[1:]:  # Ignorar a primeira e última linhas (cabeçalho e total)
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
                    # Alteração: Adicionar um espaço extra para garantir a formatação correta
                    file.write(f"{condition.ljust(20)} {str(occurrences).ljust(20)} {str(value).ljust(20)}\n")

            messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")

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

        # Adicionar o gráfico à interface gráfica usando NavigationToolbar2Tk
        canvas = FigureCanvasTkAgg(fig, master=self.pareto_chart_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Adicionar barra de navegação
        toolbar = NavigationToolbar2Tk(canvas, self.pareto_chart_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



    def insert_number(self):
        # Obter o número inserido
        number_str = self.condition_entry.get()

        # Converter o número para float
        try:
            number = float(number_str)
            # Adicionar o número à lista
            self.inserted_numbers.append(number)
        except ValueError:
            messagebox.showerror("Erro", "Insira um número válido.")

        # Limpar o campo de entrada
        self.condition_entry.delete(0, tk.END)

    def calculate_measures(self):
        # Verificar se há números para calcular
        if not self.inserted_numbers:
            messagebox.showwarning("Aviso", "Insira pelo menos um número para realizar os cálculos.")
            return

        # Calcular medidas de tendência central e dispersão
        mean = statistics.mean(self.inserted_numbers)
        mode = statistics.mode(self.inserted_numbers)
        median = statistics.median(self.inserted_numbers)

        # Calcular quartis
        quartiles = [np.percentile(self.inserted_numbers, q) for q in [25, 50, 75]]


        # Calcular desvio padrão
        std_deviation = statistics.stdev(self.inserted_numbers)

        # Criar tabela de medidas
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

        # Exibir os resultados na janela de rolagem de texto
        self.result_table_text.delete(1.0, tk.END)
        self.result_table_text.insert(tk.END, measures_table)
