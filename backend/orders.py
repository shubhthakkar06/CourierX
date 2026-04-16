"""
orders.py — Order Management
Handles placing, modifying, cancelling, tracking, and viewing courier orders.
"""

import time
import random
from datetime import date
from tabulate import tabulate

from backend.db import con, cursor
from backend.utils import get_difference, endindate, deliverynogen, deliverydate
from backend.address import add, add2, adds, newadd, modiadd

# ─── Forward references ───────────────────────────────────────────────────────
def _menu():
    from backend.navigation import menu
    menu()

# ─── Globals ──────────────────────────────────────────────────────────────────
orderid  = None   # generated order ID
ordersid = None   # selected order ID (for track/cancel/modify)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def orderidgen():
    """Generate a unique 8-digit order ID."""
    global orderid
    orderid = random.randint(10000000, 99999999)
    cursor.execute("select orderid from orders")
    data = cursor.fetchall()
    for i in data:
        if i == (orderid,):
            orderidgen()


def fedbk(orderid):
    """Collect post-delivery feedback and save to DB."""
    print("+----------------------------------------+")
    print("|  please share your experience with us  |")
    print("+----------------------------------------+")
    print("|  1. Excellent                          |")
    print("|  2. Moderate                           |")
    print("|  3. Bad                                |")
    print("+----------------------------------------+")
    ch34 = input("Enter Choice 1/2/3")
    if ch34 == '1':
        val = ('excellent', orderid)
        query = "insert into feedback(review,orderid) values(%s,%s)"
        cursor.execute(query, val)
        con.commit()
        print("+---------------------------+")
        print("|  Thanks for the feedback  |")
        print("+---------------------------+")
        time.sleep(2)
        _menu()
    elif ch34 == '2':
        val = ('moderate', orderid)
        query = "insert into feedback(review,orderid) values(%s,%s)"
        cursor.execute(query, val)
        con.commit()
        print("+---------------------------+")
        print("|  Thanks for the feedback  |")
        print("+---------------------------+")
        time.sleep(2)
        _menu()
    elif ch34 == '3':
        val = ('bad', orderid)
        query = "insert into feedback(review,orderid) values(%s,%s)"
        cursor.execute(query, val)
        con.commit()
        print("+---------------------------+")
        print("|  Thanks for the feedback  |")
        print("+---------------------------+")
        time.sleep(2)
        _menu()
    else:
        print("+-----------------+")
        print("|  invalid input  |")
        print("+-----------------+")
        time.sleep(1)
        fedbk(orderid)


