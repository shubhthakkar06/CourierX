import mysql.connector
from tabulate import tabulate
import  random
import time
from  matplotlib import pyplot as mpt
from PIL import Image
import csv
from datetime import date
import sys
con=mysql.connector.connect(host="localhost",user="root",password="20052006")
cursor=con.cursor()
cursor.execute("use Project")

def usr():
    global uer
    print("+-----------------------------|")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------|")
    uer=input("Enter Username:")
    if uer =='1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        home()
    if len(uer)<8 or len(uer)>31:
        print("+----------------------------------------------+")
        print("|  Username should be between 8-30 characters  |")
        print("|            Please Enter Again                |")
        print("+----------------------------------------------+")
        time.sleep(1)
        usr()
    else:
        if uer.isalpha():
            uer=uer.lower()
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
        elif  " " in uer:
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
            
def cpwd():
    global cps
    cps=input("Confirm Password")
    if cps==ps:
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

def pwd():
    global ps
    print("+-----------------------------|")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------|")
    ps=input("Enter Password")
    if ps=='1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        home()
    if len(ps)<8 or len(ps)>21:
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
        elif  " " in ps:
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

def  usrid():
    global uid
    print("+-----------------------------|")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------|")
    uid=input("Enter your Email-id")
    if uid=='1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        home()
    uid=uid.lower()
    if len(uid)<8 or len(uid)>31:
        print("+----------------------------------------------+")
        print("|  UserID should be between 8-30 characters  |")
        print("|            Please Enter Again                |")
        print("+----------------------------------------------+")
        time.sleep(1)
        usrid()
    elif  " " in uid:
        print('+-----------------------------------+')
        print("|  UserID Should not have Spaces  |")
        print("+-----------------------------------+")
        time.sleep(1)
        usrid()
    else:
        if  '@' not in uid:
            print("+-----------------------------------------+")
            print("|  UserID to be Of Fomrat User@gmail.com  |")
            print("+-----------------------------------------+")
            time.sleep(1)
            usrid()
        else:
            if uid[len(uid)-4:len(uid):1] != '.com':
                print("+-----------------------------------------+")
                print("|  UserID to be of Format User@gmail.com  |")
                print("+-----------------------------------------+")
                time.sleep(1)
                usrid()
            else:
                cursor.execute("select userid from user")
                data=cursor.fetchall()
                for i in data:
                    if i==(uid,):
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

def recd():
    global rcd
    print('+-----------------------------------+')
    print("|     Enter 1 to go to HomePage     |")
    print("+-----------------------------------+")
    rcd=input("Enter 6 digit Recovery Code:")
    if rcd=='1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        home()
    if len(rcd)==6:
        if rcd.isalpha():
            print("+--------------------------+")
            print("|  Code should be numeric  |")
            print("|  Enter Again             |")
            print("+--------------------------+")
            time.sleep(1)
            recd()
        elif  " " in rcd:
            print('+---------------------------------------+')
            print("|  RecoveryCode Should not have Spaces  |")
            print("+---------------------------------------+")
            time.sleep(1)
            recd()
        elif rcd.isdigit():
            cursor.execute("select recoverycode from user")
            data=cursor.fetchall()
            for i in data:
                if i==(int(rcd),):
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

def ye():
    global y
    print("+-----------------------------|")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------|")
    y=input("Enter Year of Birth in YYYY Fromat")
    if y=='1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        home()
    if len(y) !=4:
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
    m=input("Enter Month of Birth in MM format")
    if m=='1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        home()
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
            if int(m) not in [1,2,3,4,5,6,7,8,9,10,11,12]:
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
    d=input("Enter Date of brith in DD Format")
    if d=='1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        home()
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
            if int(m) in [1,3,5,7,8,10,12]:
                if int(d) <1 or int(d)>31:
                    print("+-------------------------------+")
                    print("|  Date should be between 1-31  |")
                    print("+-------------------------------+")
                    time.sleep(1)
                    de()
            elif int(m) in [4,6,9,11]:
                if int(d) <1 or int(d)>30:
                    print("+--------------------------------+")
                    print("|  Date should be between 1-30  |")
                    print("+--------------------------------+")
                    time.sleep(1)
                    de()
            elif int(m) ==2:
                if int(y)%4==0:
                    if int(d) <1 or int(d)>29:
                        print("+----------------------------+")
                        print("|  Date Should Be From 1-29  |")
                        print("+----------------------------+")
                        time.sleep(1)
                        de()
                else:
                    if int(d) <1 or int(d)>28:
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
    db=y+'-'+m+'-'+d

def rpwd():
    print("+-----------------------------+")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------+")
    rd=input("To Reset your password please enter your recoverycode:")
    if rd=='1':
        print("+------------------------+")
        print("+|  Redirecting to Home  |")
        print("+------------------------+")
        time.sleep(1)
        home()
    query= "select recoverycode from user where userid = %s"
    val=(urid,)
    cursor.execute(query,val)
    data=cursor.fetchall()
    for i in data:
        if i ==(rd,):
            print("+------------------+")
            print("|  Reset Password  |")
            print("+------------------+")
            pwd()
            query="update user set password=%s where recoverycode=%s"
            val=(ps,rd)
            cursor.execute(query,val)
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
            ch6=input("Enter Choice")
            if ch6=='1':
                rpwd()
            else:
                print("+---------------------------+")
                print("|  Redirecting You to Home  |")
                print("+---------------------------+")
                time.sleep(1)
                home()

