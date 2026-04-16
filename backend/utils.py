"""
utils.py — Shared Utility Functions
Date-difference helpers, delivery-number generator, and last-login CSV logic.
"""

import time
import csv
import random
from datetime import date
from backend.db import con, cursor

# ─── Globals shared by utils ──────────────────────────────────────────────────
x       = None   # day difference between two dates
enddate = None   # today's date object
delid   = None   # generated delivery number


def get_difference(startdate, enddate):
    """Return the number of days between two date objects (stored in global x)."""
    global x
    diff = enddate - startdate
    x = diff.days


def endindate():
    """Set global `enddate` to today's date parsed from time.ctime()."""
    global enddate
    l = time.ctime().split()
    dic = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
        '05': 'May', '06': 'Jul', '07': 'Jul', '08': 'Aug',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }
    for i in dic:
        if dic[i] == l[1]:
            m = i
    enddate = date(int(l[4]), int(m), int(l[2]))


def deliverydate():
    """Generate and store today's formatted date as the delivery date."""
    l = time.ctime().split()
    dic = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
        '05': 'May', '06': 'Jul', '07': 'Jul', '08': 'Aug',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }
    for i in dic:
        if dic[i] == l[1]:
            m = i
    global ddate
    if len(l[2]) == 1:
        l3 = '0' + l[2]
        ddate = l3 + '/' + m + '/' + l[4]
    else:
        ddate = l[2] + '/' + m + '/' + l[4]


def deliverynogen(ordersid):
    """Generate a unique 10-digit delivery tracking number for a given order."""
    global delid
    delid = random.randint(1000000000, 9999999999)
    cursor.execute("select delivery_no from delivery")
    data = cursor.fetchall()
    if (delid,) in data:
        deliverynogen(ordersid)
    else:
        deliv = 0
        cursor.execute("select orderid from delivery")
        data = cursor.fetchall()
        if (str(ordersid),) in data:
            val = (ordersid,)
            query = "select delivery_no from delivery where orderid=%s"
            cursor.execute(query, val)
            data = cursor.fetchall()
            for i in data:
                deliv = i[0]
                print("+----------------------------+")
                print("|  Mobile No.", deliv, "  |")
                print("+----------------------------+")
                break
        else:
            val = (ordersid, delid)
            query = 'insert into delivery(orderid,delivery_no) values(%s,%s)'
            cursor.execute(query, val)
            con.commit()
            print("+----------------------------+")
            print("|  Mobile No.", delid, "  |")
            print("+----------------------------+")


def lastlogin2(urid):
    """Print the last-login timestamp for urid from laslogin.csv."""
    with open('laslogin.csv', mode='r') as f:
        reader = csv.reader(f, delimiter=',')
        for i in reader:
            if i[2] == urid:
                print("+-----------------------------------------+")
                print("|  Your Last Login", i[0], i[1],           "|")
                print("+-----------------------------------------+")


def lastlogin1(urid):
    """Write the current timestamp for urid to laslogin.csv."""
    tm = time.ctime()
    tim = tm[11:19:1]
    dat = tm[4:10] + "  " + tm[20:24]
    with open('laslogin.csv', mode='w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([dat, tim, urid])
