import tkinter as tk

OTIMIZERS = [
    "adadelta",
    "adagrad",
    "adam",
    "adamax",
    "ftrl",
    "nadam",
    "rmsprop"
]

LOSS = [
    "mean_absolute_error",
    "mean_squared_error",
    "mean_squared_logarithmic_error",
]

def validate_percentage(number):
    try:
        number = float(number)
        return number >= 0 and number <= 100
    except ValueError:
        return False

def is_positive_number(number):
    try:
        number = int(number)
        return number > 0
    except ValueError:
        return False

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
            command = lambda : controller.show_frame(ConfigurationPage)
        )
        custom_button.pack(pady=5)

        default_button = tk.Button(
            self,
            text = "Configurações\nPadrões (Recomendado)",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : controller.show_frame(CryptocurrencyChoicePage)
        )
        default_button.pack(pady=5)


class ConfigurationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.alert = "Alerta"

        welcome_label = tk.Label(self, text ="Configurações Customizadas", font = ("Verdana", 14, "bold"))
        welcome_label.pack(pady=10)

        container_bottom = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        container_bottom.pack(fill=tk.BOTH, side=tk.BOTTOM)

        container1 = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        container1.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        container2 = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        container2.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        container1_child_list = []

        for i in range(10):
            container = tk.Frame(container1, relief=tk.RAISED, padx=10)
            container.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
            container1_child_list.append(container)

        days_label = tk.Label(container1_child_list[0], text ="Dias Anteriores", font = ("Verdana", 20, "bold"))
        days_label.pack(side=tk.LEFT)
        days_entry = tk.Entry(container1_child_list[1], font = ("Verdana", 20), textvariable=controller.shared_data["days"])
        days_entry.pack(side=tk.LEFT)

        otimizer_label = tk.Label(container1_child_list[2], text ="Otimizador", font = ("Verdana", 20, "bold"))
        otimizer_label.pack(side=tk.LEFT)
        otimizer_menu = tk.OptionMenu(container1_child_list[3], controller.shared_data["optimizer"], *OTIMIZERS)
        otimizer_menu.config(font = ("Verdana", 20))
        otimizer_menu.pack(side=tk.LEFT)

        loss_label = tk.Label(container1_child_list[4], text ="Loss", font = ("Verdana", 20, "bold"))
        loss_label.pack(side=tk.LEFT)
        loss_menu = tk.OptionMenu(container1_child_list[5], controller.shared_data["loss"], *LOSS)
        loss_menu.config(font = ("Verdana", 20))
        loss_menu.pack(side=tk.LEFT)

        epochs_label = tk.Label(container1_child_list[6], text ="Epochs", font = ("Verdana", 20, "bold"))
        epochs_label.pack(side=tk.LEFT)
        epochs_entry = tk.Entry(container1_child_list[7], font = ("Verdana", 20), textvariable=controller.shared_data["epochs"])
        epochs_entry.pack(side=tk.LEFT)

        batch_label = tk.Label(container1_child_list[8], text ="Batch Size", font = ("Verdana", 20, "bold"))
        batch_label.pack(side=tk.LEFT)
        batch_entry = tk.Entry(container1_child_list[9], font = ("Verdana", 20), textvariable=controller.shared_data["batch"])
        batch_entry.pack(side=tk.LEFT)

        back_button = tk.Button(
            container_bottom,
            text = "Voltar",
            font = ("Verdana", 14),
            height=2,
            width=20,
            command = lambda : controller.show_frame(StartPage)
        )
        back_button.pack(side=tk.LEFT)

        next_button = tk.Button(
            container_bottom,
            text = "Avançar",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : self.verify_values(days_entry.get(), epochs_entry.get(), batch_entry.get(), controller)
        )
        next_button.pack(side=tk.RIGHT)

        self.alert_label = tk.Label(container_bottom, text = self.alert, font = ("Verdana", 14))
        self.alert_label.pack()

    def verify_values(self, days, epochs, batch, controller):
        if (not is_positive_number(days)) or (not is_positive_number(epochs)) or (not is_positive_number(batch)):
            self.alert_label["text"] = "Deve ser um numero maior que 0"
            return
        
        controller.show_frame(CryptocurrencyChoicePage)


class CryptocurrencyChoicePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        FONT = ("Verdana", 16)

        cryptocurrency_list = [c[:-4] for c in controller.shared_data["cryptocurrency_list"]]
        cryptocurrency_list.sort()

        welcome_label = tk.Label(self, text = "Ótimo! A rede neural está configurada!", font = ("Verdana", 35))
        welcome_label.pack(fill=tk.X, pady=70)

        info_label = tk.Label(self, text = "Agora que as configurações foram definidas, falta uma coisa:", font = FONT)
        info_label.pack(fill=tk.X, pady=5)
        
        training_label = tk.Label(self, text = "Você deseja prever o valor de qual criptomoeda?", font = FONT)
        training_label.pack(fill=tk.X, pady=50)

        container_options = tk.Frame(self)
        container_options.pack()

        scrollbar = tk.Scrollbar(container_options)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        mylist = tk.Listbox(container_options, yscrollcommand = scrollbar.set, font = ("Verdana", 12))
        for c in cryptocurrency_list:
            mylist.insert(tk.END, c)
        
        mylist.pack()
        scrollbar.config(command = mylist.yview)

        train_button = tk.Button(
            self,
            text = "Treinar Rede Neural",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
        )
        train_button.pack(pady=80)


class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

