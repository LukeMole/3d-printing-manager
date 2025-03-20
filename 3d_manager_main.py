from tkinter import *
from tkinter import ttk # library and all associated commands sourced from https://tkdocs.com/tutorial/onepage.html on 2023/06/28 14:27
from tkinter import messagebox
import csv
import datetime
import re

pending_orders_print = []
available_prints = []
pending_orders = []
income_expenses = []
income_expenses_print = []
filament_colors = []
filament_type = []
print_type_list = []

income = float()
expense = float()
profit = float()

file_names = ['pending_orders.csv', 'income_expenses.csv', 'filaments.txt','colors.txt','inoutprofit.txt','prints.csv']

#filament_stats = {}
#color_stats = {}
#delivery_collect_stats = {}


def main():
    #check if files exist and makes them if not
    for file in file_names: #checking if a file exists sourced from https://www.freecodecamp.org/news/file-handling-in-python/#:~:text=How%20to%20Create%20Files%20in,it%20will%20return%20an%20error. 20:35 2023/08/22
        try:
            open(file, 'x')
        except FileExistsError:
            pass

    # load pending orders
    with open('pending_orders.csv') as file:
        reader = csv.reader(file)
        try:
            for name, dprint, color, address, price, coll_del, filament, place_date in reader:
                pending_orders.append({
                    'name': name,
                    'print': dprint,
                    'color': color,
                    'address': address,
                    'price': price,
                    'collect_deliver':coll_del,
                    'filament': filament,
                    'date': place_date
                    })
                pending_orders_print.append(dprint)
        except ValueError:
            pass
    pending_orders.reverse() # .reverse() sourced from https://www.programiz.com/python-programming/methods/list/reverse at 17:48 2023/07/09
    pending_orders_print.reverse()

    #loading completed orders
    with open('income_expenses.csv') as file:
        for line in file:
            try:
                print(line)
                name, dprint, color, address, price, coll_del, filament, place_date, comp_date, o_e_type = line.split(',')
                income_expenses.append(
                    {
                        'name':name,
                        'print':dprint,
                        'color':color,
                        'address': address,
                        'price': price,
                        'collect_deliver':coll_del,
                        'filament':filament,
                        'date':place_date,
                        'complete_date': comp_date,
                        'type': o_e_type.removesuffix('\n')
                    }
                )
                print(income_expenses)
                income_expenses_print.append(dprint)
            except ValueError:
                try:
                    description, cost, date, o_e_type = line.split(',')
                    income_expenses.append(
                        {
                            'description':description,
                            'cost':cost,
                            'date':date,
                            'type':o_e_type
                        }
                    )
                    income_expenses_print.append('Expense ' + date)
                except ValueError:
                    ...
    income_expenses.reverse()
    income_expenses_print.reverse()


    #load filament types
    with open('filaments.txt') as file:
        for line in file:
            global filament_type
            filament_type.append(line) # how to add things to a tuple sourced from https://note.nkmk.me/en/python-tuple-operation/#:~:text=comma%20in%20Python-,Add%2Finsert%20items%20to%20a%20tuple,a%20list%20using%20list()%20.&text=Insert%20an%20item%20using%20insert()%20. at 11:14 2023/06/29
        filament_type.append('Add...')
        filament_type.append('Rem...')
        print(filament_type)

    #load colors
    with open('colors.txt') as file:
        for line in file:
            global filament_colors
            i = tuple([line])
            filament_colors += i

        filament_colors += ('Add...', 'Rem...')

    #load income, expenses, profit
    global income, expense, profit
    with open('inoutprofit.txt') as file:
        for line in file:
            income, expense = line.split(',')
        income = float(income)
        expense = float(expense)
        profit = income - expense

    #load stats
    #load_stats(filament_stats, 'FILAMENT')
    #load_stats(color_stats, 'COLOR')
    #load_stats(delivery_collect_stats, 'SEND')

def add_order(*args):
    global print_type
    global print_type_list
    global available_prints
    global print_type_cmbx

    order_info_lbl.configure(text='ADD ORDER:')
    edit_btn.grid_forget()
    remove_order_btn.configure(text='Add', command=add_new_order)


    print_type_cmbx = ttk.Combobox(homeframe, textvariable=print_type)
    print_type_cmbx.grid(column=3, row=3, sticky=(W,S), padx=10, pady=8, rowspan=2, columnspan=2)
    print_type_cmbx.configure(width=17)
    print_type_cmbx.bind('<<ComboboxSelected>>', add_new_print)
    print_type_list = []

    with open('prints.csv') as file:
        reader = csv.reader(file)
        for name, price in reader:
            available_prints.append({'print': name, 'price': price})
            i = tuple([name])
            print_type_list += i

    print_type_list += ('Add...', 'Rem...')
    print_type_cmbx['values'] = print_type_list
    print_type_cmbx.current(0)
    print_type_cmbx.state(['readonly'])

    # sourced how to disable a button from https://stackoverflow.com/questions/53580507/disable-enable-button-in-tkinter at 13:08 2023/06/29
    order_complete_btn['state'] = DISABLED
    new_expense_btn['state'] = DISABLED
    pending_orders_lstbx['state'] = DISABLED

    name_edt.delete(0, 'end')
    address_edt.delete(0, 'end')
    price_edt.delete(0, 'end')
    date_edt.delete(0,'end')

    add_order_btn.configure(text='Cancel', command=cancel_new_order)
    price_edt.insert(0, available_prints[0]['price'])

    todays_date = str(datetime.date.today())
    todays_date = todays_date.replace('-', '/')
    date_edt.insert(0, todays_date)


