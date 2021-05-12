import tkinter as tk
import page_list
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TrainingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.cryptocurrency_list = [c[:-4] for c in controller.shared_data["cryptocurrency_list"]]

        self.test_set_size = controller.TEST_SET_SIZE
        self.test_set = controller.test_set

        welcome_label = tk.Label(self, text = "Clique no botão para começar a treinar", font = ("Verdana", 35))
        welcome_label.pack(fill=tk.X, pady=20)

        self.progress = tk.Label(self, text ="", font = ("Verdana", 20))
        self.progress.pack(side = tk.BOTTOM)

        self.cryptocurrency = tk.StringVar()
        self.cryptocurrency.set("Selecione a criptomoeda")

        self.container_plot = tk.Frame(self, relief=tk.RAISED, height=500)

        self.cryptocurrency.trace("w", self.show_test)

        self.cryptocurrency_menu = tk.OptionMenu(self, self.cryptocurrency, *self.cryptocurrency_list)
        self.cryptocurrency_menu.config(font = ("Verdana", 20))
        self.cryptocurrency_menu["state"] = tk.DISABLED
        self.cryptocurrency_menu.pack(pady=5)

        self.container_plot.pack()

        container_button = tk.Frame(self)
        container_button.pack()

        config_button = tk.Button(
            container_button,
            text = "Treinar com outras\nconfigurações",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : controller.show_frame(page_list.CONFIGURATION_PAGE)
        )
        config_button.grid(row=0, column=0, padx=10, pady=10)

        self.train_button = tk.Button(
            container_button,
            text = "Treinar",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : self.train(controller)
        )
        self.train_button.grid(row=0, column=1, padx=10, pady=10)

        self.next_button = tk.Button(
            container_button,
            text = "Avançar",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            state = tk.DISABLED,
            command = lambda : controller.show_frame(page_list.RESULT_PAGE)
        )
        self.next_button.grid(row=0, column=2, padx=10, pady=10)
    
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