# ─────────────────────────────────────────────────────────────────────────────
# Place New Order
# ─────────────────────────────────────────────────────────────────────────────
def neworder(urid):
    """Walk user through placing a new courier order."""
    print("+-------------------+")
    print("|  Press 0 to exit  |")
    print("+-------------------+")
    w = input("Enter Order Weight:")
    if w == '0':
        print("+---------------------------+")
        print("|  Redirecting You to Menu  |")
        print("+---------------------------+")
        time.sleep(2)
        _menu()
    if float(w) < 3 or float(w) > 30:
        print("+----------------------------------------------------------+")
        print("|  Minimum Weight to be placed is 3kg and maximum is 30kg  |")
        print("+----------------------------------------------------------+")
        print("|                      Enter Again                         |")
        print("+----------------------------------------------------------+")
        time.sleep(1)
        neworder(urid)
    else:
        pr = 0
        cursor.execute("select * from wtscale")
        data = cursor.fetchall()
        for i in data:
            if int(i[0]) < float(w):
                if int(i[1]) > float(w):
                    pr = i[2]
        dic3 = {3: '500', 5: '1000', 7: '1500', 9: '2000', 11: '2500', 13: '3000',
                15: '3500', 17: '4000', 19: '4500', 21: '5000', 23: '5500',
                25: '6000', 27: '6500', 29: '7000', 30: '7000'}
        for i in dic3:
            if float(w) == i:
                pr = dic3[i]
        print("+-------------------------------------------------+")
        print("|                price", pr, "                      |")
        print("+-------------------------------------------------+")
        print("select an address from your saved adresses")
        query = "select * from addresses where userid=%s"
        val = (urid,)
        cursor.execute(query, val)
        data = cursor.fetchall()
        if data == []:
            print("+-------------------------------------+")
            print("|  You dont have any addresses added  |")
            print("+-------------------------------------+")
            print("|           Add new adress            |")
            print("+-------------------------------------+")
            add(urid)
            print("+-------------------------------------------------------------------------------+")
            print("|  This Address will be used to deliver your courier                            |")
            print("|  Only Cash Payment Method is Accepted                                         |")
            print("|  Please Pay Rs", pr, " at our nearest branch when you come to drop the courier  |")
            print("|  Do You Want to Place this Order                                              |")
            print("+-------------------------------------------------------------------------------+")
            ch19 = input("Enter y/n")
            if ch19 == 'y' or ch19 == 'Y':
                from backend.address import fadd as _fadd
                orderidgen()
                deliverydate()
                from backend.utils import ddate
                print("+----------------------------------------------------------------------------------+")
                print("|  Order Placed                                                                    |")
                print("|  Order will be delivered within 5 days                                           |")
                print("|  To Cancel/Modify/Track Please goto Cancel/Modify/Track option on the mainpage   |")
                print("+----------------------------------------------------------------------------------+")
                val = (orderid, _fadd, w, pr, ddate, urid)
                query = "insert into orders(orderID,address,weight,price,order_date,userid) values(%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, val)
                con.commit()
                time.sleep(2)
                fedbk(orderid)
        else:
            headers = ('UserID', 'PinCode', 'Reciever_Name', 'Reciever_City', 'Reciever_Street', 'Reciever_House', 'Reciever_Mobile')
            print(tabulate(data, headers, tablefmt='fancy_grid'))
            print("+----------------------------+")
            print("|  Want to Add a new adress  |")
            print("+----------------------------+")
            print("+--------------------------------------------+")
            print("|  Enter y for yes and anything else for no  |")
            print("+--------------------------------------------+")
            ch24 = input("Enter Choice")
            if ch24 == 'y' or ch24 == 'Y':
                add(urid)
            else:
                add2()
                from backend.address import adf as _adf
                print("+-------------------------------------------------------------------------------+")
                print("|  This Address will be used to deliver your courier                            |")
                print("|  Only Cash Payment Method is Accepted                                         |")
                print("|  Please Pay Rs", pr, " at our nearest branch when you come to drop the courier  |")
                print("|  Do You Want to Place this Order                                              |")
                print("+-------------------------------------------------------------------------------+")
                print("+--------------------------------------------+")
                print("|  Enter y for yes and anything else for no  |")
                print("+--------------------------------------------+")
                ch19 = input("Enter Choice")
                if ch19 == 'y' or ch19 == 'Y':
                    orderidgen()
                    deliverydate()
                    from backend.utils import ddate
                    print("+----------------------------------------------------------------------------------+")
                    print("|  Order Placed                                                                    |")
                    print("|  Order will be delivered within 5 days                                           |")
                    print("|  To Cancel/Modify/Track Please goto Cancel/Modify/Track option on the mainpage   |")
                    print("+----------------------------------------------------------------------------------+")
                    val = (orderid, _adf, w, pr, ddate, urid)
                    query = "insert into orders(orderID,address,weight,price,order_date,userid) values(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(query, val)
                    con.commit()
                    time.sleep(1)
                    fedbk(orderid)
                else:
                    print("+--------------------------+")
                    print("|  Redirecting You to Menu |")
                    print("+--------------------------+")
                    time.sleep(1)
                    _menu()


# ─────────────────────────────────────────────────────────────────────────────
# View Orders
# ─────────────────────────────────────────────────────────────────────────────
def vieworder(urid):
    val = (urid,)
    query = 'select * from orders where userid=%s'
    cursor.execute(query, val)
    data = cursor.fetchall()
    headers = ('OrderID', 'Address', 'Weight', 'Price', 'Order_Date', 'UserID')
    print(tabulate(data, headers, tablefmt='fancy_grid'))
    ch31 = input("Press 1 to goto menu")
    if ch31 == '1':
        print("+-----------------------+")
        print("|  Redirecting to Menu  |")
        print("+-----------------------+")
        time.sleep(2)
        _menu()
    else:
        print("+-----------------+")
        print('|  invalid input  |')
        print("+-----------------+")
        time.sleep(2)
        vieworder(urid)


