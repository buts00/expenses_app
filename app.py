from datetime import datetime
from tkinter import *
from tkinter import ttk
import expenses_helper as eh
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as font_manager
import seaborn as sns


class App(Tk):

    def __init__(self):
        super().__init__()
        self.title('Expenses')
        self.resizable(0, 0)
        self['background'] = '#EBEBEB'
        self.iconbitmap('icon.ico')
        self.style = ttk.Style()
        self.style.theme_use('xpnative')
        self.conf = {'padx': {10, 10}, 'pady': 10}
        self.bold_font = 'Helvetica 11 bold'
        self.put_btn_graph()
        self.put_frames()

    def put_frames(self):
        self.frame_graph = Graph(self)
        self.frame_list = ListFrame(self)
        self.frame_add_form = AddForm(self)
        self.statistic = StatFrame(self)
        self.frame_pie_graph = PieGraph(self)
        self.frame_add_form.grid(column=0, row=0, sticky='ns')
        self.check_btn()

    def put_btn_graph(self):
        self.enabled = IntVar()
        self.checkbutton = ttk.Checkbutton(text="Graph", variable=self.enabled,
                                           command=lambda: self.check_btn())
        self.checkbutton.lift()
        self.checkbutton.configure(takefocus=0)
        self.checkbutton.place(relx=0.5, rely=0.375, anchor='center')

    def refresh(self):
        all_f = [f for f in self.children]
        for frame in all_f:
            if self.nametowidget(frame) != self.nametowidget(self.checkbutton):
                self.nametowidget(frame).destroy()
        self.put_frames()

    def check_btn(self):
        if self.enabled.get():
            self.checkbutton.lift()
            self.checkbutton.place(relx=0.52, rely=0.32, anchor='center')
            self.statistic.grid_forget()
            self.frame_pie_graph.grid(column=1, row=0, sticky='ns')
            self.frame_list.grid_forget()
            self.frame_graph.grid(column=0, row=1, columnspan=2, sticky='we')
        else:
            self.checkbutton.lift()
            self.frame_pie_graph.grid_forget()
            self.statistic.grid(column=1, row=0, sticky='ns')
            self.checkbutton.place(relx=0.55, rely=0.375, anchor='center')
            self.frame_graph.grid_forget()
            self.frame_list.grid(column=0, row=1, columnspan=2, sticky='we')


class AddForm(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()

    def put_widgets(self):
        self.all_expenses = eh.get_all_expenses_name()
        self.l_choose = ttk.Label(self, text='Choose an expense item')
        self.f_choose = ttk.Combobox(self, values=self.all_expenses)
        self.l_amount = ttk.Label(self, text='Enter amount')
        self.f_amount = ttk.Entry(self, validate='key', validatecommand=(self.register(self.validate_amount), '%P'))
        self.l_date = ttk.Label(self, text='Enter date')
        self.f_date = DateEntry(self, foreground='black', normalforeground='black', selectforeground='red',
                                selectbackground='white', background='white', date_pattern='mm-dd-YYYY')
        self.btn_submit = ttk.Button(self, text='Submit', command=self.add_form)
        self.btn_del = ttk.Button(self, text='Delete', command=lambda: self.master.frame_list.delete_form())

        self.l_choose.grid(row=0, column=0, sticky='w', cnf=self.master.conf)
        self.f_choose.grid(row=0, column=1, sticky='e', cnf=self.master.conf)
        self.l_amount.grid(row=1, column=0, sticky='w', cnf=self.master.conf)
        self.f_amount.grid(row=1, column=1, sticky='e', cnf=self.master.conf)
        self.l_date.grid(row=2, column=0, sticky='w', cnf=self.master.conf)
        self.f_date.grid(row=2, column=1, sticky='e', cnf=self.master.conf)
        self.btn_submit.grid(row=3, column=1,sticky='e', cnf=self.master.conf)
        self.btn_del.grid(row=3, column=0,sticky='w', cnf=self.master.conf)

    def validate_amount(self, input):
        if input == '':
            return True
        try:
            x = float(input)
            return True
        except ValueError:
            return False
            self.bell()

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
        self.put_widgets_table()

    def put_widgets_table(self):
        list_of_payments = eh.get_all_payments()
        self.table = ttk.Treeview(self, show='headings')
        self.heads = ['id', 'name', 'amount', 'date']
        self.table['column'] = self.heads
        for header in self.heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')

        for row in list_of_payments:
            value = (row.id, eh.Expense[row.payment_id].name, row.amount, row.payment_date)
            self.table.insert('', END, values=value)
        self.table.bind("<Delete>", lambda event: self.delete_form())
        self.scr = ttk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scr.set)
        self.scr.pack(side=RIGHT, fill=Y)
        self.table.pack(expand=YES, fill=BOTH)

    def delete_form(self):
        try:
            self.cur_item = self.table.focus()
            self.item_id = self.table.item(self.cur_item)['values'][0]
            eh.delete_form(self.item_id)
            self.table.delete(self.cur_item)
            self.master.refresh()
        except IndexError:
            pass


class Graph(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.put_widgets()

    def put_widgets(self):
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.amount = eh.get_amount_for_month()
        self.fig = plt.Figure(figsize=(8, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.bar(self.months, self.amount,
                    color=["#4c00ff", "#19278c", '#4df065', '#24d63f', "#0aad23", "#f3b197", "#f7926a", '#ed7140',
                           '#ff9c38',
                           '#de7b16', '#c98540', "#00aeff"], edgecolor="gray", linewidth=1)
        self.ax.set_title("Statistic", fontsize=16)
        self.ax.grid(axis='y', linestyle='--', linewidth=0.5)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.fig.subplots_adjust(right=0.95,left= 0.1)
        self.canvas.draw()
        self.fig.set_facecolor(self.master['background'])
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


class PieGraph(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.put_widgets()

    def put_widgets(self):
        self.all_name,self.all_amount = eh.get_all_expenses_dict()
        self.fig = plt.Figure(figsize=(3.7, 1.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.pie(self.all_amount, autopct='%1.1f%%', startangle=0, shadow=True,rotatelabels=False,pctdistance=0.75, textprops={ 'size': 7},colors = sns.color_palette('pastel'))
        self.ax.legend(title='Category', labels=self.all_name, loc='upper left', bbox_to_anchor=(-0.4, 1.1),prop=font_manager.FontProperties(size=8))
        self.ax.axis('equal')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.fig.subplots_adjust(right=1.1,left=0.45)
        self.canvas.draw()
        self.fig.set_facecolor(self.master['background'])
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


app = App()
app.mainloop()
