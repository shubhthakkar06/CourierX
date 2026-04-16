"""
profile.py — User Profile Management
Displays user info and handles account updates (username, userid, password, DOB)
and account deletion.
"""

import time
from backend.db import con, cursor
from backend.validation import usr, usrid, pwd, dob
import backend.validation as v

# ─── Forward references ───────────────────────────────────────────────────────
def _home():
    from backend.navigation import home
    home()

def _menu():
    from backend.navigation import menu
    menu()

def _signin():
    from backend.auth import signin
    signin()

def _vieworder(urid):
    from backend.orders import vieworder
    vieworder(urid)

def _adds(urid):
    from backend.address import adds
    adds(urid)


# ─────────────────────────────────────────────────────────────────────────────
# Reset helpers (all require recovery code to authorise the change)
# ─────────────────────────────────────────────────────────────────────────────
def rpun(urid):
    """Reset username via recovery code."""
    print("+--------------------------------+")
    print("|  Enter 1. to goto Profilepage  |")
    print("+--------------------------------+")
    rd = int(input("To Reset your Username please enter your recoverycode"))
    if rd == '1':
        print("+------------------------------+")
        print("|  Redirecting to ProfilePage  |")
        print("+------------------------------+")
        time.sleep(1)
        profile(urid)
    cursor.execute("select recoverycode from user")
    data = cursor.fetchall()
    for i in data:
        if i == (rd,):
            print("+------------------+")
            print("|  Reset Username  |")
            print("+------------------+")
            usr()
            query = "update user set username=%s where recoverycode=%s"
            val = (v.uer, rd)
            cursor.execute(query, val)
            con.commit()
            print("+--------------------+")
            print("|  Username Changed  |")
            print("+--------------------+")
            profile(urid)


def rpdb(urid):
    """Reset date of birth via recovery code."""
    print("+--------------------------------+")
    print("|  Enter 1. to goto Profilepage  |")
    print("+--------------------------------+")
    rd = int(input("To Reset your DOB please enter your recoverycode:"))
    if rd == '1':
        print("+------------------------------+")
        print("|  Redirecting to ProfilePage  |")
        print("+------------------------------+")
        time.sleep(2)
        profile(urid)
    cursor.execute("select recoverycode from user")
    data = cursor.fetchall()
    for i in data:
        if i == (rd,):
            print("+-------------+")
            print("|  Reset DOB  |")
            print("+-------------+")
            dob()
            query = "update user set DOB=%s where recoverycode=%s"
            val = (v.db, rd)
            cursor.execute(query, val)
            con.commit()
            print("+----------------------------------+")
            print("|  Date Of Birth Has Been Changed  |")
            print("+----------------------------------+")
            time.sleep(2)
            profile(urid)


def dele(urid):
    """Delete the user account after recovery-code verification."""
    print("+--------------------------------+")
    print("|  Enter 1. to goto Profilepage  |")
    print("+--------------------------------+")
    rd = int(input("To Delete Your Account please enter your recoverycode::"))
    if rd == '1':
        print("+------------------------------+")
        print("|  Redirecting to ProfilePage  |")
        print("+------------------------------+")
        time.sleep(2)
        profile(urid)
    cursor.execute("select recoverycode from user")
    data = cursor.fetchall()
    for i in data:
        if i == (rd,):
            ch20 = input("Are You Sure You Want to Delete Your Account Enter y for yes")
            print("+----------------------------------------------------------------------------------------+")
            print("|  Anything else entered will be taken as no and you will be redicrected to profilepage  |")
            print("+----------------------------------------------------------------------------------------+")
            if ch20 == 'y' or ch20 == 'Y':
                query = "delete from user where userid = %s"
                val = (urid,)
                cursor.execute(query, val)
                con.commit()
                query = "delete from addresses where userid = %s"
                cursor.execute(query, val)
                con.commit()
                val = ("Deleted Account", urid)
                query = "update orders set userid=%s where userid=%s"
                cursor.execute(query, val)
                con.commit()
                print("+--------------------------------+")
                print("|  Account Deleted Successfully  |")
                print("+--------------------------------+")
                time.sleep(2)
                _home()
            else:
                print("+------------------------------+")
                print("|  Redirecting to ProfilePage  |")
                print("+------------------------------+")
                time.sleep(1)
                profile(urid)


# ─────────────────────────────────────────────────────────────────────────────
# Profile Page
# ─────────────────────────────────────────────────────────────────────────────
def profile(urid):
    """Display user info and offer account management options."""
    from backend.auth import rpwd, rsud
    query = "select * from user where userid=%s"
    val = (urid,)
    cursor.execute(query, val)
    data = cursor.fetchall()
    for i in data:
        print("+-------------------------------------------------------+")
        print("|  Name:", data[0][1], "                                  |")
        print("|  Email:", data[0][0], "                         |")
        print("|  Date of Birth", data[0][3], "                            |")
        print("+-------------------------------------------------------+")
        print("|  1. Change UserID    |")
        print("|  2. Change Password  |")
        print("|  3. Change Name      |")
        print("|  4. Change DOB       |")
        print("|  5. Delete Account   |")
        print("|  6. Your Orders      |")
        print("|  7. Your Address     |")
        print("|  8.Sign out          |")
        print("+----------------------+")
        ch22 = input("Press anything else to goto mainpage")
        if ch22 == '1':
            rsud()
        elif ch22 == '2':
            rpwd()
        elif ch22 == '3':
            rpun(urid)
        elif ch22 == '4':
            rpdb(urid)
        elif ch22 == '5':
            dele(urid)
        elif ch22 == '6':
            _vieworder(urid)
        elif ch22 == '7':
            _adds(urid)
        elif ch22 == '8':
            time.sleep(1)
            _home()
        else:
            time.sleep(1)
            _menu()