def add_new_order():
    name = name_edt.get()
    placed_print = print_type_cmbx.get()
    address = address_edt.get()
    price = price_edt.get()
    filament = filament_type_cmbx.get()
    filament = filament.removesuffix('\n')
    color = color_cmbx.get()
    color = color.removesuffix('\n')
    deliver_collect = del_col_cmbx.get()
    placed_date = date_edt.get()

    with open('pending_orders.csv', 'a') as file:
        file.write(name+','+placed_print+','+color+','+address+','+str(price)+','+deliver_collect+','+filament+','+placed_date+'\n')

    pending_orders.insert(0, {
                'name': name,
                'print': placed_print,
                'color': color,
                'address': address,
                'price': price,
                'collect_deliver':deliver_collect,
                'filament': filament,
                'date': placed_date
                })

    pending_orders_lstbx['state'] = NORMAL
    pending_orders_print.insert(0, placed_print)
    prints_var.set(pending_orders_print)
    pending_orders_lstbx.configure(listvariable=prints_var)

    remove_order_btn.configure(text='Remove', command=remove_order)
    cancel_new_order()


def remove_order():
    yes_no = messagebox.askyesno(
        message='Are you sure you want to delete this order?'
    )

    if yes_no == True:

        pending_orders.pop(pending_orders_lstbx.curselection()[0])
        pending_orders_print.pop(pending_orders_lstbx.curselection()[0])
        prints_var.set(pending_orders_print)
        pending_orders.reverse()

        with open('pending_orders.csv', 'w') as file:
            for item in pending_orders:
                file.write(item['name'] +','+
                        item['print']+','+
                        item['color']+','+
                        item['address']+','+
                        item['price']+','+
                        item['collect_deliver']+','+
                        item['filament']+','+
                        item['date']+'\n')

        pending_orders.reverse()

        print(pending_orders_lstbx.curselection())
        if len(pending_orders_lstbx.curselection()) == 0:
            change_info(0)
            pending_orders_lstbx.select_set(0)
        else:
            change_info(pending_orders_lstbx.curselection()[0])

def edit_order():
    yes_no = messagebox.askyesno(message='Are you sure you want to edit this order?')

    if yes_no == True:
        pending_orders[current_selection]['name'] = name_edt.get()
        pending_orders[current_selection]['color'] = color_cmbx.get().removesuffix('\n')
        pending_orders[current_selection]['address'] = address_edt.get()
        pending_orders[current_selection]['price'] = price_edt.get()
        pending_orders[current_selection]['collect_deliver'] = del_col_cmbx.get()
        pending_orders[current_selection]['filament'] = filament_type_cmbx.get().removesuffix('\n')
        pending_orders[current_selection]['date'] = date_edt.get()
        pending_orders.reverse()

        with open('pending_orders.csv', 'w') as file:
            for item in pending_orders:
                file.write(item['name'] +','+
                        item['print']+','+
                        item['color']+','+
                        item['address']+','+
                        item['price']+','+
                        item['collect_deliver']+','+
                        item['filament']+','+
                        item['date']+'\n')

        pending_orders.reverse()

def order_complete():
    global income, profit, expense
    yes_no = messagebox.askyesno(message='Confirm that the order is completed')

    if yes_no == True:

        complete_date = str(datetime.date.today())
        index = pending_orders_lstbx.curselection()[0]
        income_expenses.insert(0, (pending_orders[index] | {'complete_date': complete_date}))
        print(income_expenses)
        income_expenses_print.insert(0, pending_orders_print[index])

        income += float(income_expenses[0]['price'])
        income_lbl.configure(text='INCOME: ' + str(income))
        profit = income - expense
        profit_lbl.configure(text='PROFIT: ' + str(profit))

        with open('inoutprofit.txt', 'w') as file:
            file.write(str(income) + ',' + str(expense))

        with open('income_expenses.csv', 'a') as file:
            file.write(
                income_expenses[0]['name'] +','+
                income_expenses[0]['print']+','+
                income_expenses[0]['color']+','+
                income_expenses[0]['address']+','+
                income_expenses[0]['price']+','+
                income_expenses[0]['collect_deliver']+','+
                income_expenses[0]['filament']+','+
                income_expenses[0]['date']+','+
                income_expenses[0]['complete_date']+
                ',income' + '\n'
            )

    temp_pen_order = []

    with open('pending_orders.csv', 'r') as file:
        for line in file:
            temp_pen_order.append(line)

    temp_pen_order.reverse()
    temp_pen_order.pop(index)
    pending_orders.pop(index)
    pending_orders_print.pop(index)
    temp_pen_order.reverse()

    with open('pending_orders.csv', 'w') as file:
        for info in temp_pen_order:
            file.write(info)

    prints_var.set(pending_orders_print)
    change_info(0)
    pending_orders_lstbx.select_set(0)


