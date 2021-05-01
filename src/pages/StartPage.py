import tkinter as tk
import page_list
from Layer import (
    DEFAULT_DAYS,
    DEFAULT_OPTIMIZER,
    DEFAULT_LOSS,
    DEFAULT_EPOCHS,
    DEFAULT_BATCH_SIZE,
    DEFAULT_LAYERS
)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        FONT = ("Verdana", 16)

        welcome_label = tk.Label(self, text ="Olá, Bem-vindo ao NextValue!", font = ("Verdana", 35))
        welcome_label.pack(fill=tk.X, pady=70)

        info_label1 = tk.Label(self, text ="Aqui você poderá usar técnicas de DeepLearning para", font = FONT)
        info_label1.pack(fill=tk.X, pady=5)
        info_label2 = tk.Label(self, text ="tentar prever o valor das criptomoedas.", font = FONT)
        info_label2.pack(fill=tk.X, pady=5)
        
        training_label = tk.Label(self, text ="Primeiro será necessário treinar uma rede neural.", font = FONT)
        training_label.pack(fill=tk.X, pady=50)

        question_label1 = tk.Label(self, text ="Você deseja usar as configurações padrões ou", font = FONT)
        question_label1.pack(fill=tk.X, pady=5)
        question_label2 = tk.Label(self, text ="configurações customizadas?", font = FONT)
        question_label2.pack(fill=tk.X, pady=5)

        tk.Label(self).pack(pady=20)

        custom_button = tk.Button(
            self,
            text = "Configurações\nCustomizadas",
            font = ("Verdana", 14),
            height=2,
            width=20,
            command = lambda : controller.show_frame(page_list.CONFIGURATION_PAGE)
        )
        custom_button.pack(pady=5)

        default_button = tk.Button(
            self,
            text = "Configurações\nPadrões (Recomendado)",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : self.use_default(controller)
        )
        default_button.pack(pady=5)
    
    def use_default(self, controller):
        controller.shared_data["days"].set(DEFAULT_DAYS)
        controller.shared_data["optimizer"].set(DEFAULT_OPTIMIZER)
        controller.shared_data["loss"].set(DEFAULT_LOSS)
        controller.shared_data["epochs"].set(DEFAULT_EPOCHS)
        controller.shared_data["batch"].set(DEFAULT_BATCH_SIZE)
        controller.shared_data["layers"] = DEFAULT_LAYERS
        
        controller.show_frame(page_list.TRAINING_PAGE)