from models import *


def get_all_expenses_name():
    all_expenses = Expense.select()
    all = []
    for el in all_expenses:
        all.append(el.name)
    return all


def get_all_payments():
    all_payments = Payment.select().join(Expense)
    return all_payments


def get_most_common_item(f=0):
    quantity = {}
    all_payments = get_all_payments()
    for p in all_payments:
        id = p.payment_id
        if id in quantity:
            if not f:
                quantity[id]['count'] += 1
            else:
                quantity[id]['count'] += p.amount
        else:
            if not f:
                quantity[id] = {'count': 1, 'name': Expense[p.payment_id]}
            else:
                quantity[id] = {'count': p.amount, 'name': Expense[p.payment_id]}

    return max(quantity.values(), key=lambda x: x['count'])['name'].name


def get_most_expensive_item():
    return get_most_common_item(1)


def get_most_expensive_month(f=1):
    quantity = {}
    all_payments = get_all_payments()
    for p in all_payments:
        date = p.payment_date
        if f:
            date = date.strftime("%B")
        else:
            date = date.strftime("%A")
            pass

        if date in quantity:
            quantity[date]['count'] += p.amount
        else:
            quantity[date] = {'count': p.amount, 'name': date}
    return max(quantity.values(), key=lambda x: x['count'])['name']


def get_most_expensive_day():
    return get_most_expensive_month(0)


def create_new_form(name, amount, date):
    p_id = Expense.select().where(Expense.name == name)
    try:
        p_id = p_id[0]
    except IndexError:
        Expense(name=name).save()
        all_id = Expense.select()
        p_id = all_id[len(all_id) - 1]
    Payment(amount=amount, payment_date=date, payment_id=p_id).save()


def delete_form(id_item):
    s = Payment.select().where(Payment.id == id_item)
    expenses_id = s[0].payment_id
    if len(Payment.select().where(Payment.payment_id == expenses_id)) == 1:
        expenses_to_del = Expense.get(Expense.id == expenses_id)
        expenses_to_del.delete_instance()
    obj = Payment.get(Payment.id == id_item)
    obj.delete_instance()


def get_amount_for_month():
    amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    all_payments = get_all_payments()
    for p in all_payments:
        date = p.payment_date
        date = date.month - 1
        amount[date] += p.amount
    return amount


def get_all_expenses_dict():
    all_expenses = {}
    all_payments = get_all_payments()
    for el in all_payments:
        if Expense[el.payment_id].name in all_expenses:
            all_expenses[Expense[el.payment_id].name] += el.amount
        else:
            all_expenses[Expense[el.payment_id].name] = el.amount
    all_amount = list(all_expenses.values())
    all_name = list(all_expenses.keys())
    for i in range(0,len(all_name)):
        all_name[i] += ' ('+str(int(all_amount[i]))+')'
    return all_name,all_amount



