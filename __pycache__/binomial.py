import tkinter as tk
from tkinter import ttk, font
import math
class binomial:
    def __init__(self, tab_control):
        self.tab_control = tab_control
        self.binomial = ttk.Frame(tab_control)

    def add_to_notebook(self):
        self.tab_control.add(self.binomial, text="Calculadora Binomial")
        style = ttk.Style()
        style.configure("Custom.TLabel", background="#FFFF00")
        self.condition_label = ttk.Label(self.binomial, text="Calculadora binomial:\n     Digite os valores:", style="Custom.TLabel", font=("Helvetica", 22, "bold"))
        self.condition_label.pack(pady=5)

        self.condition_label = ttk.Label(self.binomial, text="n:", style="Custom.TLabel", font=("Helvetica", 14, "bold"))
        self.condition_label.pack(pady=5)

        self.condition_n = ttk.Entry(self.binomial)
        self.condition_n.pack(pady=5)

        self.condition_label = ttk.Label(self.binomial, text="p:", style="Custom.TLabel", font=("Helvetica", 14, "bold"))
        self.condition_label.pack(pady=5)

        self.condition_p = ttk.Entry(self.binomial)
        self.condition_p.pack(pady=5)

        self.condition_label = ttk.Label(self.binomial, text="K:", style="Custom.TLabel", font=("Helvetica", 14, "bold"))
        self.condition_label.pack(pady=5)

        self.condition_k = ttk.Entry(self.binomial)
        self.condition_k.pack(pady=5)

        self.condition_k1 = ttk.Entry(self.binomial)
        self.condition_k1.pack(pady=5)

        self.calculate_button = tk.Button(self.binomial, text="Realizar Cálculo", command=self.calculate_binomial, width=20, height=2, bg="#FFFF00")
        self.calculate_button.pack(pady=10)

        self.result_table_text = tk.Text(self.binomial, width=80, height=25)
        self.result_table_text.pack(pady=10)

    def calculate_binomial(self):
        try:
            n = int(self.condition_n.get())
            k = int(self.condition_k.get())
            p = float(self.condition_p.get())
            k1 = int(self.condition_k1.get())

            if n < 0 or k < 0 or p < 0 or p > 1 or k1 < k:
                raise ValueError("Invalid input. Please enter valid values.")

            cumulative_result = 0
            for i in range(k, k1 + 1):
                result_i = self.calculate_binomial_coefficient(n, i) * (p ** i) * ((1 - p) ** (n - i)*100)
                cumulative_result += result_i

            self.result_table_text.insert(tk.END, f"Resultado do calculo binomial: {cumulative_result}%\n")
            self.result_table_text.tag_configure("custom_font", font=font.Font(family="Helvetica", size=16))
            self.result_table_text.tag_add("custom_font", "1.0", "end")
        except ValueError as e:
            self.result_table_text.insert(tk.END, f"Error: {str(e)}\n")

    @staticmethod
    def calculate_binomial_coefficient(n, k):
        return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