def show_stats():
    Widget['dingus'] = ttk.Label(homeframe, text='test').grid(column=1, row=1) # how to dynamically make widgets sourced from https://stackoverflow.com/questions/49195002/creating-dynamically-named-gui-objects-in-python-with-tkinter at 17:10 2023/07/23



def new_expense():

    new_expense_date = StringVar()
    new_expense_price = StringVar()
    expense = StringVar()

    todays_date = str(datetime.date.today())
    todays_date = todays_date.replace('-', '/')


    def confirm_new_expense():
        global expense, expense_lbl

        yes_no = messagebox.askyesno(message='Please confirm everything is correct')
        if yes_no:
            with open('income_expenses.csv', 'a') as file:
                file.write(
                    new_expense_edt.get() + ',' +
                    new_expense_price_edt.get() + ',' +
                    new_expense_date_edt.get() + ',' +
                    'expense' + '\n'
                )
            income_expenses.insert(0, {
                'description':new_expense_edt.get(),
                'cost':new_expense_price_edt.get(),
                'date':new_expense_date_edt.get(),
                'type':'expense'
            })
            income_expenses_print.insert(0,
                'Expense ' + new_expense_date_edt.get()
            )

            expense += int(new_expense_price_edt.get())
            profit = income - expense
            with open('inoutprofit.txt', 'w') as file:
                file.write(str(income) + ',' + str(expense))
            expense_lbl.configure(text='EXPENSE: ' + str(expense))
            profit_lbl.configure(text='PROFIT: ' + str(profit))

            cancel()
        if list_change_cmbx.current() == 1:
            prints_var.set(income_expenses_print)


    def cancel():
        print(new_expense_date)
        expense.set('')
        new_expense_price.set('')
        add_expense_window.destroy()

    add_expense_window = Toplevel(root)
    add_expense_window.resizable(FALSE,FALSE)
    add_expense_window.protocol("WM_DELETE_WINDOW", cancel)
    add_expense_frame = ttk.Frame(add_expense_window)
    add_expense_frame.grid(column=0, row=0, sticky=(N,E,S,W))

    cancel_expense_btn = ttk.Button(add_expense_frame, text='Cancel', command=cancel)
    cancel_expense_btn.grid(column=1, row=3, sticky=E, pady=10)

    add_expense_btn = ttk.Button(add_expense_frame, text='Add')
    add_expense_btn.grid(column=0, row=3, pady=10)
    add_expense_btn.configure(text='Add', command=confirm_new_expense)

    add_expense_window.title('Add New Expense')

    new_expense_edt = ttk.Entry(add_expense_frame, textvariable=expense)
    new_expense_edt.grid(column=1, row=0)


    new_expense_price_edt = ttk.Entry(add_expense_frame, textvariable=new_expense_price)
    new_expense_price_edt.grid(column=1, row=1)

    new_expense_edt.focus()
    new_expense_edt.bind('<Return>', lambda *args: new_expense_price_edt.focus())
    new_expense_price_edt.bind('<Return>', lambda *args: new_expense_date_edt.focus())

    new_expense_date_edt = ttk.Entry(add_expense_frame, textvariable=new_expense_date)
    new_expense_date_edt.grid(column=1, row=2)
    new_expense_date_edt.bind('<Return>', lambda *args: confirm_new_expense())
    new_expense_date_edt.insert(0, todays_date)

    new_expense_date_txt = ttk.Label(add_expense_frame, text='Date:')
    new_expense_date_txt.grid(column=0, row=2, sticky=E)

    new_expense_txt = ttk.Label(add_expense_frame, text='Description:')
    new_expense_txt.grid(column=0, row=0, sticky=E)

    new_expense_price_txt = ttk.Label(add_expense_frame, text='Price:')
    new_expense_price_txt.grid(column=0, row=1, sticky=E)


