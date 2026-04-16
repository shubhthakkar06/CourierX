"""
address.py — Address Management
Handles adding, selecting, viewing, and modifying delivery addresses.
"""

import time
from backend.db import con, cursor
from backend.validation import pcd, reccnm, reccno, recity, recst, revo
import backend.validation as v
from tabulate import tabulate

# ─── Forward references ───────────────────────────────────────────────────────
def _menu():
    from backend.navigation import menu
    menu()

def _profile():
    from backend.profile import profile
    profile()


# ─── Globals ──────────────────────────────────────────────────────────────────
fadd = None   # full formatted address string (new address flow)
adf  = None   # full formatted address string (select from existing)


def add(urid):
    """Collect all address fields and insert a new address row."""
    global fadd
    pcd()
    reccnm()
    reccno()
    recity()
    recst()
    revo()
    val = (urid, v.pc, v.nm, v.rcy, v.st, v.rvno, v.rno)
    print(val)
    fadd = str(v.pc) + ' ' + str(v.nm) + ' ' + str(v.rcy) + ' ' + str(v.st) + ' ' + str(v.rvno) + ' ' + str(v.rno)
    query = 'insert into addresses(userid,pincode,reciever_name,reciever_city,reciever_street,reciever_house,reciever_no) values(%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(query, val)
    con.commit()
    print("+------------------------------+")
    print("|  Address Added Successfully  |")
    print("+------------------------------+")
    time.sleep(1)
    adds(urid)


def add2():
    """Let user pick an address from the saved list by index."""
    global adf
    ch25 = input("Enter the no. of the adress you want to select from the adresses shown:")
    if ch25 == '0':
        print("+------------------------------+")
        print("|  0 is not valid Enter again  |")
        print("+------------------------------+")
        time.sleep(1)
        add2()
    else:
        cursor.execute("select * from addresses")
        data = cursor.fetchall()
        adf = ""
        for i in range(1, 7):
            adf = adf + str(data[int(ch25) - 1][i]) + "  "
        print(adf)


def addn(urid, ordersid):
    """Add a brand-new address and redirect to address-selection flow."""
    global fadd
    pcd()
    reccnm()
    reccno()
    recity()
    recst()
    revo()
    val = (urid, v.pc, v.nm, v.rcy, v.st, v.rvno, v.rno)
    fadd = ' ' + str(v.pc) + ' ' + str(v.nm) + ' ' + str(v.rcy) + ' ' + str(v.st) + ' ' + str(v.rvno) + ' ' + str(v.rno)
    query = 'insert into addresses(userid,pincode,reciever_name,reciever_city,reciever_street,reciever_house,reciever_no) values(%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(query, val)
    con.commit()
    print("+----------------------------------------------------+")
    print("|  Now you will be redirected to choose the address  |")
    print("+----------------------------------------------------+")
    time.sleep(1)
    newadd(urid, ordersid)


def newadd(urid, ordersid):
    """Show saved addresses and let user update the order address or add a new one."""
    val = (urid,)
    query = "select * from addresses where userid=%s"
    cursor.execute(query, val)
    data = cursor.fetchall()
    headers = ('UserID', 'PinCode', 'Reciever_Name', 'Reciever_City', 'Reiever_Street', 'Reciever_house', 'Reciever_Mobile')
    print(tabulate(data, headers, tablefmt='fancy_grid'))
    print("+------------------------+")
    print("|  Enter 0 to goto menu  |")
    print("+------------------------+")
    chi = input("Enter the address you want to update:")
    if int(chi) > len(data):
        print("+---------------+")
        print("|  wrong input  |")
        print("+---------------+")
        time.sleep(1)
        newadd(urid, ordersid)
    elif chi == '0':
        print("+-----------------------+")
        print('|  Redirecting to menu  |')
        print("+-----------------------+")
        time.sleep(1)
        _menu()
    else:
        print("+----------------------------------------------------------------------------+")
        print("|  You want to update this address or add new one, y for update ,n for new:  |")
        print("+----------------------------------------------------------------------------+")
        ch29 = input("")
        if ch29 == 'y' or ch29 == 'Y':
            nadf = ''
            for i in data[int(chi) - 1]:
                nadf = nadf + str(i) + '  '
            val = (nadf, ordersid)
            query = "update orders set address=%s where orderid=%s"
            cursor.execute(query, val)
            con.commit()
            print("+------------------------------+")
            print("|  Order Updated Successfully  |")
            print("+------------------------------+")
            _menu()
        elif ch29 == 'n' or ch29 == 'N':
            addn(urid, ordersid)
        else:
            print("+-----------------+")
            print("|  Invalid Input  |")
            print("+-----------------+")
            time.sleep(1)
            newadd(urid, ordersid)


