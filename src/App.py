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