def add_new_print(*args):
    global print_type
    global print_type_list
    global available_prints
    global print_type_cmbx
    new_print = StringVar()
    new_print_price = StringVar()

    def confirm_new_print(*args):

        new_print_type = new_print_edt.get()
        new_print_type = new_print_type.title()
        length = len(print_type_cmbx['values'])-2
        print_type_list.insert(length, new_print_type)
        available_prints.append({'print': new_print_type, 'price': new_print_price_edt.get()})
        print_type_cmbx['values'] = tuple(print_type_list)
        print_type_cmbx.current(length)
        price_edt.delete(0, 'end')
        price_edt.insert(0, str(available_prints[length]['price']))

        with open('prints.csv', 'a') as file:
            file.write(new_print_edt.get() + ',' + new_print_price_edt.get() + '\n')
            file.close()

        new_print_edt.delete(0, 'end')
        add_print_window.destroy()
        print(print_type)


    def confirm_rem_print(*args):
        available_prints.pop(rem_print_cmbx.current())
        rem_print_type.pop(rem_print_cmbx.current())

        with open('prints.csv', 'w') as file:
            for print in available_prints:
                file.write(print['print'] + ',' + print['price'] + '\n')

        rem_print_type.append('Add...')
        rem_print_type.append('Rem...')
        print_type_cmbx['values'] = tuple(rem_print_type)
        print_type_cmbx.current(0)

        price_edt.delete(0, 'end')
        price_edt.insert(0, str(available_prints[0]['price']))


        add_print_window.destroy()

    def cancel():
        try:
            new_print_edt.delete(0, 'end')
        except NameError:
            pass

        add_print_window.destroy()
        print_type_cmbx.current(0)


    if print_type_cmbx.current() >= (len(print_type_cmbx['values'])-2):
        add_print_window = Toplevel(root)
        add_print_window.resizable(FALSE,FALSE)
        add_print_window.protocol("WM_DELETE_WINDOW", cancel)
        add_print_frame = ttk.Frame(add_print_window)
        add_print_frame.grid(column=0, row=0, sticky=(N,E,S,W))

        cancel_print_btn = ttk.Button(add_print_frame, text='Cancel', command=cancel)
        cancel_print_btn.grid(column=1, row=2, sticky=E, pady=10)

        add_print_btn = ttk.Button(add_print_frame, text='')
        add_print_btn.grid(column=0, row=2, pady=10)

    if print_type_cmbx.current() == (len(print_type_cmbx['values'])-2):
        add_print_btn.configure(text='Add', command=confirm_new_print)

        add_print_window.title('Add New Print')

        new_print_edt = ttk.Entry(add_print_frame, textvariable=new_print)
        new_print_edt.grid(column=1, row=0)
        new_print_price_edt = ttk.Entry(add_print_frame, textvariable=new_print_price)
        new_print_price_edt.grid(column=1, row=1)
        new_print_edt.focus()
        new_print_edt.bind('<Return>', lambda *args: new_print_price_edt.focus())
        new_print_price_edt.bind('<Return>', confirm_new_print) #return bind sourced at 17:10 2023/07/04 from https://www.tutorialspoint.com/how-to-bind-the-enter-key-to-a-tkinter-window#:~:text=To%20bind%20the%20key,full%20control%20over%20the%20events.

        new_print_txt = ttk.Label(add_print_frame, text='Enter:')
        new_print_txt.grid(column=0, row=0)

        new_print_price_txt = ttk.Label(add_print_frame, text='Price:')
        new_print_price_txt.grid(column=0, row=1)

    elif print_type_cmbx.current() == (len(print_type_cmbx['values'])-1):
        add_print_window.title('Remove Print')

        add_print_btn.configure(text='Remove', command=confirm_rem_print)

        rem_print_cmbx = ttk.Combobox(add_print_frame)
        rem_print_cmbx.grid(column=0, row=0, columnspan=2)
        rem_print_cmbx.bind('<Return>', confirm_rem_print)
        rem_print_cmbx.state(['readonly'])
        rem_print_cmbx.focus()

        rem_print_type = print_type_list
        rem_print_type.pop(len(rem_print_type)-1)
        rem_print_type.pop(-1)
        rem_print_cmbx['values'] = tuple(rem_print_type)

        rem_print_cmbx.current(0)
        rem_print_cmbx.bind('<Return>', confirm_rem_print)

    else:
        price_edt.delete(0, 'end')
        price_edt.insert(0, str(available_prints[print_type_cmbx.current()]['price']))


def cancel_new_order():
    remove_order_btn.configure(text='Remove', command=remove_order)
    order_info_lbl.configure(text='ORDER INFORMATION:')
    add_order_btn.configure(text='Add Order', command=add_order)
    print_type_cmbx.grid_forget()
    edit_btn.grid(column=3, row=3, sticky=(W,S), padx=9, pady=8, rowspan=2)

    price_edt.delete(0, 'end')
    address_edt.delete(0, 'end')
    name_edt.delete(0, 'end')

    pending_orders_lstbx['state'] = NORMAL
    remove_order_btn['state'] = NORMAL
    order_complete_btn['state'] = NORMAL
    new_expense_btn['state'] = NORMAL

    pending_orders_lstbx.selection_set(0)
    change_info(0)


