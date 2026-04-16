"""
admin.py — Admin Panel
Allows an admin user to view Users, Addresses, and Orders tables.
"""

import time
from backend.db import cursor
from tabulate import tabulate

# ─── Forward reference ────────────────────────────────────────────────────────
def _home():
    from backend.navigation import home
    home()


def admenu():
    """Admin dashboard — view any table."""
    print("+-----------------------------------+")
    print("|  Welcome Admin                    |")
    print("+-----------------------------------+")
    print("|  1. Check Users Table             |")
    print("|  2. Check Addresses Table         |")
    print("|  3. Check Orders Table            |")
    print("|  Enter anything else to sign out  |")
    print("+-----------------------------------+")
    ch19 = input("Enter Choice 1/2/3")
    if ch19 == '1':
        cursor.execute("select * from user")
        data = cursor.fetchall()
        headers = ('UserID', 'UserName', 'Password', 'DOB', 'Recovery Code')
        print(tabulate(data, headers, tablefmt='fancy_grid'))
        time.sleep(5)
        admenu()
    elif ch19 == '2':
        cursor.execute("select * from Addresses")
        data = cursor.fetchall()
        headers = ('UserID', 'PinCode', 'Reciever_Name', 'Reciever_City', 'Reiever_Street', 'Reciever_house', 'Reciever_Mobile')
        print(tabulate(data, headers, tablefmt='fancy_grid'))
        time.sleep(5)
        admenu()
    elif ch19 == '3':
        cursor.execute("select * from Orders")
        data = cursor.fetchall()
        headers = ('OrderID', 'Address', 'Weight', 'Price', 'Order_Date', 'UserID')
        print(tabulate(data, headers, tablefmt='fancy_grid'))
        time.sleep(5)
        admenu()
    else:
        time.sleep(1)
        _home()


def admin():
    """Admin login flow."""
    print("+--------------------------------+")
    print("|  Enter 1. to goto Profilepage  |")
    print("+--------------------------------+")
    usrid = input("Enter Admin ID")
    if usrid.lower() == 'admin':
        print("+-----------------------------+")
        print("|  Enter 1. to goto Homepage  |")
        print("+-----------------------------+")
        aps = input("Enter Password")
        if aps.lower() == 'admin':
            print("+--------------------------+")
            print("|  Admin Login Successful  |")
            print("+--------------------------+")
            time.sleep(1)
            admenu()
        elif aps == '1':
            print("+-------------------------------+")
            print("|    Redirecting to HomePage    |")
            print("+-------------------------------+")
            time.sleep(1)
            _home()
        else:
            print("+------------------------------+")
            print("|  Wrong Password Enter Again  |")
            print("+------------------------------+")
            time.sleep(1)
            admin()
    elif usrid == '1':
        print("+-------------------------------+")
        print("|    Redirecting to HomePage    |")
        print("+-------------------------------+")
        time.sleep(1)
        _home()
    else:
        print("+------------------------------+")
        print("|  Wrong Admin ID Enter Again  |")
        print("+------------------------------+")
        time.sleep(1)
        admin()
