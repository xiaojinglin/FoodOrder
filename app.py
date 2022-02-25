from models import engine, session, Base, Customer, OrderInfo

import time


dishes = {'1': ['Beef Stew', '9.99'],
          '2': ['Curry Chicken', '8.99'],
          '3': ['Grilled Salmon', '12.99'],
          '4': ['Black Bean Soup', '6.99']
        }

def menu():
    print('\n******** Knight Catering ********\n')
    for key, value in dishes.items():
        print(f"{key}. {','.join(value)}")
    print('\n********************************\n')


def clean_phone():
    while True:
        phone = input('What is your phone number(eg: 5022002222)? ')
        if phone.isdigit() and len(phone) == 10:
            return phone
        else:
            print('Please enter a valid phone number, try again: ')
            continue


def clean_order():
    while True:
        dish_choice = input('Which number of dish do you want to order? ')
        if dish_choice not in dishes.keys():
            print(f'Please choose a number between {list(dishes.keys())}, try again')
            continue
        while True:
            dish_qty = input('How many do you want to order? ')
            if not dish_qty.isdigit() or int(dish_qty) <= 0:
                input('Enter a number that is bigger that 0, try again')
                continue
            else:
                return dishes[dish_choice], int(dish_qty)
    
def add_order(customer_id):
    while(True):
        menu()
        order = clean_order()
        name = order[0][0]
        price = int(float(order[0][1])*100)
        qty = order[1]
        new_order = OrderInfo(customer_id=customer_id, name=name, price=price, qty=qty)
        session.add(new_order)
        session.commit()
        choice = input("Enter 'c' to continue ordering or press enter to check out: ")
        if choice.lower() == 'c':
            continue
        else:
            break


def check_out(customer_id):
    order_info = session.query(OrderInfo).filter(OrderInfo.customer_id==customer_id)
    total = 0
    print('You order:')
    for order in order_info:
        print(order)
        total += order.price * order.qty
    print(f'Total amount: ${total/100}')
            
def app():
    name = input('What is your name? ')
    phone = clean_phone()
    new_customer = Customer(name=name, phone=phone)
    session.add(new_customer)
    session.commit()
    input(f'{name}, press enter to start ordering')
    add_order(new_customer.id)
    check_out(new_customer.id)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()