def change_info(selected, *args):
    global current_selection
    expense = False

    def reset():
            name_edt.grid(column=0, row=2, sticky=W)
            buyer_name_lbl.grid(column=0, row=1, sticky=W, pady=2)

            filament_type_cmbx.grid(column=2, row=2, sticky=E)
            filament_type_lbl.grid(column=2, row=1, sticky=E)

            address_edt.grid(column=0, row=4, sticky=W)
            address_lbl.grid(column=0, row=3, sticky=W, pady=2)

            color_cmbx.grid(column=2, row=4, sticky=E)
            color_lbl.grid(column=2, row=3, sticky=E)

            del_col_cmbx.grid(column=2, row=6, sticky=E)
            del_col_lbl.grid(column=2, row=5, sticky=E)

            date_txt.grid(column=0, row=7, sticky=W, pady=2)
            date_edt.grid(column=0, row=8, sticky=W)

            complete_date.grid(column=2, row=8, sticky=E)
            complete_date.configure(width=10)
            complete_date_txt.grid(column=2, row=7, sticky=E)

            order_info_lbl.configure(text='ORDER INFORMATION:')

            address_lbl.configure(text='Address:')
            price_lbl.configure(text='Price:')

    if list_change_cmbx.current() == 0:
        current_list = pending_orders
        if len(name_edt.grid_info()) == 0:
            reset()
    else:
        current_list = income_expenses

        try:
            expense = False
            complete_date_var.set(current_list[selected]['complete_date'])
        except KeyError:
            expense = True

    if len(current_list) > 0:
        if expense == False:
            if len(name_edt.grid_info()) == 0:
                reset()

            current_selection = selected
            name_edt.delete(0, 'end')
            address_edt.delete(0, 'end')
            price_edt.delete(0, 'end')
            date_edt.delete(0, 'end')

            name_edt.insert(0, current_list[selected]['name'])
            address_edt.insert(0, current_list[selected]['address'])
            price_edt.insert(0, current_list[selected]['price'])
            date_edt.insert(0, current_list[selected]['date'])

            for i in range(len(filament_type)-1):
                if filament_type[i] == (current_list[selected]['filament'] + '\n'):
                    filament_type_cmbx.current(i)
                    found = True
                    break
                else:
                    found = False
            if found == False:
                messagebox.showinfo(message='Filament not found, defaulting to first filament')
                filament_type_cmbx.current(0)

            for i in range(len(filament_colors)-1):
                if filament_colors[i] == (current_list[selected]['color']) or filament_colors[i] == (current_list[selected]['color'] + '\n'):
                    color_cmbx.current(i)
                    found = True
                    break
                else:
                    found = False
            if found == False:
                messagebox.showinfo(message='Color not found, defaulting to first color')
                color_cmbx.current(0)

            if current_list[selected]['collect_deliver'] == 'Deliver':
                del_col_cmbx.current(0)
            elif current_list[selected]['collect_deliver'] == 'Collect':
                del_col_cmbx.current(1)

        else:
            if len(name_edt.grid_info()) > 0:
                name_edt.grid_forget()
                buyer_name_lbl.grid_forget()
                filament_type_lbl.grid_forget()
                filament_type_cmbx.grid_forget()
                color_cmbx.grid_forget()
                color_lbl.grid_forget()
                del_col_cmbx.grid_forget()
                del_col_lbl.grid_forget()
                complete_date.grid_forget()
                complete_date_txt.grid_forget()

                order_info_lbl.configure(text='EXPENSE INFORMATION:')

                address_edt.grid(columnspan=2, sticky=(W, E))
                address_lbl.configure(text='Information:')
                price_lbl.configure(text='Cost:')

            address_edt.delete(0, 'end')
            address_edt.insert(0, current_list[selected]['description'])

            price_edt.delete(0, 'end')
            price_edt.insert(0, current_list[selected]['cost'])

            date_edt.delete(0, 'end')
            date_edt.insert(0, current_list[selected]['date'])


