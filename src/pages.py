import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
            command = lambda : controller.show_frame(TrainingPage)
        )
        default_button.pack(pady=5)


class ConfigurationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.alert = ""

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
        
        controller.show_frame(TrainingPage)


class TrainingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.cryptocurrency_list = [c[:-4] for c in controller.shared_data["cryptocurrency_list"]]
        self.cryptocurrency_list.sort()

        self.test_set_size = controller.TEST_SET_SIZE
        self.test_set = controller.test_set

        welcome_label = tk.Label(self, text = "Clique no botão para começar a treinar", font = ("Verdana", 35))
        welcome_label.pack(fill=tk.X, pady=30)

        self.progress = tk.Label(self, text ="", font = ("Verdana", 20))
        self.progress.pack(side = tk.BOTTOM)

        self.cryptocurrency = tk.StringVar()
        self.cryptocurrency.set("Selecione a criptomoeda")

        self.container_plot = tk.Frame(self, relief=tk.RAISED, height=500)

        self.cryptocurrency.trace("w", self.show_test)

        self.cryptocurrency_menu = tk.OptionMenu(self, self.cryptocurrency, *self.cryptocurrency_list)
        self.cryptocurrency_menu.config(font = ("Verdana", 20))
        self.cryptocurrency_menu["state"] = tk.DISABLED
        self.cryptocurrency_menu.pack()

        self.container_plot.pack()

        config_button = tk.Button(
            self,
            text = "Treinar com outras\nconfigurações",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : controller.show_frame(ConfigurationPage)
        )
        config_button.pack(side = tk.LEFT)

        self.train_button = tk.Button(
            self,
            text = "Treinar",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : self.train(controller)
        )
        self.train_button.pack(side = tk.LEFT)

        self.next_button = tk.Button(
            self,
            text = "Avançar",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            state = tk.DISABLED
        )
        self.next_button.pack(side = tk.LEFT)
    
    def train(self, controller):
        self.train_button["state"] = tk.DISABLED
        self.next_button["state"] = tk.DISABLED
        self.cryptocurrency_menu["state"] = tk.DISABLED

        controller.build_rnn()

        total_epochs = int(controller.shared_data["epochs"].get())

        X_train, y_train = controller.X_train, controller.y_train

        batch_size = int(controller.shared_data["batch"].get())

        for i in range(total_epochs):
            controller.rnn.fit(X_train, y_train, epochs = 1, batch_size = batch_size, verbose=0)
            controller.rnn.reset_states()
            progress = ((i+1)*100) / total_epochs
            self.progress["text"] = "{:.3f}".format(progress) + "%"
            self.update_idletasks()
        
        self.train_button["state"] = tk.NORMAL
        self.train_button["text"] = "Treinar\nnovamente"

        self.next_button["state"] = tk.NORMAL
        self.cryptocurrency_menu["state"] = tk.NORMAL

        self.predict = controller.get_test_predict()

        if(self.cryptocurrency.get() != "Selecione a criptomoeda"):
            self.show_test()
    
    def show_test(self, *args):
        option = self.cryptocurrency.get()
        INDEX_OF_CRYPTOCURRENCY = self.cryptocurrency_list.index(option)
        test_cryptocurrency = []
        predict_cryptocurrency = []

        for i in range(self.test_set_size):
            test_cryptocurrency.append(self.test_set[i, INDEX_OF_CRYPTOCURRENCY])
            predict_cryptocurrency.append(self.predict[i, INDEX_OF_CRYPTOCURRENCY])

        for child in self.container_plot.winfo_children():
            child.destroy()

        fig = Figure(figsize=(7,5))
        a = fig.add_subplot(111)
        a.plot(test_cryptocurrency, color = 'red', label = 'Real ' + option + ' Price')
        a.plot(predict_cryptocurrency, color = 'blue', label = 'Predicted ' + option + ' Price')
        a.set_title(option + ' Price Prediction')
        a.set_ylabel(option + ' Price', fontsize=14)
        a.set_xlabel("Time", fontsize=14)
        canvas = FigureCanvasTkAgg(fig, master=self.container_plot)
        canvas.get_tk_widget().pack()
        canvas.draw()


class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

