import tkinter as tk
import page_list
from tkcalendar import Calendar
from datetime import date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChooseIntervalPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

        save_table_button = tk.Button(
            button_area,
            text = "Salvar\n(Tabela)",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : self.save_table()
        )
        save_table_button.grid(row=0, column=2, padx=10, pady=10)

        save_image_button = tk.Button(
            button_area,
            text = "Salvar\n(Gráfico)",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : self.save_image()
        )
        save_image_button.grid(row=0, column=3, padx=10, pady=10)

        self.selected_day_start.trace("w", self.update_calendar)
    
    def predict(self):
        cryptocurrency = self.cryptocurrency.get()

        if cryptocurrency == "Selecione a criptomoeda":
            return

        selected_day_start = self.selected_day_start.get()
        selected_day_end = self.selected_day_end.get()

        predicted_values = [
            12345.67,
            12355.67,
            12360.67,
            12345.67,
            12353.67,
        ]

        predict_dates = [
            "2021-04-30",
            "2021-05-01",
            "2021-05-02",
            "2021-05-03",
            "2021-05-04",
        ]

        for child in self.container_plot.winfo_children():
            child.destroy()
        
        fig = Figure(figsize=(7,3.5))
        a = fig.add_subplot(111)
        a.plot(predict_dates, predicted_values, color = 'blue', label = 'Predicted ' + cryptocurrency + ' Price')
        a.set_title(cryptocurrency + ' Price Prediction')
        a.set_ylabel(cryptocurrency + ' Price', fontsize=14)
        canvas = FigureCanvasTkAgg(fig, master=self.container_plot)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def save_table(self):
        pass

    def save_image(self):
        pass
    
    def update_calendar(self, *args):
        self.cal_end["mindate"] = date.fromisoformat(self.selected_day_start.get())