from models import *


def get_all_expenses(db=db):
    with db as db:
        all_expenses = Expense.select()
    return all_expenses


def get_all_payments(db=db):
    with db as db:
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
    except:
        Expense(name=name).save()
        all_id = Expense.select()
        p_id = all_id[len(all_id) - 1]
    Payment(amount=amount, payment_date=date, payment_id=p_id).save()
