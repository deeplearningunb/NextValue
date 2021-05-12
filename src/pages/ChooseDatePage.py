import tkinter as tk
import page_list
from tkcalendar import Calendar
from datetime import date

class ChooseDatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        cryptocurrency_list = [c[:-4] for c in controller.shared_data["cryptocurrency_list"]]
        cryptocurrency_list.sort()

        welcome_label = tk.Label(self, text = "Escolha a data", font = ("Verdana", 35))
        welcome_label.pack(fill=tk.X, pady=30)

        self.selected_day = tk.StringVar()
        self.cryptocurrency = tk.StringVar()
        self.cryptocurrency.set("Selecione a criptomoeda")

        self.selected_day.trace("w", self.show_predict)
        self.cryptocurrency.trace("w", self.show_predict)

        cal = Calendar(self, selectmode = 'day', mindate = date.today(), textvariable = self.selected_day, date_pattern="yyyy-mm-dd")
        cal.selection_set(date.today())
        cal.pack()

        cryptocurrency_menu = tk.OptionMenu(self, self.cryptocurrency, *cryptocurrency_list)
        cryptocurrency_menu.config(font = ("Verdana", 16))
        cryptocurrency_menu.pack(pady=50)

        self.value = tk.Label(self, text = "US$: ", font = ("Verdana", 20, "bold"))
        self.value.pack(fill=tk.X, pady=30)

        back_button = tk.Button(
            self,
            text = "Voltar",
            font = ("Verdana", 14),
            height = 2,
            width = 20,
            command = lambda : controller.show_frame(page_list.RESULT_PAGE)
        )
        back_button.pack(pady=50)
    
    def show_predict(self, *args):
        cryptocurrency = self.cryptocurrency.get()

        if cryptocurrency == "Selecione a criptomoeda":
            return

        selected_day = self.selected_day.get()

        value = self.controller.predict(cryptocurrency, selected_day)

        self.value["text"] = "US$: {:.2f}".format(value)