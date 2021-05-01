import tkinter as tk
import page_list

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        welcome_label = tk.Label(self, text = "Você quer prever o valor para quantos dias?", font = ("Verdana", 35))
        welcome_label.pack(fill=tk.X, pady=30)

        config_button = tk.Button(
            self,
            text = "1 dia",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : controller.show_frame(page_list.CHOOSE_DATE_PAGE)
        )
        config_button.pack(pady=50)

        config_button = tk.Button(
            self,
            text = "Período de dias",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : controller.show_frame(page_list.CHOOSE_INTERVAL_PAGE)
        )
        config_button.pack(pady=50)

        back_button = tk.Button(
            self,
            text = "Voltar",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : controller.show_frame(page_list.TRAINING_PAGE)
        )
        back_button.pack(pady=50)
