"""
auth.py — Authentication & Account Management
Handles sign-up, sign-in, password/userid resets, and wrong-password tracking.
"""

import time
from backend.db import con, cursor
from backend.validation import usr, pwd, usrid, recd, dob
from backend.validation import uer, ps, uid, rcd, db
from backend.utils import lastlogin1, lastlogin2

# ─── Globals ──────────────────────────────────────────────────────────────────
urid  = None   # currently logged-in user's email
pdd   = None   # password entered during sign-in
data2 = None   # wrong-password attempt row


def _home():
    from backend.navigation import home
    home()

def _menu():
    from backend.navigation import menu
    menu()

def _profile():
    from backend.profile import profile
    profile()


# ─────────────────────────────────────────────────────────────────────────────
# Userid input during sign-in (not validation — just capture)
# ─────────────────────────────────────────────────────────────────────────────
def ud():
    global urid
    print("+-----------------------------+")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------+")
    urid = input("Enter Userid")
    if urid == '1':
        print("+---------------------------+")
        print("|  Redirecting You to Home  |")
        print("+---------------------------+")
        time.sleep(1)
        _home()
    urid = urid.lower()


def pds():
    global pdd
    print("+-----------------------------+")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------+")
    pdd = input("Enter Password:")
    if pdd == '1':
        print("+---------------------------+")
        print("|  Redirecting You to Home  |")
        print("+---------------------------+")
        time.sleep(1)
        _home()


# ─────────────────────────────────────────────────────────────────────────────
# Wrong-password attempt counter
# ─────────────────────────────────────────────────────────────────────────────
def rpd1():
    val = (1 + int(data2[0][0]), int(data2[0][0]))
    query = "update wpd set attemps=%s where attemps=%s"
    cursor.execute(query, val)
    con.commit()


def rpd2():
    cursor.execute("select * from wpd")
    global data2
    data2 = cursor.fetchall()
    for i in data2:
        if i[0] < 3:
            print("+-----------------------------------------+")
            print("|  Your Have", 3 - int(i[0]), "Attempts left  |")
            print("+-----------------------------------------+")
            rpd1()
            pds()
            pdw()
        else:
            print("+------------------------------------+")
            print("|  To many attempts Reset passwords  |")
            print("+------------------------------------+")
            val = (1, int(data2[0][0]))
            query = "update wpd set attemps=%s where attemps=%s"
            cursor.execute(query, val)
            con.commit()
            rpwd()


def pdw():
    """Verify the entered password against the database."""
    val = (urid,)
    query = "select password from user where userid = %s"
    cursor.execute(query, val)
    data = cursor.fetchall()
    for i in data:
        if i == (pdd,):
            print("+---------------------+")
            print('|  SignIn Successful  |')
            print("+---------------------+")
            time.sleep(1)
            cursor.execute("select attemps from wpd")
            data3 = cursor.fetchall()
            val = (1, int(data3[0][0]))
            query = "update wpd set attemps=%s where attemps=%s"
            cursor.execute(query, val)
            con.commit()
            lastlogin2(urid)
            lastlogin1(urid)
            _menu()
        else:
            print("+----------------------+")
            print("|  Incorrect Password  |")
            print("+----------------------+")
            rpd2()
            rpd1()


# ─────────────────────────────────────────────────────────────────────────────
# Password / UserID Reset (via recovery code)
# ─────────────────────────────────────────────────────────────────────────────
def rpwd():
    """Reset password using recovery code."""
    import backend.validation as v
    print("+-----------------------------+")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------+")
    rd = input("To Reset your password please enter your recoverycode:")
    if rd == '1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        _home()
    query = "select recoverycode from user where userid = %s"
    val = (urid,)
    cursor.execute(query, val)
    data = cursor.fetchall()
    for i in data:
        if i == (rd,):
            print("+------------------+")
            print("|  Reset Password  |")
            print("+------------------+")
            pwd()
            query = "update user set password=%s where recoverycode=%s"
            val = (v.ps, rd)
            cursor.execute(query, val)
            con.commit()
            print("+--------------------+")
            print("|  Password Changed  |")
            print("+--------------------+")
            time.sleep(1)
            signin()
        else:
            print("+-----------------------------------------+")
            print("|  Recoverycode Incorret                  |")
            print("|  1. Enter Again                         |")
            print("|  Anything else would take to homepage   |")
            print("+-----------------------------------------+")
            ch6 = input("Enter Choice")
            if ch6 == '1':
                rpwd()
            else:
                print("+---------------------------+")
                print("|  Redirecting You to Home  |")
                print("+---------------------------+")
                time.sleep(1)
                _home()


def rsud():
    """Reset UserID using recovery code."""
    import backend.validation as v
    print("+-----------------------------+")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------+")
    rd = input("To Reset your UserID please enter your recoverycode:")
    if rd == '1':
        print("+---------------------------+")
        print("|  Redirecting You to Home  |")
        print("+---------------------------+")
        time.sleep(1)
        _home()
    query = "select recoverycode from user where userid = %s"
    val = (urid,)
    cursor.execute(query, val)
    data = cursor.fetchall()
    for i in data:
        if i == (int(rd),):
            print("+----------------+")
            print("|  Reset Userid  |")
            print("+----------------+")
            usrid()
            query = "update user set userid=%s where recoverycode=%s"
            val = (v.uid, rd)
            cursor.execute(query, val)
            con.commit()
            print("+------------------+")
            print("|  UserID Changed  |")
            print("+------------------+")
            signin()
        else:
            print("+-----------------------------------------+")
            print("|  Recoverycode Incorret                  |")
            print("|  1. Enter Again                         |")
            print("|  Anything else would take to homepage   |")
            print("+-----------------------------------------+")
            ch6 = input("Enter Choice")
            if ch6 == '1':
                rsud()
            else:
                print("+---------------------------+")
                print("|  Redirecting You to Home  |")
                print("+---------------------------+")
                time.sleep(1)
                _home()


# ─────────────────────────────────────────────────────────────────────────────
# Sign In / Sign Up
# ─────────────────────────────────────────────────────────────────────────────
def signin():
    print("+-----------+")
    print("|  Welcome  |")
    print("+-----------+")
    ud()
    cursor.execute("select userid from user")
    data = cursor.fetchall()
    if (urid,) in data:
        pds()
        pdw()
    else:
        print("+------------------------------------------+")
        print("|  Userid Incorrect                        |")
        print("|  1. Enter Again                          |")
        print("|  2. Reset UseriD                         |")
        print("|  Anything else would take to homepage    |")
        print("+------------------------------------------+")
        ch7 = input("Enter Choice")
        if ch7 == '1':
            signin()
        elif ch7 == '2':
            print("+--------------------------------+")
            print("|  Redirecting You to ResetPage  |")
            print("+--------------------------------+")
            time.sleep(1)
            rsud()
        else:
            print("+---------------------------+")
            print("|  Redirecting You to Home  |")
            print("+---------------------------+")
            time.sleep(1)
            _home()


def signup():
    """Register a new user account."""
    import backend.validation as v
    print("+-----------+")
    print("|  Sign Up  |")
    print("+-----------+")
    usr()
    pwd()
    usrid()
    recd()
    dob()
    query = "insert into user(UserID,Username,Password,DOB,RecoveryCode) values(%s,%s,%s,%s,%s)"
    val = (v.uid, v.uer, v.ps, v.db, v.rcd)
    cursor.execute(query, val)
    con.commit()
    print("+--------------------------------+")
    print("|  Account Created Successfully  |")
    print("+--------------------------------+")
    time.sleep(1)
    signin()