def rsud():
    print("+-----------------------------+")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------+")
    rd=input("To Reset your UserID please enter your recoverycode:")
    if rd=='1':
        print("+---------------------------+")
        print("|  Redirecting You to Home  |")
        print("+---------------------------+")
        time.sleep(1)
        home()
    query= "select recoverycode from user where userid = %s"
    val=(urid,)
    cursor.execute(query,val)
    data=cursor.fetchall()
    for i in data:
        if i ==(int(rd),):
            print("+----------------+")
            print("|  Reset Userid  |")
            print("+----------------+")
            usrid()
            query="update user set userid=%s where recoverycode=%s"
            val=(uid,rd)
            cursor.execute(query,val)
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
            ch6=input("Enter Choice")
            if ch6=='1':
                rsud()
            else:
                print("+---------------------------+")
                print("|  Redirecting You to Home  |")
                print("+---------------------------+")
                time.sleep(1)
                home()

def ud():
    global c
    c=0
    global urid
    print("+-----------------------------+")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------+")
    urid=input("Enter Userid")
    if urid=='1':
        print("+---------------------------+")
        print("|  Redirecting You to Home  |")
        print("+---------------------------+")
        time.sleep(1)
        home()
    urid=urid.lower()

def pds():
    global pdd
    print("+-----------------------------+")
    print("|  Enter 1. to goto Homepage  |")
    print("+-----------------------------+")
    pdd=input("Enter Password:")
    if pdd=='1':
        print("+---------------------------+")
        print("|  Redirecting You to Home  |")
        print("+---------------------------+")
        time.sleep(1)
        home()

def rpd1():
    val=(1+int(data2[0][0]),int(data2[0][0]))
    query="update wpd set attemps=%s where attemps=%s"
    cursor.execute(query,val)
    con.commit()

def rpd2():
   cursor.execute("select * from wpd")
   global data2
   data2=cursor.fetchall()
   for i in data2:
       if i[0]<3:
           print("+-----------------------------------------+")
           print("|  Your Have",3-int(i[0]),"Attempts left  |")
           print("+-----------------------------------------+")
           rpd1()
           pds()
           pdw()
       else:
           print("+------------------------------------+")
           print("|  To many attempts Reset passwords  |")
           print("+------------------------------------+")
           val=(1,int(data2[0][0]))
           query="update wpd set attemps=%s where attemps=%s"
           cursor.execute(query,val)
           con.commit()
           rpwd()

def pdw():
    val=(urid,)
    query="select password from user where userid = %s"
    cursor.execute(query,val)
    data = cursor.fetchall()
    for i in data:
        if i==(pdd,):
            print("+---------------------+")
            print('|  SignIn Successful  |')
            print("+---------------------+")
            time.sleep(1)
            cursor.execute("select attemps from wpd")
            data3=cursor.fetchall()
            val=(1,int(data3[0][0]))
            query="update wpd set attemps=%s where attemps=%s"
            cursor.execute(query,val)
            con.commit()
            lastlogin2()
            lastlogin1()
            menu()
        else:
            print("+----------------------+")
            print("|  Incorrect Password  |")
            print("+----------------------+")
            rpd2()
            rpd1()
                                   
def lastlogin2():
    with open('laslogin.csv',mode='r') as f:
        reader=csv.reader(f,delimiter=',')
        for i in reader:
            if i[2]==urid:
                print("+-----------------------------------------+")
                print("|  Your Last Login",i[0],i[1],                "|")
                print("+-----------------------------------------+")

def lastlogin1():
    tm=time.ctime()
    tim=tm[11:19:1]
    dat=tm[4:10]+"  "+tm[20:24]
    with open('laslogin.csv',mode='w') as f:
        writer=csv.writer(f, delimiter=',')
        writer.writerow([dat,tim,urid])

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
        ch7=input("Enter Choice")
        if ch7=='1':
            signin()
        elif ch7=='2':
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
            home()

def pcd():
    print("+------------------------------+")
    print("|  Enter Your Address Details  |")
    print("+------------------------------+")
    global pc
    pc=input("Enter Your Pincode:")
    if len(pc) !=6:
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
    nm=input("Enter reciever Name:")
    if len(nm)>30:
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
    rno=input("Enter Reciever Mobile Number:")
    if len(rno)!= 10 :
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
    rcy=input("Enter Reciever City:")
    if  len(rcy)>25:
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
    st=input("Enter Reciever Street/Area:")
    if len(st)>25:
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
    rvno=input("Enter House no. with society/hotel name:")
    if len(rvno)>25:
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

def add():
    pcd()
    reccnm()
    reccno()
    recity()
    recst()
    revo()
    val=(urid,pc,nm,rcy,st,rvno,rno)
    print(val)
    global fadd
    fadd= str(pc)+' '+str(nm)+' '+str(rcy)+' '+str(st)+' '+str(rvno)+' '+str(rno)
    query='insert into addresses(userid,pincode,reciever_name,reciever_city,reciever_street,reciever_house,reciever_no) values(%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(query,val)
    con.commit()
    print("+------------------------------+")
    print("|  Address Added Successfully  |")
    print("+------------------------------+")
    time.sleep(1)
    adds()

def add2():
    ch25=input("Enter the no. of the adress you want to select from the adresses shown:")
    if ch25=='0':
        print("+------------------------------+")
        print("|  0 is not valid Enter again  |")
        print("+------------------------------+")
        time.sleep(1)
        add2()
    else:
        cursor.execute("select * from addresses")
        data=cursor.fetchall()
        add1=data[int(ch25)-1]
        global adf
        adf=""
        for i in range(1,7):
            adf=adf+str(data[int(ch25)-1][i])+"  "
        print(adf)

