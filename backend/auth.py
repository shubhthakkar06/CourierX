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
            # rpd1() is called by pdw() on failure
            pds()
            pdw()
        else:
            print("+------------------------------------+")
            print("|  To many attempts Reset passwords  |")
            print("+------------------------------------+")
            rpwd()


def pdw():
    """Verify the entered password against the database."""
    cursor.execute("select attemps from wpd")
    att = cursor.fetchone()
    if att and att[0] >= 3:
        print("+------------------------------------+")
        print("|  To many attempts Reset passwords  |")
        print("+------------------------------------+")
        rpwd()
        return

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
            query_db("UPDATE wpd SET attemps=1", commit=True)
            lastlogin2(urid)
            lastlogin1(urid)
            _menu()
        else:
            print("+----------------------+")
            print("|  Incorrect Password  |")
            print("+----------------------+")
            rpd1()
            rpd2()


# ─────────────────────────────────────────────────────────────────────────────
# Password / UserID Reset (via recovery code)
# ─────────────────────────────────────────────────────────────────────────────
128: def rpwd():
129:     """Reset password using OTP verification."""
130:     import backend.validation as v
131:     from backend.sms import send_otp, verify_otp
132:     from backend.db import query_db
133: 
134:     print("+-----------------------------+")
135:     print("|  Enter 1. to goto Homepage  |")
136:     print("+-----------------------------+")
137:     uid = input("To Reset your password please enter your Userid (Email): ").lower().strip()
138:     if uid == '1':
139:         _home()
140:         return
141: 
142:     user = query_db('SELECT mobile FROM user WHERE userid=%s', (uid,), fetchone=True)
143:     if not user:
144:         print("+---------------------------------+")
145:         print("|  User ID not found              |")
146:         print("+---------------------------------+")
147:         time.sleep(1)
148:         _home()
149:         return
150: 
151:     mobile = user['mobile']
152:     clean = mobile.replace('+91', '').replace(' ', '')
153:     ok, msg = send_otp(clean)
154:     if not ok:
155:         print(f"Error: {msg}")
156:         _home()
157:         return
158: 
159:     print(f"+---------------------------------+")
160:     print(f"|  OTP sent to {mobile[:6]}****{mobile[-2:]}  |")
161:     print("+---------------------------------+")
162:     code = input("Enter 6-digit OTP: ").strip()
163:     
164:     valid, msg = verify_otp(clean, code)
165:     if valid:
166:         print("+------------------+")
167:         print("|  Reset Password  |")
168:         print("+------------------+")
169:         pwd()
170:         query_db("UPDATE user SET password=%s WHERE userid=%s", (v.ps, uid), commit=True)
171:         query_db("UPDATE wpd SET attemps=1", commit=True)
172:         print("+--------------------+")
173:         print("|  Password Changed  |")
174:         print("+--------------------+")
175:         time.sleep(1)
176:         signin()
177:     else:
178:         print(f"+---------------------------------+")
179:         print(f"|  OTP Error: {msg}              |")
180:         print("|  1. Try Again                   |")
181:         print("|  Anything else: Homepage        |")
182:         print("+---------------------------------+")
183:         if input("Choice: ") == '1':
184:             rpwd()
185:         else:
186:             _home()


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
        print("|  3. Forgot Password                      |")
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
        elif ch7 == '3':
            rpwd()
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