def add_fil_type(*args):


    def confirm_new_fil(*args):
        global filament_type
        global filament_type_cmbx

        new_filament_type = new_filament_edt.get()
        new_filament_type = new_filament_type.upper()
        length = len(filament_type_cmbx['values'])-2
        filament_type.insert(length, new_filament_type + '\n')
        filament_type_cmbx['values'] = tuple(filament_type)
        filament_type_cmbx.current(length)

        with open('filaments.txt', 'a') as file:
            file.write(new_filament_edt.get() + '\n')



        new_filament_edt.delete(0, 'end')
        add_filament_window.destroy()
        print(filament_type)


    def confirm_rem_fil(*args):
        filament_type.pop(rem_filament_cmbx.current())

        with open('filaments.txt', 'w') as file:
            for filament in filament_type:
                file.write(filament)

        filament_type.append('Add...')
        filament_type.append('Rem...')
        filament_type_cmbx['values'] = tuple(filament_type)
        filament_type_cmbx.current(0)

        add_filament_window.destroy()

    def cancel():
        try:
            new_filament_edt.delete(0, 'end')
        except NameError:
            pass

        add_filament_window.destroy()
        filament_type_cmbx.current(0)


    if filament_type_cmbx.current() >= (len(filament_type_cmbx['values'])-2):
        add_filament_window = Toplevel(root)
        add_filament_window.resizable(FALSE,FALSE)
        add_filament_window.protocol("WM_DELETE_WINDOW", cancel)
        add_fil_frame = ttk.Frame(add_filament_window)
        add_fil_frame.grid(column=0, row=0, sticky=(N,E,S,W))

        cancel_fil_btn = ttk.Button(add_fil_frame, text='Cancel', command=cancel)
        cancel_fil_btn.grid(column=1, row=1, sticky=E, pady=10)

        add_fil_btn = ttk.Button(add_fil_frame, text='')
        add_fil_btn.grid(column=0, row=1, pady=10)

    if filament_type_cmbx.current() == (len(filament_type_cmbx['values'])-2):
        add_fil_btn.configure(text='Add', command=confirm_new_fil)

        add_filament_window.title('Add New Filament')

        new_filament_edt = ttk.Entry(add_fil_frame, textvariable=new_filament)
        new_filament_edt.grid(column=1, row=0)
        new_filament_edt.focus()
        new_filament_edt.bind('<Return>', confirm_new_fil) #return bind sourced at 17:10 2023/07/04 from https://www.tutorialspoint.com/how-to-bind-the-enter-key-to-a-tkinter-window#:~:text=To%20bind%20the%20key,full%20control%20over%20the%20events.

        new_filament_txt = ttk.Label(add_fil_frame, text='Enter:')
        new_filament_txt.grid(column=0, row=0)

    elif filament_type_cmbx.current() == (len(filament_type_cmbx['values'])-1):
        add_filament_window.title('Remove Filament')

        add_fil_btn.configure(text='Remove', command=confirm_rem_fil)

        rem_filament_cmbx = ttk.Combobox(add_fil_frame)
        rem_filament_cmbx.grid(column=0, row=0, columnspan=2)
        rem_filament_cmbx.bind('<Return>', confirm_rem_fil)
        rem_filament_cmbx.state(['readonly'])
        rem_filament_cmbx.focus()

        rem_filament_type = filament_type
        rem_filament_type.pop(len(rem_filament_type)-1)
        rem_filament_type.pop(-1)
        rem_filament_cmbx['values'] = tuple(rem_filament_type)

        rem_filament_cmbx.current(0)
        rem_filament_cmbx.bind('<Return>', confirm_rem_fil)


def add_color_type(*args):

    def confirm_new_col(*args):
        global filament_colors
        global color_cmbx

        new_color = new_color_edt.get()
        new_color = new_color.title()
        length = len(color_cmbx['values'])-2
        filament_colors.insert(length, new_color)
        color_cmbx['values'] = tuple(filament_colors)
        color_cmbx.current(length)

        with open('colors.txt', 'a') as file:
            file.write(new_color_edt.get().title() + '\n')
            file.close()

        new_color_edt.delete(0, 'end')
        add_color_window.destroy()


    def confirm_rem_col(*args):
        filament_colors.pop(rem_color_cmbx.current())

        with open('colors.txt', 'w') as file:
            for color in filament_colors:
                file.write(color)

        filament_colors.append('Add...')
        filament_colors.append('Rem...')
        color_cmbx['values'] = tuple(filament_colors)
        color_cmbx.current(0)

        add_color_window.destroy()

    def cancel():
        try:
            new_color_edt.delete(0, 'end')
        except NameError:
            pass

        add_color_window.destroy()
        color_cmbx.current(0)


    if color_cmbx.current() >= (len(color_cmbx['values'])-2):
        add_color_window = Toplevel(root)
        add_color_window.resizable(FALSE,FALSE)
        add_color_window.protocol("WM_DELETE_WINDOW", cancel)
        add_col_frame = ttk.Frame(add_color_window)
        add_col_frame.grid(column=0, row=0, sticky=(N,E,S,W))

        cancel_col_btn = ttk.Button(add_col_frame, text='Cancel', command=cancel)
        cancel_col_btn.grid(column=1, row=1, sticky=E, pady=10)

        add_col_btn = ttk.Button(add_col_frame, text='')
        add_col_btn.grid(column=0, row=1, pady=10)

    if color_cmbx.current() == (len(color_cmbx['values'])-2):
        add_col_btn.configure(text='Add', command=confirm_new_col)

        add_color_window.title('Add New Color')

        new_color_edt = ttk.Entry(add_col_frame, textvariable=new_filament)
        new_color_edt.grid(column=1, row=0)
        new_color_edt.focus()
        new_color_edt.bind('<Return>', confirm_new_col) #return bind sourced at 17:10 2023/07/04 from https://www.tutorialspoint.com/how-to-bind-the-enter-key-to-a-tkinter-window#:~:text=To%20bind%20the%20key,full%20control%20over%20the%20events.

        new_color_txt = ttk.Label(add_col_frame, text='Enter:')
        new_color_txt.grid(column=0, row=0)

    elif color_cmbx.current() == (len(color_cmbx['values'])-1):
        add_color_window.title('Remove Filament')

        add_col_btn.configure(text='Remove', command=confirm_rem_col)

        rem_color_cmbx = ttk.Combobox(add_col_frame)
        rem_color_cmbx.grid(column=0, row=0, columnspan=2)
        rem_color_cmbx.bind('<Return>', confirm_rem_col)
        rem_color_cmbx.state(['readonly'])
        rem_color_cmbx.focus()

        rem_color_type = filament_colors
        rem_color_type.pop(len(rem_color_type)-1)
        rem_color_type.pop(-1)
        rem_color_cmbx['values'] = tuple(rem_color_type)

        rem_color_cmbx.current(0)
        rem_color_cmbx.bind('<Return>', confirm_rem_col)


