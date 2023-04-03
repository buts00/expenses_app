from datetime import datetime
from tkinter import *
from tkinter import ttk
import expenses_helper as eh
from tkcalendar import DateEntry


class App(Tk):

    def __init__(self):
        super().__init__()
        self.title('Expenses')
        self['background'] = '#EBEBEB'
        self.resizable(0,0)
        self.iconbitmap('icon.ico')
        self.style = ttk.Style()
        self.style.theme_use('xpnative')
        self.conf = {'padx': {10, 10}, 'pady': 10}
        self.bold_font = 'Helvetica 11 bold'
        self.put_frames()

    def put_frames(self):
        self.frame_add_form = AddForm(self).grid(column=0, row=0, sticky='ns')
        self.self = StatFrame(self).grid(column=1, row=0, sticky='ns')
        self.frame_list = ListFrame(self).grid(column=0, row=1, columnspan=2, sticky='we')

    def refresh(self):
        all_f = [f for f in self.children]
        for frame in all_f:
            self.nametowidget(frame).destroy()
        self.put_frames()


class AddForm(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()

    def put_widgets(self):
        self.get_all_names_of_payments()
        self.l_choose = ttk.Label(self, text='Choose an expense item')
        self.f_choose = ttk.Combobox(self, values=self.items)
        self.l_amount = ttk.Label(self, text='Enter amount')
        self.f_amount = ttk.Entry(self, validate='key', validatecommand=(self.register(self.validate_amount),'%P'))
        self.l_date = ttk.Label(self, text='Enter date')
        self.f_date = DateEntry(self, foreground='black', normalforeground='black', selectforeground='red',
                                selectbackground='white', background='white', date_pattern='mm-dd-YYYY')
        self.btn_submit = ttk.Button(self, text='submit', command=self.add_form)

        self.l_choose.grid(row=0, column=0, sticky='w', cnf=self.master.conf)
        self.f_choose.grid(row=0, column=1, sticky='e', cnf=self.master.conf)
        self.l_amount.grid(row=1, column=0, sticky='w', cnf=self.master.conf)
        self.f_amount.grid(row=1, column=1, sticky='e', cnf=self.master.conf)
        self.l_date.grid(row=2, column=0, sticky='w', cnf=self.master.conf)
        self.f_date.grid(row=2, column=1, sticky='e', cnf=self.master.conf)
        self.btn_submit.grid(row=3, column=0, columnspan=2, cnf=self.master.conf)

    def validate_amount(self, input):
        if input == '':
            return True
        try:
            x = float(input)
            return True
        except ValueError:
            return False
            self.bell()

    def get_all_names_of_payments(self):
        all_expenses = eh.get_all_expenses()
        self.items = []
        for expense in all_expenses:
            self.items.append(expense.name)

    def add_form(self):
        flag = True
        name = str(self.f_choose.get())
        name = name.strip()
        date = datetime.strptime(self.f_date.get(), '%m-%d-%Y').date()
        self.l_choose['foreground'] = 'black'
        self.l_amount['foreground'] = 'black'

        if name == '':
            self.l_choose['foreground'] = 'red'
            self.bell()
            flag = False

        try:
           amount = float(self.f_amount.get())
        except ValueError:
            self.l_amount['foreground'] = 'red'
            flag = False
            self.bell()

        if flag:
            eh.create_new_form(name, amount, date)
            self.master.refresh()


class StatFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()

    def put_widgets(self):
        self.l_most_common_text = Label(self, text='The most common item')
        self.l_most_common_value = Label(self, text=eh.get_most_common_item(), font=self.master.bold_font)
        self.l_exp_item_text = Label(self, text='The most expensive item')
        self.l_exp_item_value = Label(self, text=eh.get_most_expensive_item(), font=self.master.bold_font)
        self.l_exp_day_value = Label(self, text=eh.get_most_expensive_day(), font=self.master.bold_font)
        self.l_exp_day_text = Label(self, text='The most expensive day')
        self.l_exp_month_text = Label(self, text='The most expensive month')
        self.l_exp_month_text_value = Label(self, text=eh.get_most_expensive_month(), font=self.master.bold_font)

        self.l_most_common_text.grid(row=0, column=0, sticky='w', cnf=self.master.conf)
        self.l_most_common_value.grid(row=0, column=1, sticky='e', cnf=self.master.conf)
        self.l_exp_item_text.grid(row=1, column=0, sticky='w', cnf=self.master.conf)
        self.l_exp_item_value.grid(row=1, column=1, sticky='e', cnf=self.master.conf)
        self.l_exp_day_text.grid(row=2, column=0, sticky='w', cnf=self.master.conf)
        self.l_exp_day_value.grid(row=2, column=1, sticky='e', cnf=self.master.conf)
        self.l_exp_month_text.grid(row=3, column=0, sticky='w', cnf=self.master.conf)
        self.l_exp_month_text_value.grid(row=3, column=1, sticky='e', cnf=self.master.conf)


class ListFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()

    def put_widgets(self):
        list_of_payments = eh.get_all_payments()
        table = ttk.Treeview(self, show='headings')
        heads = ['id', 'name', 'amount', 'date']
        table['column'] = heads
        for header in heads:
            table.heading(header, text=header, anchor='center')
            table.column(header, anchor='center')

        for row in list_of_payments:
            value = (row.id, eh.Expense[row.payment_id].name, row.amount, row.payment_date)
            table.insert('', END, values=value)

        scr = ttk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scr.set)
        scr.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)


app = App()
app.mainloop()
