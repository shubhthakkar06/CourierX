"""
validation.py — Input Validation Helpers
All functions that validate and capture user input fields:
username, password, email/userid, recovery code, date of birth parts,
and address components.
"""

import time
from backend.db import con, cursor

# ─── Global variables set by validators ───────────────────────────────────────
uer = None   # username
ps  = None   # password
cps = None   # confirm password
uid = None   # email / userid
rcd = None   # recovery code
y   = None   # year of birth
m   = None   # month of birth
d   = None   # day of birth
db  = None   # full date of birth  (YYYY-MM-DD)
pc  = None   # pincode
nm  = None   # receiver name
rno = None   # receiver mobile number
rcy = None   # receiver city
st  = None   # receiver street / area
rvno= None   # receiver house number

# ─── Forward reference (home is defined in navigation.py) ─────────────────────
def _home():
    from backend.navigation import home
    home()


# ─────────────────────────────────────────────────────────────────────────────
# Username
# ─────────────────────────────────────────────────────────────────────────────
def usr():
    global uer
    print("+-----------------------------|")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------|")
    uer = input("Enter Username:")
    if uer == '1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        _home()
    if len(uer) < 8 or len(uer) > 31:
        print("+----------------------------------------------+")
        print("|  Username should be between 8-30 characters  |")
        print("|            Please Enter Again                |")
        print("+----------------------------------------------+")
        time.sleep(1)
        usr()
    else:
        if uer.isalpha():
            uer = uer.lower()
            print("+-----------------------------+")
            print("|       Username Taken        |")
            print("+-----------------------------+")
        elif uer.isdigit():
            print("+---------------------------------------+")
            print("|  Username should have only alphabets  |")
            print("|             Enter Again               |")
            print("+---------------------------------------+")
            time.sleep(1)
            usr()
        elif " " in uer:
            print("+-----------------------------------+")
            print("|  Username Should not have Spaces  |")
            print("+-----------------------------------+")
            time.sleep(1)
            usr()
        else:
            print("+----------------------------------------------+")
            print("|  Username should have no special characters  |")
            print("+----------------------------------------------+")
            time.sleep(1)
            usr()


# ─────────────────────────────────────────────────────────────────────────────
# Confirm Password
# ─────────────────────────────────────────────────────────────────────────────
def cpwd():
    global cps
    cps = input("Confirm Password")
    if cps == ps:
        print('+---------------------+')
        print("|   Password Taken    |")
        print('+---------------------+')
    else:
        print('+-------------------------+')
        print("|  Password doesn't match |")
        print("|  Please enter again     |")
        print("+-------------------------+")
        time.sleep(1)
        cpwd()


# ─────────────────────────────────────────────────────────────────────────────
# Password
# ─────────────────────────────────────────────────────────────────────────────
def pwd():
    global ps
    print("+-----------------------------|")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------|")
    ps = input("Enter Password")
    if ps == '1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        _home()
    if len(ps) < 8 or len(ps) > 21:
        print("+----------------------------------------------+")
        print("|  Password should be between 8-30 characters  |")
        print("|            Please Enter Again                |")
        print("+----------------------------------------------+")
        time.sleep(1)
        pwd()
    else:
        if ps.islower() or ps.isupper():
            print('+--------------------------------------------------------------------+')
            print("|  Password Should be in TitleCase- Atleast 1st letter in uppercase  |")
            print("+--------------------------------------------------------------------+")
            time.sleep(1)
            pwd()
        elif ps.isdigit():
            print('+--------------------------------------------+')
            print("|  password should have Alphabets + numbers  |")
            print("+--------------------------------------------+")
            time.sleep(1)
            pwd()
        elif " " in ps:
            print('+-----------------------------------+')
            print("|  Password Should not have Spaces  |")
            print("+-----------------------------------+")
            time.sleep(1)
            pwd()
        elif "@" not in ps:
            print('+---------------------------------+')
            print("|  Password should have @ symbol  |")
            print("+---------------------------------+")
            time.sleep(1)
            pwd()
        else:
            cpwd()


# ─────────────────────────────────────────────────────────────────────────────
# Email / UserID
# ─────────────────────────────────────────────────────────────────────────────
def usrid():
    global uid
    print("+-----------------------------|")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------|")
    uid = input("Enter your Email-id")
    if uid == '1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        _home()
    uid = uid.lower()
    if len(uid) < 8 or len(uid) > 31:
        print("+----------------------------------------------+")
        print("|  UserID should be between 8-30 characters  |")
        print("|            Please Enter Again                |")
        print("+----------------------------------------------+")
        time.sleep(1)
        usrid()
    elif " " in uid:
        print('+-----------------------------------+')
        print("|  UserID Should not have Spaces  |")
        print("+-----------------------------------+")
        time.sleep(1)
        usrid()
    else:
        if '@' not in uid:
            print("+-----------------------------------------+")
            print("|  UserID to be Of Fomrat User@gmail.com  |")
            print("+-----------------------------------------+")
            time.sleep(1)
            usrid()
        else:
            if uid[len(uid) - 4:len(uid):1] != '.com':
                print("+-----------------------------------------+")
                print("|  UserID to be of Format User@gmail.com  |")
                print("+-----------------------------------------+")
                time.sleep(1)
                usrid()
            else:
                cursor.execute("select userid from user")
                data = cursor.fetchall()
                for i in data:
                    if i == (uid,):
                        print("+------------------------+")
                        print("|  UserID Already Taken  |")
                        print("|  Please enter another  |")
                        print("+------------------------+")
                        time.sleep(1)
                        usrid()
                    else:
                        print('+----------------+')
                        print("|  UserID Taken  |")
                        print("+----------------+")
                        break


