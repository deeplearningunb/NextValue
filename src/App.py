import tkinter as tk
from os import listdir
from os.path import isfile, join
from pages import (
    StartPage,
    ConfigurationPage,
    CryptocurrencyChoicePage,
    ResultPage
)

DEFAULT_DAYS = 50
DEFAULT_OPTIMIZER = "adam"
DEFAULT_LOSS = "mean_squared_error"
DEFAULT_EPOCHS = 50
DEFAULT_BATCH_SIZE = 128
UNITS = 600
DROPOUT = 0.2

DATA_PATH = "../Prices"

class App(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self)

        self.shared_data = {
            "days": tk.StringVar(),
            "optimizer": tk.StringVar(),
            "loss": tk.StringVar(),
            "epochs": tk.StringVar(),
            "batch": tk.StringVar(),
            "cryptocurrency": tk.StringVar(),
            "cryptocurrency_list": [f for f in listdir(DATA_PATH) if (isfile(join(DATA_PATH, f)) and f.endswith(".csv"))],
        }
        self.shared_data["days"].set(DEFAULT_DAYS)
        self.shared_data["optimizer"].set(DEFAULT_OPTIMIZER)
        self.shared_data["loss"].set(DEFAULT_LOSS)
        self.shared_data["epochs"].set(DEFAULT_EPOCHS)
        self.shared_data["batch"].set(DEFAULT_BATCH_SIZE)
        self.shared_data["cryptocurrency"].set("Selecione a criptomoeda")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        for F in (StartPage, ConfigurationPage, CryptocurrencyChoicePage, ResultPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(StartPage)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()

    def process_data(self):
        pass

    def build_rnn(self):
        NUMBER_OF_LAYERS = len(self.layer_list)
        NUMBER_OF_CRYPTOCURRENCIES = len(self.shared_data["cryptocurrency_list"])

        regressor = Sequential()

        if NUMBER_OF_LAYERS == 1:
            layer = self.layer_list[0]
            units = layer["units"]
            dropout = layer["dropout"]

            regressor.add(LSTM(units = units, input_shape = (self.dataset.shape[1], NUMBER_OF_CRYPTOCURRENCIES)))

            if dropout > 0:
                regressor.add(Dropout(dropout))
        else:
            first_layer = self.layer_list[0]
            units = first_layer["units"]
            dropout = first_layer["dropout"]

            regressor.add(LSTM(units = units, return_sequences = True, input_shape = (self.dataset.shape[1], NUMBER_OF_CRYPTOCURRENCIES)))

            if dropout > 0:
                regressor.add(Dropout(dropout))

            for i in range(1, NUMBER_OF_LAYERS-1):
                layer = self.layer_list[i]
                units = layer["units"]
                dropout = layer["dropout"]

                regressor.add(LSTM(units = units, return_sequences = True))

                if dropout > 0:
                    regressor.add(Dropout(dropout))

            last_layer = self.layer_list[-1]
            units = last_layer["units"]
            dropout = last_layer["dropout"]

            regressor.add(LSTM(units = units))

            if dropout > 0:
                regressor.add(Dropout(dropout))


        regressor.add(Dense(units = NUMBER_OF_CRYPTOCURRENCIES))
        regressor.compile(optimizer = self.shared_data["optimizer"], loss = self.shared_data["loss"])