def list_change(*args):
    print('test')
    if list_change_cmbx.current() == 1:
        add_order_btn['state'] = DISABLED
        remove_order_btn['state'] = DISABLED
        order_complete_btn['state'] = DISABLED
        edit_btn['state'] = DISABLED

        prints_var.set(income_expenses_print)

        complete_date_txt.grid(column=2, row=7, sticky=E)

        complete_date.grid(column=2, row=8, sticky=E)
        complete_date.configure(width=10)

        pending_orders_lstbx.select_set(0)
        change_info(0)

    elif list_change_cmbx.current() == 0:
        add_order_btn['state'] = NORMAL
        remove_order_btn['state'] = NORMAL
        order_complete_btn['state'] = NORMAL
        edit_btn['state'] = NORMAL

        prints_var.set(pending_orders_print)

        complete_date.grid_forget()
        complete_date_txt.grid_forget()

        pending_orders_lstbx.select_set(0)
        change_info(0)


if __name__ == '__main__':
    main()
    root = Tk()
    root.title('3D Printing Manager')
    root.resizable(FALSE,FALSE)

    homeframe = ttk.Frame(root)
    homeframe.grid(column=0, row=0, sticky=(N, E, S, W))

    # entry validation

    def validate_price(newval):
        validation = re.match('^[0-9]*$', newval) is not None
        return(validation)
    validate_price_wrapper = (root.register(validate_price), '%P')


    # listbox
    prints_var = StringVar(value=pending_orders_print)
    pending_orders_lstbx = Listbox(homeframe, height=12, width=26, listvariable=prints_var)
    pending_orders_lstbx.grid(column=0, row=1, columnspan=2, sticky=N)
    pending_orders_lstbx.selection_set(0)

    # scroll box
    scroll_lstbx = ttk.Scrollbar(homeframe, orient=VERTICAL, command=pending_orders_lstbx.yview)
    scroll_lstbx.grid(column=2, row=1, sticky=(N, S, W))
    pending_orders_lstbx.configure(yscrollcommand=scroll_lstbx.set)

    # buttons under listbox
    add_order_btn = ttk.Button(homeframe, text='Add Order', command=add_order)
    add_order_btn.grid(column=0, row=3, sticky=S, pady=5)
    remove_order_btn = ttk.Button(homeframe, text='Remove', command=remove_order)
    remove_order_btn.grid(column=1, row=3, sticky=S, pady=5)
    order_complete_btn = ttk.Button(homeframe, text='Complete', command=order_complete)
    order_complete_btn.grid(column=0, row=4, sticky=N)
    new_expense_btn = ttk.Button(homeframe, text='Expense', command=new_expense)
    new_expense_btn.grid(column=1, row=4, sticky=N)

    #list changer
    pending_previous = StringVar()
    list_change_cmbx = ttk.Combobox(homeframe, textvariable=pending_previous)
    list_change_cmbx.grid(column=0, row=2, sticky=(N,W,E), columnspan=2)
    list_change_cmbx['values'] = ('Pending Orders', 'Income/Expenses')
    list_change_cmbx.state(['readonly'])
    list_change_cmbx.current(0)
    #list_change_cmbx.configure(width=23)

    # colored labels detailing income, expense, profit
    income_lbl = ttk.Label(homeframe, text=('INCOME: ' + str(income)), foreground=('#52b24d'))
    income_lbl.grid(column=3, row=5, padx=10) # sourced how to change colours from https://stackoverflow.com/questions/64290131/how-to-change-the-text-color-using-tkinter-label at 16:10 2023/06/28
    expense_lbl = ttk.Label(homeframe, text=('EXPENSES: ' + str(expense)), foreground='#FF0000')
    expense_lbl.grid(column=4, row=5, sticky=E)
    profit_lbl = ttk.Label(homeframe, text=('PROFIT: ' + str(profit)), foreground='#d112ed')
    profit_lbl.grid(column=5, row=5, sticky=E, padx=10)


    # order information
    order_info_frame = ttk.Frame(homeframe)
    order_info_frame.grid(column=3, row=1, sticky=(N, W, S, E), padx=5, columnspan=3, rowspan=4)
    order_info_frame.configure(borderwidth=5, relief='solid')

    order_info_lbl = ttk.Label(order_info_frame, text='ORDER INFORMATION:', font=20) # how to change font size sourced from https://www.tutorialspoint.com/how-to-change-the-size-of-text-on-a-label-in-tkinter#:~:text=If%20you%20want%20to%20change,property%20in%20the%20widget%20constructor. at 17:13 2023/06/28
    order_info_lbl.grid(column=0, row=0, sticky=(W, N), pady=10)
    name_lbl = ttk.Label(homeframe)
    order_info_frame.grid_propagate(False)
    order_info_frame.columnconfigure(1, weight=1, uniform='column') # sourced from https://stackoverflow.com/questions/58042901/prevent-tkinter-grid-from-dynamically-resizing-cells at 12:01 2023/06/29

    #Buyers name
    buyer_name = StringVar()
    name_edt = ttk.Entry(order_info_frame, textvariable=buyer_name, width=20)
    name_edt.grid(column=0, row=2, sticky=W)

    buyer_name_lbl = ttk.Label(order_info_frame, text='Buyer Name:')
    buyer_name_lbl.grid(column=0, row=1, sticky=W, pady=2)

    #Filament Type
    filament_type_var = StringVar()
    filament_type_cmbx = ttk.Combobox(order_info_frame, textvariable=filament_type_var)
    filament_type_cmbx['values'] = tuple(filament_type)
    filament_type_cmbx.state(['readonly'])
    filament_type_cmbx.current(0)
    filament_type_cmbx.configure(width=7)
    filament_type_cmbx.grid(column=0, row=2, sticky=E, columnspan=3)

    filament_type_lbl = ttk.Label(order_info_frame, text='Filament:')
    filament_type_lbl.grid(column=0, row=1, sticky=E, columnspan=3)

    #address
    address_var = StringVar()
    address_edt = ttk.Entry(order_info_frame, textvariable=address_var, width=20)
    address_edt.grid(column=0, row=4, sticky=W)

    address_lbl = ttk.Label(order_info_frame, text='Address')
    address_lbl.grid(column=0, row=3, sticky=W, pady=2)

    #color
    color_var = StringVar()
    color_cmbx = ttk.Combobox(order_info_frame, textvariable=color_var)
    color_cmbx['values'] = filament_colors
    color_cmbx.state(['readonly'])
    color_cmbx.current(0)
    color_cmbx.configure(width=7)
    color_cmbx.grid(column=0, row=4, sticky=E, columnspan=3)

    color_lbl = ttk.Label(order_info_frame, text='Color')
    color_lbl.grid(column=0, row=3, sticky=E, columnspan=3)

    #Price
    price_var = StringVar()
    price_edt = ttk.Entry(order_info_frame, textvariable=price_var, validate='key', validatecommand=validate_price_wrapper)
    price_edt.grid(column=0, row=6, sticky=W)

    price_lbl = ttk.Label(order_info_frame, text='Price:')
    price_lbl.grid(column=0, row=5, sticky=W, pady=2)

    #collect or deliver
    del_col = StringVar()
    del_col_cmbx = ttk.Combobox(order_info_frame, textvariable=del_col)
    del_col_cmbx['values'] = ('Deliver', 'Collect')
    del_col_cmbx.current(0)
    del_col_cmbx.configure(width=7)
    del_col_cmbx.grid(column=0, row=6, sticky=E, columnspan=3)

    del_col_lbl = ttk.Label(order_info_frame, text='Deliver/Collect')
    del_col_lbl.grid(column=0, row=5, sticky=E, columnspan=3)

    #Date
    date_txt = ttk.Label(order_info_frame, text='Date Placed:')
    date_txt.grid(column=0, row=7, sticky=W, pady=2)

    date = StringVar()
    date_edt = ttk.Entry(order_info_frame, textvariable=date)
    date_edt.grid(column=0, row=8, sticky=W)

    # Complete date
    complete_date_txt = ttk.Label(order_info_frame, text='Completed:')
    complete_date_var = StringVar()
    complete_date = ttk.Entry(order_info_frame, textvariable=complete_date_var)

    # edit button
    edit_btn = ttk.Button(homeframe, command=edit_order, text='Edit')
    edit_btn.grid(column=3, row=3, sticky=(W,S), padx=9, pady=8, rowspan=2)

    #function variables
    print_type = StringVar()
    new_filament = StringVar()

    #add/rem filament type
    filament_type_cmbx.bind('<<ComboboxSelected>>', add_fil_type)

    #add/rem color type
    color_cmbx.bind('<<ComboboxSelected>>', add_color_type)

    # add order var
    print_type_cmbx = ttk.Combobox(homeframe, textvariable=print_type)

    # listbox bindings
    print(pending_orders_lstbx.curselection())
    change_info(0)
    pending_orders_lstbx.bind("<<ListboxSelect>>", lambda *args: change_info(pending_orders_lstbx.curselection()[0]))
    current_selection = 0

    # change between pending orders and expenses/finished orders
    list_change_cmbx.bind('<<ComboboxSelected>>', list_change)

    root.mainloop()