def modiadd(urid, ordersid):
    """Modify a single field of the user's saved address."""
    print("+-------------------------------------+")
    print('|  1. Update pincode                  |')
    print('|  2. update reciever name            |')
    print("|  3. reciever city                   |")
    print("|  4. reciever house                  |")
    print("|  5. reciever mobile no.             |")
    print("|  6.reciever street                  |")
    print("|  Enter anything else to go to menu  |")
    print("+-------------------------------------+")
    ch30 = input("Enter Choice 1/2/3/4/5:")
    if ch30 == '1':
        pcd()
        val = (v.pc, urid)
        query = 'update addresses set pincode = %s where userid=%s'
        cursor.execute(query, val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd(urid, ordersid)
    elif ch30 == '2':
        reccnm()
        val = (v.nm, urid)
        query = 'update addresses set reciever_name = %s where userid=%s'
        cursor.execute(query, val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd(urid, ordersid)
    elif ch30 == '3':
        recity()
        val = (v.rcy, urid)
        query = 'update addresses set reciever_city = %s where userid=%s'
        cursor.execute(query, val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd(urid, ordersid)
    elif ch30 == '4':
        revo()
        val = (v.rvno, urid)
        query = 'update addresses set reciever_house = %s where userid=%s'
        cursor.execute(query, val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd(urid, ordersid)
    elif ch30 == '5':
        reccno()
        val = (v.rno, urid)
        query = 'update addresses set reciever_no = %s where userid=%s'
        cursor.execute(query, val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd(urid, ordersid)
    elif ch30 == '6':
        recst()
        val = (v.st, urid)
        query = 'update addresses set pincode = %s where userid=%s'
        cursor.execute(query, val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd(urid, ordersid)
    else:
        print("+-----------------------+")
        print("|  Redirecting to Menu  |")
        print("+-----------------------+")
        time.sleep(2)
        _menu()


def adds(urid):
    """Show addresses saved to the user's account with add-new option."""
    query = "select * from addresses where userid=%s"
    val = (urid,)
    cursor.execute(query, val)
    data = cursor.fetchall()
    headers = ('UserID', 'PinCode', 'Reciever_Name', 'Reciever_City', 'Reciever_Street', 'Reciever_House', 'Reciever_Mobile')
    print(tabulate(data, headers, tablefmt='fancy_grid'))
    if data == []:
        print("+----------------------------------------------------------------+")
        print("|  Looks like you dont have any addresses saved in your account  |")
        print("|  Wanna Add one ?                                               |")
        print("+----------------------------------------------------------------+")
        ch18 = input("Enter y/n")
        if ch18 == 'y' or ch18 == 'Y':
            add(urid)
        elif ch18 == 'n' or ch18 == 'N':
            _profile()
        else:
            print("+------------------------------+")
            print("|  Wrong Input                 |")
            print("|  Redirecting to ProfilePage  |")
            print("+------------------------------+")
            time.sleep(1)
            _profile()
    else:
        print("+-----------------------------------------+")
        print("|  Do you want to add any new addresses?  |")
        print("+-----------------------------------------+")
        ch18 = input("Enter y/n")
        if ch18 == 'y' or ch18 == 'Y':
            add(urid)
        elif ch18 == 'n' or ch18 == 'N':
            _profile()
        else:
            print("+------------------------------+")
            print("|  Wrong Input                 |")
            print("|  Redirecting to ProfilePage  |")
            print("+------------------------------+")
            time.sleep(1)
            _profile()