# ─────────────────────────────────────────────────────────────────────────────
# Recovery Code
# ─────────────────────────────────────────────────────────────────────────────
def recd():
    global rcd
    print('+-----------------------------------+')
    print("|     Enter 1 to go to HomePage     |")
    print("+-----------------------------------+")
    rcd = input("Enter 6 digit Recovery Code:")
    if rcd == '1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        _home()
    if len(rcd) == 6:
        if rcd.isalpha():
            print("+--------------------------+")
            print("|  Code should be numeric  |")
            print("|  Enter Again             |")
            print("+--------------------------+")
            time.sleep(1)
            recd()
        elif " " in rcd:
            print('+---------------------------------------+')
            print("|  RecoveryCode Should not have Spaces  |")
            print("+---------------------------------------+")
            time.sleep(1)
            recd()
        elif rcd.isdigit():
            cursor.execute("select recoverycode from user")
            data = cursor.fetchall()
            for i in data:
                if i == (int(rcd),):
                    print("+----------------------------------------------+")
                    print("|  RecoveryCode already taken Enter different  |")
                    print("+----------------------------------------------+")
                    time.sleep(1)
                    recd()
                else:
                    print("+----------------------+")
                    print("|  RecoveryCode Taken  |")
                    print("+----------------------+")
                    time.sleep(1)
                    break
        elif rcd.isalnum():
            print("+-----------------------------------+")
            print("|  Recovery code should be numeric  |")
            print("|  Enter again                      |")
            print("+-----------------------------------+")
            time.sleep(1)
            recd()
    else:
        print("+---------------------------------------+")
        print("|  Code should be of strictly 6 digits  |")
        print("|  Enter Again                          |")
        print("+---------------------------------------+")
        time.sleep(1)
        recd()


# ─────────────────────────────────────────────────────────────────────────────
# Date of Birth — Year / Month / Day
# ─────────────────────────────────────────────────────────────────────────────
def ye():
    global y
    print("+-----------------------------|")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------|")
    y = input("Enter Year of Birth in YYYY Fromat")
    if y == '1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        _home()
    if len(y) != 4:
        print("+---------------------------------+")
        print("|  Year should be in YYYY Format  |")
        print("+---------------------------------+")
        time.sleep(1)
        ye()
    else:
        if y.isalpha():
            print("+-------------------------------+")
            print("|  Enter Numbers not alphabets  |")
            print("+-------------------------------+")
            time.sleep(1)
            ye()
        elif y.isalnum():
            if not y.isdigit():
                print("+------------------------------+")
                print("|  Enter Number not alphabets  |")
                print("+------------------------------+")
                time.sleep(1)
                ye()


def me():
    global m
    print("+-----------------------------|")
    print("|  Enter 1 to goto Homepage   |")
    print("+-----------------------------|")
    m = input("Enter Month of Birth in MM format")
    if m == '1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        _home()
    if len(m) != 2:
        print("+--------------------------------+")
        print("|  Month should be in MM Format  |")
        print("+--------------------------------+")
        time.sleep(1)
        me()
    else:
        if m.isalpha():
            print("+---------------------------+")
            print("|  Month should be numeric  |")
            print("+--------------------------+")
            time.sleep(1)
            me()
        elif m.isdigit():
            if int(m) not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                print("+-----------------------------+")
                print("|  Month should be from 1-12  |")
                print("+-----------------------------+")
                time.sleep(1)
                me()
        elif m.isalnum():
            print("+---------------------------+")
            print("|  Month should be numeric  |")
            print("+---------------------------+")
            time.sleep(1)
            me()