# ─────────────────────────────────────────────────────────────────────────────
# Track Order
# ─────────────────────────────────────────────────────────────────────────────
def trackorder(urid):
    global ordersid
    val = (urid,)
    query = "select * from orders where userid=%s"
    cursor.execute(query, val)
    data = cursor.fetchall()
    headers = ('OrderID', 'Address', 'Weight', 'Price', 'Order_Date', 'UserID')
    print(tabulate(data, headers, tablefmt='fancy_grid'))
    if data == []:
        print("+------------------------------------+")
        print("|  You Havent Placed Any Orders Yet  |")
        print("+------------------------------------+")
        time.sleep(1)
        _menu()
    print("+----------------------------------------------------------------+")
    print("|  Enter the no. of order you want to track, enter 0 to go back  |")
    print("+----------------------------------------------------------------+")
    ch27 = input("Choice:")
    if ch27 == '0':
        print("+-----------------------+")
        print("|  Redirecting to Menu  |")
        print("+-----------------------+")
        time.sleep(1)
        _menu()
    elif int(ch27) > len(data):
        print("+--------------------------------------+")
        print("|  Only", len(data), "Orders exist       |")
        print("|  Enter again                         |")
        print("+--------------------------------------+")
        time.sleep(1)
        trackorder(urid)
    else:
        ordersid = data[int(ch27) - 1][0]
        d2date = data[int(ch27) - 1][4]
        startdate = date(int(d2date[6:10]), int(d2date[3:5]), int(d2date[0:2]))
        endindate()
        from backend.utils import enddate
        get_difference(startdate, enddate)
        from backend.utils import x
        if x == 0:
            print("+--------------------------+")
            print('|  Order Under Proceesing  |')
            print("+--------------------------+")
            time.sleep(4)
            _menu()
        elif x == 1:
            print("+-----------------------------+")
            print('|  Order Is Under  Packaging  |')
            print("+-----------------------------+")
            time.sleep(4)
            _menu()
        elif x == 2:
            print("+--------------------------+")
            print('|  Order Is Ready To Ship  |')
            print("+--------------------------+")
            time.sleep(4)
            _menu()
        elif x == 3:
            print("+---------------------+")
            print('|  Order Is Shipped   |')
            print("+---------------------+")
            time.sleep(4)
            _menu()
        elif x == 4:
            print("+----------------------------------------------")
            print('|  Order Is Out For Delivery                  |')
            print('|  Order Is Delivered By Our Delivery Agent   |')
            print("+---------------------------------------------+")
            deliverynogen(ordersid)
        elif x >= 5:
            deliverynogen(ordersid)
            print("+--------------------------------------------------------------------------+")
            print("|  order is delivered to your selected address                             |")
            print("|  Thankyou for choosing us                                                |")
            print("|  Hope to see you again                                                   |")
            print("+--------------------------------------------------------------------------+")
            time.sleep(4)
            _menu()


# ─────────────────────────────────────────────────────────────────────────────
# Modify Order
# ─────────────────────────────────────────────────────────────────────────────
def modimenu(urid, ordersid):
    print("+-----------------------------------------+")
    print("|  You can only modify address            |")
    print("+-----------------------------------------+")
    print("|      1. Modify address                  |")
    print("+-----------------------------------------+")
    print("|  Enter 0 to go to menu or else enter 1  |")
    print("+-----------------------------------------+")
    ch27 = input("Enter Choice")
    if ch27 == '0':
        print("+-----------------------+")
        print("|  Redirecting to Menu  |")
        print("+-----------------------+")
        time.sleep(2)
        _menu()
    elif ch27 == '1':
        print("+--------------------------------------------------------------+")
        print("|  1. Change entire address by adding new address              |")
        print("|  2.Modify existing address                                   |")
        print("+--------------------------------------------------------------+")
        print("|  Enter Anything else to go to menu                           |")
        print("+--------------------------------------------------------------+")
        ch28 = input("Enter choice:")
        if ch28 == '1':
            newadd(urid, ordersid)
        elif ch28 == '2':
            modiadd(urid, ordersid)
    else:
        print("+-----------------+")
        print("|  Invalid input  |")
        print("+-----------------+")
        time.sleep(2)
        modimenu(urid, ordersid)


