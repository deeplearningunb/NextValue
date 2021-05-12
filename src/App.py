import tkinter as tk
from os import listdir
from os.path import isfile, join
from pages.StartPage import StartPage
from pages.ConfigurationPage import ConfigurationPage
from pages.TrainingPage import TrainingPage
from pages.ResultPage import ResultPage
from pages.ChooseDatePage import ChooseDatePage
from pages.ChooseIntervalPage import ChooseIntervalPage
from Layer import (
    Layer,
    DEFAULT_DAYS,
    DEFAULT_OPTIMIZER,
    DEFAULT_LOSS,
    DEFAULT_EPOCHS,
    DEFAULT_BATCH_SIZE,
    DEFAULT_LAYERS
)
import pandas as pd
import numpy as np
import math
import page_list
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import datetime

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
            "layers": DEFAULT_LAYERS,
            "cryptocurrency": "Bitcoin",
            "cryptocurrency_list": [f for f in listdir(DATA_PATH) if (isfile(join(DATA_PATH, f)) and f.endswith(".csv"))],
        }
        self.shared_data["days"].set(DEFAULT_DAYS)
        self.shared_data["optimizer"].set(DEFAULT_OPTIMIZER)
        self.shared_data["loss"].set(DEFAULT_LOSS)
        self.shared_data["epochs"].set(DEFAULT_EPOCHS)
        self.shared_data["batch"].set(DEFAULT_BATCH_SIZE)

        self.NUMBER_OF_CRYPTOCURRENCIES = len(self.shared_data["cryptocurrency_list"])
        self.shared_data["cryptocurrency_list"].sort()

        self.process_data(self.shared_data["cryptocurrency_list"])

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        for F in (StartPage, ConfigurationPage, TrainingPage, ResultPage, ChooseDatePage, ChooseIntervalPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(page_list.START_PAGE)

    def show_frame(self, c):
        if c == page_list.START_PAGE:
            frame = self.frames[StartPage]
        elif c == page_list.CONFIGURATION_PAGE:
            frame = self.frames[ConfigurationPage]
        elif c == page_list.TRAINING_PAGE:
            frame = self.frames[TrainingPage]
        elif c == page_list.RESULT_PAGE:
            frame = self.frames[ResultPage]
        elif c == page_list.CHOOSE_DATE_PAGE:
            frame = self.frames[ChooseDatePage]
        elif c == page_list.CHOOSE_INTERVAL_PAGE:
            frame = self.frames[ChooseIntervalPage]
        else:
            return

        frame.tkraise()
    
    def generate_initial_values(self):
        initial_values = {}

        for i in range(self.dataset.shape[0]):
            initial_values[self.dataset.iloc[i, 0]] = self.dataset.iloc[i, 2:].values

        return initial_values

    def process_data(self, cryptocurrency_list):
        cryptocurrency_list.sort()
        TRAINING_RATE = 0.95
        
        self.dataset = pd.read_csv(DATA_PATH + "/Bitcoin.csv")
        self.dataset = self.dataset.iloc[:, 1:3]

        for i in range(0, self.NUMBER_OF_CRYPTOCURRENCIES):
            file = pd.read_csv(DATA_PATH + "/" + cryptocurrency_list[i])
            file = file.iloc[:, 1:3]
            self.dataset = pd.merge(self.dataset, file, on='Date', how='outer')

        self.dataset = self.dataset.replace(np.nan, 0)

        self.initial_values = self.generate_initial_values()

        self.dataset = self.dataset.iloc[:, 2:self.NUMBER_OF_CRYPTOCURRENCIES+2]

        NUMBER_OF_ROWS = self.dataset.shape[0]
        self.TRAINING_SET_SIZE = math.ceil(NUMBER_OF_ROWS*TRAINING_RATE)
        self.TEST_SET_SIZE = NUMBER_OF_ROWS - self.TRAINING_SET_SIZE

        self.test_set = self.dataset.iloc[self.TRAINING_SET_SIZE:, : ].values

        self.sc = MinMaxScaler(feature_range = (0, 1))

    def build_rnn(self):
        self.PREVIOUS_DAYS = int(self.shared_data["days"].get())
        self.values = self.initial_values.copy()

        training_set = self.dataset.iloc[:self.TRAINING_SET_SIZE, : ].values
        training_set_scaled = self.sc.fit_transform(training_set)

        self.X_train = []
        self.y_train = []
        for i in range(self.PREVIOUS_DAYS, self.TRAINING_SET_SIZE):
            self.X_train.append(training_set_scaled[i-self.PREVIOUS_DAYS:i, 0:self.NUMBER_OF_CRYPTOCURRENCIES])
            self.y_train.append(training_set_scaled[i, 0:self.NUMBER_OF_CRYPTOCURRENCIES])

        self.X_train, self.y_train = np.array(self.X_train), np.array(self.y_train)

        self.X_train = self.X_train.reshape((self.X_train.shape[0], self.X_train.shape[1], self.NUMBER_OF_CRYPTOCURRENCIES))

        layer_list = self.shared_data["layers"]
        NUMBER_OF_LAYERS = len(layer_list)

        regressor = Sequential()

        if NUMBER_OF_LAYERS == 1:
            layer = layer_list[0]
            units = layer.units
            dropout = layer.dropout

            regressor.add(LSTM(units = units, input_shape = (self.X_train.shape[1], self.NUMBER_OF_CRYPTOCURRENCIES)))

            if dropout > 0:
                regressor.add(Dropout(dropout))
        else:
            first_layer = layer_list[0]
            units = first_layer.units
            dropout = first_layer.dropout

            regressor.add(LSTM(units = units, return_sequences = True, input_shape = (self.X_train.shape[1], self.NUMBER_OF_CRYPTOCURRENCIES)))

            if dropout > 0:
                regressor.add(Dropout(dropout))

            for i in range(1, NUMBER_OF_LAYERS-1):
                layer = layer_list[i]
                units = layer.units
                dropout = layer.dropout

                regressor.add(LSTM(units = units, return_sequences = True))

                if dropout > 0:
                    regressor.add(Dropout(dropout))

            last_layer = layer_list[-1]
            units = last_layer.units
            dropout = last_layer.dropout

            regressor.add(LSTM(units = units))

            if dropout > 0:
                regressor.add(Dropout(dropout))

        regressor.add(Dense(units = self.NUMBER_OF_CRYPTOCURRENCIES))
        regressor.compile(optimizer = self.shared_data["optimizer"].get(), loss = self.shared_data["loss"].get())

        self.rnn = regressor
    
    def get_test_predict(self):
        inputs = self.dataset[self.TRAINING_SET_SIZE-self.PREVIOUS_DAYS:].values
        inputs = inputs.reshape((inputs.shape[0], inputs.shape[1]))
        inputs = self.sc.transform(inputs)

        self.X_test = []
        for i in range(self.PREVIOUS_DAYS, self.PREVIOUS_DAYS+self.TEST_SET_SIZE):
          self.X_test.append(inputs[i-self.PREVIOUS_DAYS:i, 0:self.NUMBER_OF_CRYPTOCURRENCIES])

        self.X_test = np.array(self.X_test)
        self.X_test = np.reshape(self.X_test, (self.X_test.shape[0], self.X_test.shape[1], self.NUMBER_OF_CRYPTOCURRENCIES))

        predict = self.rnn.predict(self.X_test)
        predict = self.sc.inverse_transform(predict)

        return predict
    
    def predict_day(self, date):
        if date in self.values:
            return self.values[date]
        
        delta = datetime.timedelta(days=self.PREVIOUS_DAYS)
        end_date = datetime.date.fromisoformat(date)
        start_date = end_date - delta
        delta = datetime.timedelta(days=1)

        values = []
        while start_date < end_date:
            d = start_date.strftime('%Y-%m-%d')
            inputs = self.predict_day(d)
            inputs = inputs.reshape(1, -1)
            inputs = self.sc.transform(inputs)
            values.append(inputs)
            start_date += delta
        
        values = [values]
        values = np.array(values)
        values = np.reshape(values, (values.shape[0], values.shape[1], self.NUMBER_OF_CRYPTOCURRENCIES))

        predict = self.rnn.predict(values)
        predict = self.sc.inverse_transform(predict)

        self.values[date] = predict[0]
        return predict[0]

    def predict(self, cryptocurrency, date, end=None):
        cryptocurrency_list = [c[:-4] for c in self.shared_data["cryptocurrency_list"]]
        cryptocurrency_index = cryptocurrency_list.index(cryptocurrency)

        if end == None:
            predict = self.predict_day(date)
            return predict[cryptocurrency_index]
        else:
            start_date = datetime.date.fromisoformat(date)
            end_date = datetime.date.fromisoformat(end)
            delta = datetime.timedelta(days=1)
            predict_list = []

            while start_date <= end_date:
                d = start_date.strftime('%Y-%m-%d')
                predict = self.predict_day(d)
                predict_list.append(predict[cryptocurrency_index])
                start_date += delta

            return predict_list