def de():
    global d
    print("+-----------------------------|")
    print("|  Enter 1 to goto Homepage   |")
    print("+-----------------------------|")
    d = input("Enter Date of brith in DD Format")
    if d == '1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        _home()
    if len(d) != 2:
        print("+----------------------------+")
        print("|  Date Should of DD Format  |")
        print("+----------------------------+")
        time.sleep(1)
        de()
    else:
        if d.isalpha():
            print("+--------------------------+")
            print("|  Date Should Be Numeric  |")
            print("+--------------------------+")
            time.sleep(1)
            de()
        elif m.isdigit():
            if int(m) in [1, 3, 5, 7, 8, 10, 12]:
                if int(d) < 1 or int(d) > 31:
                    print("+-------------------------------+")
                    print("|  Date should be between 1-31  |")
                    print("+-------------------------------+")
                    time.sleep(1)
                    de()
            elif int(m) in [4, 6, 9, 11]:
                if int(d) < 1 or int(d) > 30:
                    print("+--------------------------------+")
                    print("|  Date should be between 1-30  |")
                    print("+--------------------------------+")
                    time.sleep(1)
                    de()
            elif int(m) == 2:
                if int(y) % 4 == 0:
                    if int(d) < 1 or int(d) > 29:
                        print("+----------------------------+")
                        print("|  Date Should Be From 1-29  |")
                        print("+----------------------------+")
                        time.sleep(1)
                        de()
                else:
                    if int(d) < 1 or int(d) > 28:
                        print("+----------------------------+")
                        print("|  Date Should Be From 1-28  |")
                        print("+----------------------------+")
                        time.sleep(1)
                        de()
        elif d.isalnum():
            print("+--------------------------+")
            print("|  Date Should Be Numeric  |")
            print("+--------------------------+")
            time.sleep(1)
            de()


def dob():
    global db
    ye()
    me()
    de()
    db = y + '-' + m + '-' + d


# ─────────────────────────────────────────────────────────────────────────────
# Address component validators
# ─────────────────────────────────────────────────────────────────────────────
def pcd():
    print("+------------------------------+")
    print("|  Enter Your Address Details  |")
    print("+------------------------------+")
    global pc
    pc = input("Enter Your Pincode:")
    if len(pc) != 6:
        print("+-----------------------------------+")
        print("|  Pincode should have 6 numbers    |")
        print("|  Enter Again                      |")
        print("+-----------------------------------+")
        time.sleep(1)
        pcd()
    else:
        if pc.isdigit():
            print("+------------------------------+")
            print("|  Pincode taken successfully  |")
            print("+------------------------------+")
            time.sleep(1)
        else:
            print("+-----------------------------+")
            print("|  Pincode should be numeric  |")
            print("+-----------------------------+")
            time.sleep(1)
            pcd()


def reccnm():
    global nm
    nm = input("Enter reciever Name:")
    if len(nm) > 30:
        print("+---------------------------------------------------------+")
        print("|  Reciever Name should not be more than 30 characters    |")
        print("|  Enter Again                                            |")
        print("+---------------------------------------------------------+")
        time.sleep(1)
        reccnm()
    else:
        print("+---------------------------+")
        print("|  Name taken Successfully  |")
        print("+---------------------------+")
        time.sleep(1)


def reccno():
    global rno
    rno = input("Enter Reciever Mobile Number:")
    if len(rno) != 10:
        print("+-------------------------------------------------+")
        print("|  Mobile  number should stricty be of 10 digits  |")
        print("|  Enter Again                                    |")
        print("+-------------------------------------------------+")
        time.sleep(1)
        reccno()
    else:
        if rno.isdigit():
            print("+------------------------------------+")
            print("|  Mobile Number taken Successfully  |")
            print("+------------------------------------+")
            time.sleep(1)
        else:
            print("+---------------------------------------------+")
            print("|  Mobile number should stricty have numbers  |")
            print("|  Enter Again                                |")
            print("+---------------------------------------------+")
            time.sleep(1)
            reccno()


def recity():
    global rcy
    rcy = input("Enter Reciever City:")
    if len(rcy) > 25:
        print("+--------------------------------------------------+")
        print("|  City Name should not be more than 25 charcters  |")
        print("|  Enter Again                                     |")
        print("+--------------------------------------------------+")
        time.sleep(1)
        recity()
    else:
        print("+---------------------------+")
        print("|  City taken Successfully  |")
        print("+---------------------------+")
        time.sleep(1)


def recst():
    global st
    st = input("Enter Reciever Street/Area:")
    if len(st) > 25:
        print("+----------------------------------------------------------+")
        print("|  Street/Area name should not be more than 25 characters  |")
        print("|  Enter Again                                             |")
        print("+----------------------------------------------------------+")
        time.sleep(1)
        recst()
    else:
        print("+-------------------------------------+")
        print("|  Street Details taken successfully  |")
        print("+-------------------------------------+")
        time.sleep(1)


def revo():
    global rvno
    rvno = input("Enter House no. with society/hotel name:")
    if len(rvno) > 25:
        print("+---------------------------------------------------------+")
        print("|  House no. & scoety name should be at max 25 charaters  |")
        print("|  Enter Again                                            |")
        print("+---------------------------------------------------------+")
        time.sleep(1)
        revo()
    else:
        print("+--------------------------------------------------+")
        print("|  House no. with Society Name taken successfully  |")
        print("+--------------------------------------------------+")
        time.sleep(1)