def modiorder(urid):
    global ordersid
    print("+-------------------------------------------------------------------+")
    print("|  Orders can be Modified only till 2 days after placing the order  |")
    print("+-------------------------------------------------------------------+")
    val = (urid,)
    query = "select * from orders where userid=%s"
    cursor.execute(query, val)
    data = cursor.fetchall()
    headers = ('OrderID', 'Address', 'Weight', 'Price', 'Order_Date', 'UserID')
    print(tabulate(data, headers, tablefmt='fancy_grid'))
    if data == []:
        print("+------------------------------------+")
        print("|  You Havent Placed Any Orders Yet  |")
        print("+------------------------------------+")
        time.sleep(2)
        _menu()
    print("+----------------------------------------------------------------+")
    print("|  Enter the no. of order you want to track, enter 0 to go back  |")
    print("+----------------------------------------------------------------+")
    ch27 = input("Enter Choice")
    if ch27 == '0':
        print("+----------------------+")
        print("|  Redirecting to Menu |")
        print("+----------------------+")
        time.sleep(1)
        _menu()
    elif int(ch27) > len(data):
        print("+-----------------------------------+")
        print("|  Only", len(data), "Orders exist    |")
        print("|  Enter again                      |")
        print("+-----------------------------------+")
        time.sleep(2)
        modiorder(urid)
    else:
        ordersid = data[int(ch27) - 1][0]
        d2date = data[int(ch27) - 1][4]
        startdate = date(int(d2date[6:10]), int(d2date[3:5]), int(d2date[0:2]))
        endindate()
        from backend.utils import enddate, x
        get_difference(startdate, enddate)
        from backend.utils import x
        if x > 2:
            print("+--------------------------------------------------------+")
            print("|  This order cant be modified as it is already shipped  |")
            print("|  Redirecting you to other orders                       |")
            print("+--------------------------------------------------------+")
            time.sleep(1)
            modiorder(urid)
        else:
            modimenu(urid, ordersid)


# ─────────────────────────────────────────────────────────────────────────────
# Cancel Order
# ─────────────────────────────────────────────────────────────────────────────
def canorder(urid):
    global ordersid
    print("+--------------------------------------------------------------------+")
    print("|  Orders can be Cancelled only till 2 days after placing the order  |")
    print("+--------------------------------------------------------------------+")
    val = (urid,)
    query = "select * from orders where userid=%s"
    cursor.execute(query, val)
    data = cursor.fetchall()
    headers = ('OrderID', 'Address', 'Weight', 'Price', 'Order_Date', 'UserID')
    print(tabulate(data, headers, tablefmt='fancy_grid'))
    if data == []:
        print("+------------------------------------+")
        print("|  You Havent Placed Any Orders Yet  |")
        print("+------------------------------------+")
        time.sleep(2)
        _menu()
    print("+-----------------------------------------------------------------+")
    print("|  Enter the no. of order you want to Cancel, enter 0 to go back  |")
    print("+-----------------------------------------------------------------+")
    ch27 = input("Enter Choice:")
    if ch27 == '0':
        _menu()
    elif int(ch27) > len(data):
        print("+-----------------------------------+")
        print("|  Only", len(data), "Orders exist    |")
        print("|  Enter again                      |")
        print("+-----------------------------------+")
        time.sleep(1)
        canorder(urid)
    else:
        ordersid = data[int(ch27) - 1][0]
        d2date = data[int(ch27) - 1][4]
        startdate = date(int(d2date[6:10]), int(d2date[3:5]), int(d2date[0:2]))
        endindate()
        from backend.utils import enddate
        get_difference(startdate, enddate)
        from backend.utils import x
        if x > 2:
            print("+--------------------------------------------------------+")
            print("|  This order cant be Cancelled as it is already shipped  |")
            print("|  Redirecting you to other orders                       |")
            print("+--------------------------------------------------------+")
            time.sleep(2)
            _menu()
        else:
            ch33 = input("Are you sire you want to cancel your order")
            print("+------------------------------------------------------+")
            print("|  Anything Else will be taken as a no and go to menu  |")
            print("+------------------------------------------------------+")
            if ch33 == 'y' or ch33 == 'Y':
                val = (ordersid,)
                query = 'delete from orders where orderid=%s'
                cursor.execute(query, val)
                con.commit()
                print("+--------------------------------+")
                print("|  Order Cancelled successfully  |")
                print("+--------------------------------+")
                time.sleep(1)
                _menu()
            else:
                print("+-----------------------+")
                print("|  Redirecting to Menu  |")
                print("+-----------------------+")
                time.sleep(1)
                _menu()
