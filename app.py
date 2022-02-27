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
        order_exist = (session.query(OrderInfo)
                        .filter(OrderInfo.name==dishes[dish_choice][0]).count())
        if order_exist:
            print(f'You have already order this dish')
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


def edit_order(new_customer):
    for order in new_customer.order:
        print(f'{order.name}, Qty: {order.qty}')
        choice = input(f"Enter 'e' to edit order, press enter to skip to the next dish ")
        if choice != 'e':
            continue
        while True:
            order_qty = input('What is the new order quantity? ')
            if not order_qty.isdigit() or int(order_qty) <= 0:
                print('Enter a number that is bigger that 0, try again ')
                continue
            else:               
                break
        order.qty = int(order_qty)
    session.commit()
            

def show_order(new_customer):
    total = 0
    print('You order:')
    for order in new_customer.order:
        print(order)
        total += order.price * order.qty
    print(f'Total amount: ${total/100}')


def delete_order(new_customer):
    order_ids = []
    for order in new_customer.order:
        order_ids.append(order.id)
        print(f'{order.id}. {order.name}, Qty: {order.qty}')
    while True:
        choice = input("Enter the dish number you want to delete, seperated by comma: ")
        id_str_list = choice.split(',')
        if (all([id_str.isdigit() for id_str in id_str_list]) 
            and all([int(id_str) in order_ids for id_str in id_str_list])):
            for id_str in id_str_list:
                order = session.query(OrderInfo).filter(OrderInfo.id==int(id_str)).first()
                session.delete(order)
            session.commit()
            break
        else:
            print('Please enter a number that is in the list')
            continue
          
def app():
    new_customer = Customer(name='new customer', phone='5022222222')
    session.add(new_customer)
    session.commit()
    add_order(new_customer.id)
    while True:
        choice = input("""What would you like to do?
                        \r1. Edit order
                        \r2. Delete order
                        \r3. Check out """)
        if choice not in ['1', '2', '3']:
            print('Choose a number in (1,2,3), try again')
            continue
        else: 
            break
    if choice == '1':
        edit_order(new_customer)
    if choice == '2':
        delete_order(new_customer)
    if session.query(OrderInfo).count() == 0:
        print('You have not any order. GoodBye')
        exit()
    show_order(new_customer)
    name = input('What is your name? ')
    phone = clean_phone()
    new_customer.name = name
    new_customer.phone = phone
    session.commit()
    print('Check out successfully!')

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()