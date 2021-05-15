import tkinter as tk
import page_list
from Layer import Layer

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

def is_positive_number(number):
    try:
        number = int(number)
        return number > 0
    except ValueError:
        return False

def get_formated(pos, units, dropout):
    return "{:d}. Units: {:d}    Dropout: {:.0f}%".format(pos, units, dropout)

class ConfigurationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.alert = ""
        self.layers = controller.shared_data["layers"]

        welcome_label = tk.Label(self, text ="Configurações Customizadas", font = ("Verdana", 14, "bold"))
        welcome_label.pack(pady=10)

        container_bottom = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        container_bottom.pack(fill=tk.BOTH, side=tk.BOTTOM)

        container1 = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        container1.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.container2 = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.container2.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

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

        container2_button = tk.Frame(self.container2, relief=tk.RAISED, borderwidth=1)
        container2_button.pack(side=tk.BOTTOM, fill=tk.BOTH)

        container2_button_left = tk.Frame(container2_button)
        container2_button_left.pack(side=tk.LEFT)
        container2_button_right = tk.Frame(container2_button)
        container2_button_right.pack(side=tk.RIGHT)

        container2_button_left_row1 = tk.Frame(container2_button_left)
        container2_button_left_row1.pack(fill=tk.BOTH)
        container2_button_left_row2 = tk.Frame(container2_button_left)
        container2_button_left_row2.pack(fill=tk.BOTH)

        units_label = tk.Label(container2_button_left_row1, text ="Units", font = ("Verdana", 15, "bold"))
        units_label.pack(side=tk.LEFT)
        units_entry = tk.Entry(container2_button_left_row1, font = ("Verdana", 15), width=30)
        units_entry.pack(side=tk.LEFT)

        dropout_label = tk.Label(container2_button_left_row2, text ="Dropout: ", font = ("Verdana", 15, "bold"))
        dropout_label.pack(side=tk.LEFT)
        dropout_value_label = tk.Label(container2_button_left_row2, text ="0%", font = ("Verdana", 15, "bold"), width=6)
        dropout_value_label.pack(side=tk.LEFT)
        dropout_scale = tk.Scale(
            container2_button_left_row2,
            orient=tk.HORIZONTAL,
            length=255,
            showvalue=0,
            to=99,
            command = lambda value : self.update_label_value(dropout_value_label, value)
        )
        dropout_scale.pack(side=tk.LEFT)

        add_button = tk.Button(
            container2_button_right,
            text = "+",
            font = ("Verdana", 20),
            height=1,
            width=2,
            bg='blue',
            fg='white',
            activebackground='cyan',
            command = lambda : self.add_layer(units_entry.get(), dropout_scale.get())
        )
        add_button.pack(fill=tk.BOTH, side=tk.LEFT)

        remove_button = tk.Button(
            container2_button_right,
            text = "X",
            font = ("Verdana", 20),
            height=1,
            width=2,
            bg='red',
            fg='white',
            activebackground='brown',
            command = lambda : self.remove_layer(self.layer_list.curselection())
        )
        remove_button.pack(fill=tk.BOTH, side=tk.LEFT)

        scrollbar = tk.Scrollbar(self.container2)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.layer_list = tk.Listbox(self.container2, yscrollcommand=scrollbar.set, height=40, font=("Verdana", 20, "bold"))
        for l in controller.shared_data["layers"]:
            self.layer_list.insert(tk.END, get_formated(self.layer_list.size()+1, l.units, l.dropout*100))

        self.layer_list.pack(fill = tk.BOTH)
        scrollbar.config(command = self.layer_list.yview)

        back_button = tk.Button(
            container_bottom,
            text = "Voltar",
            font = ("Verdana", 14),
            height=2,
            width=20,
            command = lambda : controller.show_frame(page_list.START_PAGE)
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
        
        if self.layer_list.size() == 0:
            self.alert_label["text"] = "Deve haver pelo menos uma camada"
            return
        
        controller.shared_data["layers"] = self.layers
        controller.show_frame(page_list.TRAINING_PAGE)
    
    def update_label_value(self, label, value):
        label["text"] = value + "%"
    
    def add_layer(self, units, dropout):
        if not is_positive_number(units):
            self.alert_label["text"] = "Units deve ser um numero maior que 0"
            return

        self.layer_list.insert(tk.END, get_formated(self.layer_list.size()+1, int(units), dropout))
        self.layers.append(Layer(units=int(units), dropout=dropout/100))
    
    def remove_layer(self, position):
        if len(position) == 1:
            position = position[0]
            self.layer_list.delete(position, self.layer_list.size())

            for i in range(position+1, len(self.layers)):
                self.layer_list.insert(tk.END, get_formated(i, self.layers[i].units, self.layers[i].dropout*100))

            self.layers.pop(position)