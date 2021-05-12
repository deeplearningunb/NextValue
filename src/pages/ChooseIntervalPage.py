import tkinter as tk
from tkinter import filedialog
import page_list
from tkcalendar import Calendar
from datetime import date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import matplotlib.pyplot as plt
import pandas as pd

class ChooseIntervalPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        cryptocurrency_list = [c[:-4] for c in controller.shared_data["cryptocurrency_list"]]
        cryptocurrency_list.sort()

        welcome_label = tk.Label(self, text = "Escolha a data", font = ("Verdana", 35))
        welcome_label.pack(fill=tk.X, pady=15)

        self.selected_day_start = tk.StringVar()
        self.selected_day_end = tk.StringVar()
        self.cryptocurrency = tk.StringVar()
        self.cryptocurrency.set("Selecione a criptomoeda")

        calendar_area = tk.Frame(self)
        calendar_area.pack()

        start_label = tk.Label(calendar_area, text = "Data de Início", font = ("Verdana", 18))
        start_label.grid(row=0, column=0, padx=20)

        calendar_start = tk.Frame(calendar_area)
        calendar_start.grid(row=1, column=0, padx=20)

        end_label = tk.Label(calendar_area, text = "Data de Término", font = ("Verdana", 18))
        end_label.grid(row=0, column=1, padx=20)

        calendar_end = tk.Frame(calendar_area)
        calendar_end.grid(row=1, column=1, padx=20)

        self.cal_start = Calendar(calendar_start, selectmode = 'day', mindate = date.today(), textvariable = self.selected_day_start, date_pattern="yyyy-mm-dd")
        self.cal_start.selection_set(date.today())
        self.cal_start.pack()

        self.cal_end = Calendar(calendar_end, selectmode = 'day', mindate = date.today(), textvariable = self.selected_day_end, date_pattern="yyyy-mm-dd")
        self.cal_end.selection_set(date.today())
        self.cal_end.pack()

        cryptocurrency_menu = tk.OptionMenu(self, self.cryptocurrency, *cryptocurrency_list)
        cryptocurrency_menu.config(font = ("Verdana", 16))
        cryptocurrency_menu.pack(pady=20)

        self.container_plot = tk.Frame(self, relief=tk.RAISED, height=350)
        self.container_plot.pack()

        button_area = tk.Frame(self)
        button_area.pack()

        back_button = tk.Button(
            button_area,
            text = "Voltar",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : controller.show_frame(page_list.RESULT_PAGE)
        )
        back_button.grid(row=0, column=0, padx=10, pady=10)

        predict_button = tk.Button(
            button_area,
            text = "Fazer previsão",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : self.predict()
        )
        predict_button.grid(row=0, column=1, padx=10, pady=10)

        self.save_table_button = tk.Button(
            button_area,
            text = "Salvar\n(Tabela)",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            state = tk.DISABLED,
            command = lambda : self.save_table()
        )
        self.save_table_button.grid(row=0, column=2, padx=10, pady=10)

        self.save_image_button = tk.Button(
            button_area,
            text = "Salvar\n(Gráfico)",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            state = tk.DISABLED,
            command = lambda : self.save_image()
        )
        self.save_image_button.grid(row=0, column=3, padx=10, pady=10)

        self.selected_day_start.trace("w", self.update_calendar)
    
    def predict(self):
        self.save_table_button["state"] = tk.DISABLED
        self.save_image_button["state"] = tk.DISABLED

        cryptocurrency = self.cryptocurrency.get()

        if cryptocurrency == "Selecione a criptomoeda":
            return

        selected_day_start = self.selected_day_start.get()
        selected_day_end = self.selected_day_end.get()

        self.predicted_values = self.controller.predict(cryptocurrency, selected_day_start, selected_day_end)
        
        self.predict_dates = []

        selected_day_start = datetime.date.fromisoformat(selected_day_start)
        selected_day_end = datetime.date.fromisoformat(selected_day_end)

        delta = datetime.timedelta(days=1)

        while selected_day_start <= selected_day_end:
            self.predict_dates.append(selected_day_start.strftime('%d/%m'))
            selected_day_start += delta

        for child in self.container_plot.winfo_children():
            child.destroy()
        
        fig = Figure(figsize=(7,3.5))
        a = fig.add_subplot(111)
        a.plot(self.predict_dates, self.predicted_values, color = 'blue', label = 'Predicted ' + cryptocurrency + ' Price')
        a.xaxis.set_major_locator(plt.MaxNLocator(min(10, len(self.predict_dates))))
        a.set_title(cryptocurrency + ' Price Prediction')
        a.set_ylabel(cryptocurrency + ' Price', fontsize=14)
        canvas = FigureCanvasTkAgg(fig, master=self.container_plot)
        canvas.get_tk_widget().pack()
        canvas.draw()

        self.image = fig

        self.save_table_button["state"] = tk.NORMAL
        self.save_image_button["state"] = tk.NORMAL

    def save_table(self):
        path = filedialog.asksaveasfilename(initialdir = "/",title = "Selecione o Local para Salvar",filetypes = [("CSV files","*.csv")])
        
        if isinstance(path, tuple) or path == '':
            return
        
        dataframe = {
            "Date": self.predict_dates,
            "Closing Price (USD)": self.predicted_values
        }

        dataframe = pd.DataFrame(dataframe, columns= ['Date', 'Closing Price (USD)'])

        dataframe.to_csv(path, index = False, header=True)

    def save_image(self):
        path = filedialog.asksaveasfilename(initialdir = "/",title = "Selecione o Local para Salvar",filetypes = [("PNG files","*.png")])
        
        if isinstance(path, tuple) or path == '':
            return
        
        self.image.savefig(path)
    
    def update_calendar(self, *args):
        selected_day_start = datetime.date.fromisoformat(self.selected_day_start.get())
        selected_day_end = datetime.date.fromisoformat(self.selected_day_end.get())
        delta = datetime.timedelta(days=1)

        if selected_day_end < selected_day_start:
            self.cal_end.selection_set(selected_day_start+delta)
        
        self.cal_end["mindate"] = selected_day_start+delta