def addn():
        pcd()
        reccnm()
        reccno()
        recity()
        recst()
        revo()
        val=(urid,pc,nm,rcy,st,rvno,rno)
        global fadd
        fadd= +' '+str(pc)+' '+str(nm)+' '+str(rcy)+' '+str(st)+' '+str(rvno)+' '+str(rno)
        query='insert into addresses(userid,pincode,reciever_name,reciever_city,reciever_street,reciever_house,reciever_no) values(%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(query,val)
        con.commit()
        print("+----------------------------------------------------+")
        print("|  Now you will be redirected to choose the address  |")
        print("+----------------------------------------------------+")
        time.sleep(1)
        newadd()

def orderidgen():
    global orderid
    orderid=random.randint(10000000,99999999)
    cursor.execute("select orderid from orders")
    data=cursor.fetchall()
    for i in data:
        if i==(orderid,):
            orderidgen()

def deliverydate():
    l=time.ctime().split()
    dic={'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jul','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
    for i in dic:
        if dic[i]==l[1]:
            m=i
    global ddate
    if len(l[2])==1:
        l3='0'+l[2]
        ddate=l3+'/'+m+'/'+l[4]
    else:
        ddate=l[2]+'/'+m+'/'+l[4]

def fedbk():
    print("+----------------------------------------+")
    print("|  please share your experience with us  |")
    print("+----------------------------------------+")
    print("|  1. Excellent                          |")
    print("|  2. Moderate                           |")
    print("|  3. Bad                                |")
    print("+----------------------------------------+")
    global ch34
    ch34=input("Enter Choice 1/2/3")

def neworder():
    print("+-------------------+")
    print("|  Press 0 to exit  |")
    print("+-------------------+")
    w=input("Enter Order Weight:")
    if w=='0':
        print("+---------------------------+")
        print("|  Redirecting You to Menu  |")
        print("+---------------------------+")
        time.sleep(2)
        menu()
    if float(w)<3 or float(w)>30:
        print("+----------------------------------------------------------+")
        print("|  Minimum Weight to be placed is 3kg and maximum is 30kg  |")
        print("+----------------------------------------------------------+")
        print("|                      Enter Again                         |")
        print("+----------------------------------------------------------+")
        time.sleep(1)
        neworder()

    else:
        pr=0
        cursor.execute("select * from wtscale")
        data=cursor.fetchall()
        for i in data:
            if int(i[0])<float(w):
                if int(i[1])>float(w):
                    pr=i[2]
        dic3={3:'500',5:'1000',7:'1500',9:'2000',11:'2500',13:'3000',15:'3500',17:'4000',19:'4500',21:'5000',23:'5500',25:'6000',27:'6500',29:'7000',30:'7000'}
        for i in dic3:
            if float(w)==i:
                pr=dic3[i]
        print("+-------------------------------------------------+")
        print("|                price",pr,"                      |")
        print("+-------------------------------------------------+")
        print("select an address from your saved adresses")
        query="select * from addresses where userid=%s"
        val=(urid,)
        cursor.execute(query,val)
        data=cursor.fetchall()
        if data==[]:
            print("+-------------------------------------+")
            print("|  You dont have any addresses added  |")
            print("+-------------------------------------+")
            print("|           Add new adress            |")
            print("+-------------------------------------+")
            add()
            print("+-------------------------------------------------------------------------------+")
            print("|  This Address will be used to deliver your courier                            |")
            print("|  Only Cash Payment Method is Accepted                                         |")
            print("|  Please Pay Rs",pr," at our nearest branch when you come to drop the courier  |")
            print("|  Do You Want to Place this Order                                              |")
            print("+-------------------------------------------------------------------------------+")
            ch19=input("Enter y/n")
            if ch19=='y' or ch19=='Y':
                orderidgen()
                deliverydate()
                print("+----------------------------------------------------------------------------------+")
                print("|  Order Placed                                                                    |")
                print("|  Order will be delivered within 5 days                                           |")
                print("|  To Cancel/Modify/Track Please goto Cancel/Modify/Track option on the mainpage   |")
                print("+----------------------------------------------------------------------------------+")
                val=(orderid,fadd,w,pr,ddate,urid)
                query="insert into orders(orderID,address,weight,price,order_date,userid) values(%s,%s,%s,%s,%s,%s)"
                cursor.execute(query,val)
                con.commit()
                time.sleep(2)
                fedbk()
                if ch34=='1':
                    val=('excellent',orderid)
                    query="insert into feedback(review,orderid) values(%s,%s)"
                    cursor.execute(query,val)
                    con.commit()
                    print("+---------------------------+")
                    print("|  Thanks for the feedback  |")
                    print("+---------------------------+")
                    time.sleep(2)
                    menu()
                elif ch34=='2':
                    val=('moderate',orderid)
                    query="insert into feedback(review,orderid) values(%s,%s)"
                    cursor.execute(query,val)
                    con.commit()
                    print("+---------------------------+")
                    print("|  Thanks for the feedback  |")
                    print("+---------------------------+")
                    time.sleep(2)
                    menu()
                elif ch34=='3':
                    val=('bad',orderid)
                    query="insert into feedback(review,orderid) values(%s,%s)"
                    cursor.execute(query,val)
                    con.commit()
                    print("+---------------------------+")
                    print("|  Thanks for the feedback  |")
                    print("+---------------------------+")
                    time.sleep(2)
                    menu()
                else:
                    print("+-----------------+")
                    print("|  invalid input  |")
                    print("+-----------------+")
                    time.sleep(1)
                    fedbk()
        else:
            headers=('UserID','PinCode','Reciever_Name','Reciever_City','Reciever_Street','Reciever_House','Reciever_Mobile')
            print(tabulate(data,headers,tablefmt='fancy_grid'))
            print("+----------------------------+")
            print("|  Want to Add a new adress  |")
            print("+----------------------------+")
            print("+--------------------------------------------+")
            print("|  Enter y for yes and anything else for no  |")
            print("+--------------------------------------------+")
            ch24=input("Enter Choice")
            if ch24=='y'or ch24=='Y':
                add()
            else:
                add2()
                print("+-------------------------------------------------------------------------------+")
                print("|  This Address will be used to deliver your courier                            |")
                print("|  Only Cash Payment Method is Accepted                                         |")
                print("|  Please Pay Rs",pr," at our nearest branch when you come to drop the courier  |")
                print("|  Do You Want to Place this Order                                              |")
                print("+-------------------------------------------------------------------------------+")
                print("+--------------------------------------------+")
                print("|  Enter y for yes and anything else for no  |")
                print("+--------------------------------------------+")
                ch19=input("Enter Choice")
                if ch19=='y' or ch19=='Y':
                    orderidgen()
                    deliverydate()
                    print("+----------------------------------------------------------------------------------+")
                    print("|  Order Placed                                                                    |")
                    print("|  Order will be delivered within 5 days                                           |")
                    print("|  To Cancel/Modify/Track Please goto Cancel/Modify/Track option on the mainpage   |")
                    print("+----------------------------------------------------------------------------------+")
                    val=(orderid,adf,w,pr,ddate,urid)
                    query="insert into orders(orderID,address,weight,price,order_date,userid) values(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(query,val)
                    con.commit()
                    time.sleep(1)
                    fedbk()
                    if ch34=='1':
                        val=('excellent',orderid)
                        query="insert into feedback(review,orderid) values(%s,%s)"
                        cursor.execute(query,val)
                        con.commit()
                        print("+---------------------------+")
                        print("|  Thanks for the feedback  |")
                        print("+---------------------------+")
                        time.sleep(2)
                        menu()
                    elif ch34=='2':
                        val=('moderate',orderid)
                        query="insert into feedback(review,orderid) values(%s,%s)"
                        cursor.execute(query,val)
                        con.commit()
                        print("+---------------------------+")
                        print("|  Thanks for the feedback  |")
                        print("+---------------------------+")
                        time.sleep(2)
                        menu()
                    elif ch34=='3':
                        val=('bad',orderid)
                        query="insert into feedback(review,orderid) values(%s,%s)"
                        cursor.execute(query,val)
                        con.commit()
                        print("+---------------------------+")
                        print("|  Thanks for the feedback  |")
                        print("+---------------------------+")
                        time.sleep(2)
                        menu()
                    else:
                        print("+-----------------+")
                        print("|  invalid input  |")
                        print("+-----------------+")
                        time.sleep(2)
                        fedbk()
                else:
                    print("+--------------------------+")
                    print("|  Redirecting You to Menu |")
                    print("+--------------------------+")
                    time.sleep(1)
                    menu()
     
def get_difference(startdate, enddate):
    diff = enddate - startdate
    global x
    x= diff.days

def newadd():
    val=(urid,)
    query="select * from addresses where userid=%s"
    cursor.execute(query,val)
    data = cursor.fetchall()
    headers=('UserID','PinCode','Reciever_Name','Reciever_City','Reiever_Street','Reciever_house','Reciever_Mobile')
    print(tabulate(data,headers,tablefmt='fancy_grid'))
    print("+------------------------+")
    print("|  Enter 0 to goto menu  |")
    print("+------------------------+")
    chi=input("Enter the address you want to update:")
    if int(chi)>len(data):
        print("+---------------+")
        print("|  wrong input  |")
        print("+---------------+")
        time.sleep(1)
        newadd()
    elif chi=='0':
            print("+-----------------------+")
            print('|  Redirecting to menu  |')
            print("+-----------------------+")
            time.sleep(1)
            menu()
    else:
        print("+----------------------------------------------------------------------------+")
        print("|  You want to update this address or add new one, y for update ,n for new:  |")
        print("+----------------------------------------------------------------------------+")
        ch29=input("")
        if ch29=='y' or ch29=='Y':
            nadf=''
            for i in data[int(chi)-1]:
                nadf=nadf +str(i)+'  '
            val=(nadf,ordersid)
            query="update orders set address=%s where orderid=%s"
            cursor.execute(query,val)
            con.commit()
            print("+------------------------------+")
            print("|  Order Updated Successfully  |")
            print("+------------------------------+")
            menu()
        elif ch29=='n' or ch29=='N':
            addn()
        else:
            print("+-----------------+")
            print("|  Invalid Input  |")
            print("+-----------------+")
            time.sleep(1)
            newadd()

def modiadd():
    print("+-------------------------------------+")
    print('|  1. Update pincode                  |')
    print('|  2. update reciever name            |')
    print("|  3. reciever city                   |")
    print("|  4. reciever house                  |")
    print("|  5. reciever mobile no.             |")
    print("|  6.reciever street                  |")
    print("|  Enter anything else to go to menu  |")
    print("+-------------------------------------+")
    ch30=input("Enter Choice 1/2/3/4/5:")
    if ch30=='1':
        pcd()
        val=(pc,urid)
        query='update addresses set pincode = %s where userid=%s'
        cursor.execute(query,val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd()
    elif ch30=='2':
        reccnm()
        val=(nm,urid)
        query='update addresses set reciever_name = %s where userid=%s'
        cursor.execute(query,val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd()
    elif ch30=='3':
        recity()
        val=(rcy,urid)
        query='update addresses set reciever_city = %s where userid=%s'
        cursor.execute(query,val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd()
    elif ch30=='4':
        revo()
        val=(rvno,urid)
        query='update addresses set reciever_house = %s where userid=%s'
        cursor.execute(query,val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd()
    elif ch30=='5':
        reccno()
        val=(rno,urid)
        query='update addresses set reciever_no = %s where userid=%s'
        cursor.execute(query,val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd()
    elif ch30=='6':
        recst()
        val=(st,urid)
        query='update addresses set pincode = %s where userid=%s'
        cursor.execute(query,val)
        con.commit()
        print("+-----------------------------------------------------------------------------------------------------------+")
        print("|  Now you will be redirected to a page where you can either add a new address or select this modified one  |")
        print("+-----------------------------------------------------------------------------------------------------------+")
        time.sleep(1)
        newadd()
    else:
        print("+-----------------------+")
        print("|  Redirecting to Menu  |")
        print("+-----------------------+")
        time.sleep(2)
        menu()

def modimenu():
    print("+-----------------------------------------+")
    print("|  You can only modify address            |")
    print("+-----------------------------------------+")
    print("|      1. Modify address                  |")
    print("+-----------------------------------------+")
    print("|  Enter 0 to go to menu or else enter 1  |")
    print("+-----------------------------------------+")
    ch27=input("Enter Choice")
    if ch27=='0':
        print("+-----------------------+")
        print("|  Redirecting to Menu  |")
        print("+-----------------------+")
        time.sleep(2)
        menu()
    elif ch27=='1':
        print("+--------------------------------------------------------------+")
        print("|  1. Change entire address by adding new address              |")
        print("|  2.Modify existing address                                   |")
        print("+--------------------------------------------------------------+")
        print("|  Enter Anything else to go to menu                           |")
        print("+--------------------------------------------------------------+")
        ch28=input("Enter choice:")
        if ch28=='1':
            newadd()
        elif ch28=='2':
            modiadd()
    else:
        print("+-----------------+")
        print("|  Invalid input  |")
        print("+-----------------+")
        time.sleep(2)
        modimenu()

def vieworder():
    val=(urid,)
    query='select * from orders where userid=%s'
    cursor.execute(query,val)
    data=cursor.fetchall()
    headers=('OrderID','Address','Weight','Price','Order_Date','UserID')
    print(tabulate(data,headers,tablefmt='fancy_grid'))
    ch31=input("Press 1 to goto menu")
    if ch31=='1':
        print("+-----------------------+")
        print("|  Redirecting to Menu  |")
        print("+-----------------------+")
        time.sleep(2)
        menu()
    else:
        print("+-----------------+")
        print('|  invalid input  |')
        print("+-----------------+")
        time.sleep(2)
        vieworder()

def deliverynogen():
    global delid
    delid=random.randint(1000000000,9999999999)
    cursor.execute("select delivery_no from delivery")
    data=cursor.fetchall()
    if (delid,) in data:
        deliverynogen()
    else:
        deliv=0
        cursor.execute("select orderid from delivery")
        data=cursor.fetchall()
        if (str(ordersid),) in data:
            val=(ordersid,)
            query="select delivery_no from delivery where orderid=%s"
            cursor.execute(query,val)
            data=cursor.fetchall()
            for i in data:
                deliv=i[0]
                print("+----------------------------+")
                print("|  Mobile No.",deliv,"  |")
                print("+----------------------------+")
                break
        else:
            val=(ordersid,delid)
            query='insert into delivery(orderid,delivery_no) values(%s,%s)'
            cursor.execute(query,val)
            con.commit()
            print("+----------------------------+")
            print("|  Mobile No.",delid,"  |")
            print("+----------------------------+")
                                   
def trackorder():
    val=(urid,)
    query="select * from orders where userid=%s"
    cursor.execute(query,val)
    data = cursor.fetchall()
    headers=('OrderID','Address','Weight','Price','Order_Date','UserID')
    print(tabulate(data,headers,tablefmt='fancy_grid'))
    if data==[]:
        print("+------------------------------------+")
        print("|  You Havent Placed Any Orders Yet  |")
        print("+------------------------------------+")
        time.sleep(1)
        menu()
    print("+----------------------------------------------------------------+")
    print("|  Enter the no. of order you want to track, enter 0 to go back  |")
    print("+----------------------------------------------------------------+")
    ch27=input("Choice:")
    if ch27=='0':
        print("+-----------------------+")
        print("|  Redirecting to Menu  |")
        print("+-----------------------+")
        time.sleep(1)
        menu()
    elif int(ch27)>len(data):
            print("+--------------------------------------+")
            print("|  Only",len(data),"Orders exist       |")
            print("|  Enter again                         |")
            print("+--------------------------------------+")
            time.sleep(1)
            trackorder()
    else:
        global ordersid
        ordersid=data[int(ch27)-1][0]
        d2date=data[int(ch27)-1][4]
        startdate=date(int(d2date[6:10]),int(d2date[3:5]),int(d2date[0:2]))
        endindate()
        get_difference(startdate, enddate)
        if x==0:
            print("+--------------------------+")
            print('|  Order Under Proceesing  |')
            print("+--------------------------+")
            time.sleep(4)
            menu()
        elif x==1:
            print("+-----------------------------+")
            print('|  Order Is Under  Packaging  |')
            print("+-----------------------------+")
            time.sleeep(4)
            menu()
        elif x==2:
            print("+--------------------------+")
            print('|  Order Is Ready To Ship  |')
            print("+--------------------------+")
            time.sleep(4)
            menu()
        elif x==3:
            print("+---------------------+")
            print('|  Order Is Shipped   |')
            print("+---------------------+")
            time.sleep(4)
            menu()
        elif x==4:
            print("+----------------------------------------------")
            print('|  Order Is Out For Delivery                  |')
            print('|  Order Is Delivered By Our Delivery Agent   |')
            print("+---------------------------------------------+")
            deliverynogen()
        elif x>=5:
            deliverynogen()
            print("+--------------------------------------------------------------------------+")
            print("|  order is delivered to your selected address                             |")
            print("|  Thankyou for choosing us                                                |")
            print("|  Hope to see you again                                                   |")
            print("+--------------------------------------------------------------------------+")
            time.sleep(4)
            menu()
          
def endindate(): 
    l=time.ctime().split()
    dic={'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jul','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
    for i in dic:
        if dic[i]==l[1]:
            m=i
    global enddate
    enddate=date(int(l[4]),int(m),int(l[2]))

def modiorder():
    print("+-------------------------------------------------------------------+")
    print("|  Orders can be Modified only till 2 days after placing the order  |")
    print("+-------------------------------------------------------------------+")
    val=(urid,)
    query="select * from orders where userid=%s"
    cursor.execute(query,val)
    data = cursor.fetchall()
    headers=('OrderID','Address','Weight','Price','Order_Date','UserID')
    print(tabulate(data,headers,tablefmt='fancy_grid'))
    if data==[]:
        print("+------------------------------------+")
        print("|  You Havent Placed Any Orders Yet  |")
        print("+------------------------------------+")
        time.sleep(2)
        menu()
    print("+----------------------------------------------------------------+")
    print("|  Enter the no. of order you want to track, enter 0 to go back  |")
    print("+----------------------------------------------------------------+")
    ch27=input("Enter Choice")
    if ch27=='0':
        print("+----------------------+")
        print("|  Redirecting to Menu |")
        print("+----------------------+")
        time.sleep(1)
        menu()
    elif int(ch27)>len(data):
            print("+-----------------------------------+")
            print("|  Only",len(data),"Orders exist    |")
            print("|  Enter again                      |")
            print("+-----------------------------------+")
            time.sleep(2)
            modiorder()
    else:
        global ordersid
        ordersid=data[int(ch27)-1][0]
        d2date=data[int(ch27)-1][4]
        startdate=date(int(d2date[6:10]),int(d2date[3:5]),int(d2date[0:2]))
        endindate()
        get_difference(startdate, enddate)
        if x>2:
            print("+--------------------------------------------------------+")
            print("|  This order cant be modified as it is already shipped  |")
            print("|  Redirecting you to other orders                       |")
            print("+--------------------------------------------------------+")
            time.sleep(1)
            modiorder()
        else:
            modimenu()

def rpun():
    print("+--------------------------------+")
    print("|  Enter 1. to goto Profilepage  |")
    print("+--------------------------------+")
    rd=int(input("To Reset your Username please enter your recoverycode"))
    if rd=='1':
        print("+------------------------------+")
        print("|  Redirecting to ProfilePage  |")
        print("+------------------------------+")
        time.sleep(1)
        profile()
    cursor.execute("select recoverycode from user")
    data=cursor.fetchall()
    for i in data:
        if i ==(rd,):
            print("+------------------+")
            print("|  Reset Username  |")
            print("+------------------+")
            usr()
            query="update user set username=%s where recoverycode=%s"
            val=(uer,rd)
            cursor.execute(query,val)
            con.commit()
            print("+--------------------+")
            print("|  Username Changed  |")
            print("+--------------------+")
            profile()

def rpdb():
    print("+--------------------------------+")
    print("|  Enter 1. to goto Profilepage  |")
    print("+--------------------------------+")
    rd=int(input("To Reset your DOB please enter your recoverycode:"))
    if rd=='1':
        print("+------------------------------+")
        print("|  Redirecting to ProfilePage  |")
        print("+------------------------------+")
        time.sleep(2)
        profile()
    cursor.execute("select recoverycode from user")
    data=cursor.fetchall()
    for i in data:
        if i ==(rd,):
            print("+-------------+")
            print("|  Reset DOB  |")
            print("+-------------+")
            dob()
            query="update user set DOB=%s where recoverycode=%s"
            val=(db,rd)
            cursor.execute(query,val)
            con.commit()
            print("+----------------------------------+")
            print("|  Date Of Birth Has Been Changed  |")
            print("+----------------------------------+")
            time.sleep(2)
            profile()

def dele():
    print("+--------------------------------+")
    print("|  Enter 1. to goto Profilepage  |")
    print("+--------------------------------+")
    rd=int(input("To Delete Your Account please enter your recoverycode::"))
    if rd=='1':
        print("+------------------------------+")
        print("|  Redirecting to ProfilePage  |")
        print("+------------------------------+")
        time.sleep(2)
        profile()
    cursor.execute("select recoverycode from user")
    data=cursor.fetchall()
    for i in data:
        if i ==(rd,):
             ch20=input("Are You Sure You Want to Delete Your Account Enter y for yes")
             print("+----------------------------------------------------------------------------------------+")
             print("|  Anything else entered will be taken as no and you will be redicrected to profilepage  |")
             print("+----------------------------------------------------------------------------------------+")
             if ch20=='y' or ch20=='Y':
                 query="delete from user where userid = %s"
                 val=(urid,)
                 cursor.execute(query,val)
                 con.commit()
                 query="delete from addresses where userid = %s"
                 cursor.execute(query,val)
                 con.commit()
                 val=("Deleted Account",urid)
                 query="update orders set userid=%s where userid=%s"
                 cursor.execute(query,val)
                 con.commit()
                 print("+--------------------------------+")
                 print("|  Account Deleted Successfully  |")
                 print("+--------------------------------+")
                 time.sleep(2)
                 home()
             else:
                print("+------------------------------+")
                print("|  Redirecting to ProfilePage  |")
                print("+------------------------------+")
                time.sleep(1)
                profile()

def admenu():
    print("+-----------------------------------+")
    print("|  Welcome Admin                    |")
    print("+-----------------------------------+")
    print("|  1. Check Users Table             |")
    print("|  2. Check Addresses Table         |")
    print("|  3. Check Orders Table            |")
    print("|  Enter anything else to sign out  |")
    print("+-----------------------------------+")
    ch19=input("Enter Choice 1/2/3")
    if ch19=='1':
        cursor.execute("select * from user")
        data=cursor.fetchall()
        headers=('UserID','UserName','Password','DOB','Recovery Code')
        print(tabulate(data,headers,tablefmt='fancy_grid'))
        time.sleep(5)
        admenu()
    elif ch19=='2':
        cursor.execute("select * from Addresses")
        data=cursor.fetchall()
        headers=('UserID','PinCode','Reciever_Name','Reciever_City','Reiever_Street','Reciever_house','Reciever_Mobile')
        print(tabulate(data,headers,tablefmt='fancy_grid'))
        time.sleep(5)
        admenu()
    elif ch19=='3':
        cursor.execute("select * from Orders")
        data=cursor.fetchall()
        headers=('OrderID','Address','Weight','Price','Order_Date','UserID')
        print(tabulate(data,headers,tablefmt='fancy_grid'))
        time.sleep(5)
        admenu()
    else:
        time.sleep(1)
        home()

def admin():
    print("+--------------------------------+")
    print("|  Enter 1. to goto Profilepage  |")
    print("+--------------------------------+")
    usrid=input("Enter Admin ID")
    if usrid.lower()=='admin':
        print("+-----------------------------+")
        print("|  Enter 1. to goto Homepage  |")
        print("+-----------------------------+")
        aps=input("Enter Password")
        if aps.lower()=='admin':
            print("+--------------------------+")
            print("|  Admin Login Successful  |")
            print("+--------------------------+")
            time.sleep(1)
            admenu()
        elif aps=='1':
            print("+-------------------------------+")
            print("|    Redirecting to HomePage    |")
            print("+-------------------------------+")
            time.sleep(1)
            home()
        else:
            print("+------------------------------+")
            print("|  Wrong Password Enter Again  |")
            print("+------------------------------+")
            time.sleep(1)
            admin()
    elif usrid=='1':
        print("+-------------------------------+")
        print("|    Redirecting to HomePage    |")
        print("+-------------------------------+")
        time.sleep(1)
        home()
    else:
        print("+------------------------------+")
        print("|  Wrong Admin ID Enter Again  |")
        print("+------------------------------+")
        time.sleep(1)
        admin()

def adds():
    query="select * from addresses where userid=%s"
    val=(urid,)
    cursor.execute(query,val)
    data= cursor.fetchall()
    headers=('UserID','PinCode','Reciever_Name','Reciever_City','Reciever_Street','Reciever_House','Reciever_Mobile')
    print(tabulate(data,headers,tablefmt='fancy_grid'))
    if data==[]:
        print("+----------------------------------------------------------------+")
        print("|  Looks like you dont have any addresses saved in your account  |")
        print("|  Wanna Add one ?                                               |")
        print("+----------------------------------------------------------------+")
        ch18=input("Enter y/n")
        if ch18=='y' or ch18=='Y':
            add()
        elif ch18=='n' or ch18=='N':
            profile()
        else:
            print("+------------------------------+")
            print("|  Wrong Input                 |")
            print("|  Redirecting to ProfilePage  |")
            print("+------------------------------+")
            time.sleep(1)
            profile()
    else:
        print("+-----------------------------------------+")
        print("|  Do you want to add any new addresses?  |")
        print("+-----------------------------------------+")
        ch18=input("Enter y/n")
        if ch18=='y' or ch18=='Y':
            add()
        elif ch18=='n' or ch18=='N':
            profile()
        else:
            print("+------------------------------+")
            print("|  Wrong Input                 |")
            print("|  Redirecting to ProfilePage  |")
            print("+------------------------------+")
            time.sleep(1)
            profile()
            
def profile():
    query= "select * from user where userid=%s"
    val=(urid,)
    cursor.execute(query,val)
    data=cursor.fetchall()
    for i in data:
        print("+-------------------------------------------------------+")
        print("|  Name:",data[0][1],"                                  |")
        print("|  Email:",data[0][0],"                         |")
        print("|  Date of Birth",data[0][3],"                            |")
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
        ch22=input("Press anything else to goto mainpage")
        if ch22=='1':
            rsud()
        elif ch22=='2':
            rpwd()
        elif ch22=='3':
            rpun()
        elif ch22=='4':
            rpdb()
        elif ch22=='5':
            dele()
        elif ch22=='6':
            vieworder()
        elif ch22=='7':
            adds()
        elif ch22=='8':
            time.sleep(1)
            home()
        else:
            time.sleep(1)
            menu()

def canorder():
    print("+--------------------------------------------------------------------+")
    print("|  Orders can be Cancelled only till 2 days after placing the order  |")
    print("+--------------------------------------------------------------------+")
    val=(urid,)
    query="select * from orders where userid=%s"
    cursor.execute(query,val)
    data = cursor.fetchall()
    headers=('OrderID','Address','Weight','Price','Order_Date','UserID')
    print(tabulate(data,headers,tablefmt='fancy_grid'))
    if data==[]:
        print("+------------------------------------+")
        print("|  You Havent Placed Any Orders Yet  |")
        print("+------------------------------------+")
        time.sleep(2)
        menu()
    print("+-----------------------------------------------------------------+")
    print("|  Enter the no. of order you want to Cancel, enter 0 to go back  |")
    print("+-----------------------------------------------------------------+")
    ch27=input("Enter Choice:")
    if ch27=='0':
        menu()
    elif int(ch27)>len(data):
            print("+-----------------------------------+")
            print("|  Only",len(data),"Orders exist    |")
            print("|  Enter again                      |")
            print("+-----------------------------------+")
            time.sleep(1)
            canorder()
    else:
        global ordersid
        ordersid=data[int(ch27)-1][0]
        d2date=data[int(ch27)-1][4]
        startdate=date(int(d2date[6:10]),int(d2date[3:5]),int(d2date[0:2]))
        endindate()
        get_difference(startdate, enddate)
        if x>2:
            print("+--------------------------------------------------------+")
            print("|  This order cant be Cancelled as it is already shipped  |")
            print("|  Redirecting you to other orders                       |")
            print("+--------------------------------------------------------+")
            time.sleep(2)
            menu()
        else:
            ch33=input("Are you sire you want to cancel your order")
            print("+------------------------------------------------------+")
            print("|  Anything Else will be taken as a no and go to menu  |")
            print("+------------------------------------------------------+")
            if ch33=='y' or ch33=='Y':
                val=(ordersid,)
                query='delete from orders where orderid=%s'
                cursor.execute(query,val)
                con.commit()
                print("+--------------------------------+")
                print("|  Order Cancelled successfully  |")
                print("+--------------------------------+")
                time.sleep(1)
                menu()
            else:
                print("+-----------------------+")
                print("|  Redirecting to Menu  |")
                print("+-----------------------+")
                time.sleep(1)
                menu()

def menu():
    val=(urid,)
    query="select username from user where userid = %s"
    cursor.execute(query,val)
    data=cursor.fetchall()
    print("+-------------------------+")
    print("|  Welcome",data[0][0],"  |")
    print("|  1. Place a New Order   |")
    print("|  2.Modify Your Order    |")
    print("|  3. Cancel Your Order   |")
    print("|  4. Track Your Order    |")
    print("|  5. View Your Orders    |")
    print("|  6. Account Profile     |")
    print("|  7. Sign Out            |")
    print("+-------------------------+")
    ch11=input("Enter Choice 1/2/3/4/5")
    if ch11=='1':
        neworder()
    elif ch11=='2':
        modiorder()
    elif ch11=='3':
         canorder()
    elif ch11=='4':
         trackorder()
    elif ch11=='5':
        vieworder()
    elif ch11=='6':
        profile()
    elif ch11=='7':
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

def signup():
    print("+-----------+")
    print("|  Sign Up  |")
    print("+-----------+")
    usr()
    pwd()
    usrid()
    recd()
    dob()
    query="insert into user(UserID,Username,Password,DOB,RecoveryCode) values(%s,%s,%s,%s,%s)"
    val=(uid,uer,ps,db,rcd)
    cursor.execute(query,val)
    con.commit()
    print("+--------------------------------+")
    print("|  Account Created Successfully  |")
    print("+--------------------------------+")
    time.sleep(1)
    signin()

def abtus():
    print("+-----------------+")
    print("|  1. Who We are  |")
    print("|  2. Feedbacks   |")
    print("|  3. Home        |")
    print("+-----------------+")
    ch35=input("Enter choice")
    if ch35=='1':
        f1=open('AboutUs.txt','r')
        l=f1.read()
        print(l)
        f1.close()
        time.sleep(5)
        abtus()
    elif ch35=='2':
        e=0
        m=0
        b=0
        cursor.execute("select review from feedback")
        data=cursor.fetchall()
        for i in data:
            if i[0]=='excellent':
                e+=1
            elif i[0]=='moderate':
                m+=1
            elif i[0]=='bad':
                b+=1
        con=[e,m,b]
        zones=['Excellent','Modetrate','Bad']
        mpt.axis('equal')
        col=['blue','']
        expl=[0,0,0]
        mpt.pie(con,labels=zones,autopct='%1.1F%%',explode=expl)
        mpt.legend(loc='upper right')
        mpt.show()
        time.sleep(5)
        abtus()
    elif ch35=='3':
        time.sleep(2)
        home()
    else:
        print("+-----------------+")
        print("|  Invalid Input  |")
        print("+-----------------+")
        time.sleep(2)
        abtus()
    
def choice():
        ch=(input("Please Enter choice 1/2/3/4/5 "))
        if ch=='1':
            time.sleep(2)
            signup()
        elif ch=='2':
            time.sleep(2)
            signin()
        elif ch=='3':
            time.sleep(2)
            admin()
        elif ch=='4':
            time.sleep(2)
            abtus()
        elif ch=='5':
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
    print("+----------------------------------+")
    print("|   Welcome to FastTrack Curior    |")
    print("+----------------------------------+")
    print("|             1. Sign up           |")
    print("|             2. Sign in           |")
    print("|             3. Admin Login       |")
    print("|             4. About Us          |")
    print("|             5. Exit              |")
    print("+----------------------------------+")
    img=Image.open('/Users/shubhthakkar/Downloads/project.png')
    img.show()
    choice()
    
home()