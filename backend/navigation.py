"""
navigation.py — Main Navigation & Menus
Home screen, top-level choice dispatcher, user menu, and About Us section.
"""

import time
import sys
from matplotlib import pyplot as mpt
from PIL import Image

from backend.db import cursor
from backend.auth import signin, signup
from backend.admin import admin
from backend.orders import neworder, modiorder, canorder, trackorder, vieworder
from backend.profile import profile


def abtus():
    """About Us section — company info and feedback pie chart."""
    print("+-----------------+")
    print("|  1. Who We are  |")
    print("|  2. Feedbacks   |")
    print("|  3. Home        |")
    print("+-----------------+")
    ch35 = input("Enter choice")
    if ch35 == '1':
        f1 = open('AboutUs.txt', 'r')
        l = f1.read()
        print(l)
        f1.close()
        time.sleep(5)
        abtus()
    elif ch35 == '2':
        e = 0
        m = 0
        b = 0
        cursor.execute("select review from feedback")
        data = cursor.fetchall()
        for i in data:
            if i[0] == 'excellent':
                e += 1
            elif i[0] == 'moderate':
                m += 1
            elif i[0] == 'bad':
                b += 1
        con2 = [e, m, b]
        zones = ['Excellent', 'Modetrate', 'Bad']
        mpt.axis('equal')
        col = ['blue', '']
        expl = [0, 0, 0]
        mpt.pie(con2, labels=zones, autopct='%1.1F%%', explode=expl)
        mpt.legend(loc='upper right')
        mpt.show()
        time.sleep(5)
        abtus()
    elif ch35 == '3':
        time.sleep(2)
        home()
    else:
        print("+-----------------+")
        print("|  Invalid Input  |")
        print("+-----------------+")
        time.sleep(2)
        abtus()


def menu():
    """Main user menu after successful login."""
    from backend.auth import urid
    val = (urid,)
    query = "select username from user where userid = %s"
    cursor.execute(query, val)
    data = cursor.fetchall()
    print("+-------------------------+")
    print("|  Welcome", data[0][0], "  |")
    print("|  1. Place a New Order   |")
    print("|  2.Modify Your Order    |")
    print("|  3. Cancel Your Order   |")
    print("|  4. Track Your Order    |")
    print("|  5. View Your Orders    |")
    print("|  6. Account Profile     |")
    print("|  7. Sign Out            |")
    print("+-------------------------+")
    ch11 = input("Enter Choice 1/2/3/4/5")
    if ch11 == '1':
        neworder(urid)
    elif ch11 == '2':
        modiorder(urid)
    elif ch11 == '3':
        canorder(urid)
    elif ch11 == '4':
        trackorder(urid)
    elif ch11 == '5':
        vieworder(urid)
    elif ch11 == '6':
        profile(urid)
    elif ch11 == '7':
        print("+--------------+")
        print("|  Signed Out  |")
        print("+--------------+")
        time.sleep(1)
        home()
    else:
        print("+-----------------+")
        print("|  Invalid Input  |")
        print("+-----------------+")
        menu()
        time.sleep(1)


def choice():
    """Dispatch the home-screen choice."""
    ch = (input("Please Enter choice 1/2/3/4/5 "))
    if ch == '1':
        time.sleep(2)
        signup()
    elif ch == '2':
        time.sleep(2)
        signin()
    elif ch == '3':
        time.sleep(2)
        admin()
    elif ch == '4':
        time.sleep(2)
        abtus()
    elif ch == '5':
        print("+-----------------------+")
        print("|  Thanks For visiting  |")
        print("+-----------------------+")
        sys.exit()
    else:
        print("+------------------------------------+")
        print("|  Invalid Inpur Please Enter Again  |")
        print("+------------------------------------+")
        time.sleep(1)
        choice()


def home():
    """Application entry point — welcome screen."""
    print("+----------------------------------+")
    print("|   Welcome to FastTrack Curior    |")
    print("+----------------------------------+")
    print("|             1. Sign up           |")
    print("|             2. Sign in           |")
    print("|             3. Admin Login       |")
    print("|             4. About Us          |")
    print("|             5. Exit              |")
    print("+----------------------------------+")
    img = Image.open('/Users/shubhthakkar/Downloads/project.png')
    img.show()
    choice()
