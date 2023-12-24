#required module
from getpass import getpass
import mysql.connector
import datetime

#fetching real time date and time 
#connecting python with mysql
mydb=mysql.connector.connect (
    host="localhost",
    user="root", 
    password="Sidcode@123")

#assigning cursor
mycursor=mydb.cursor()

#creating database is not exisits
mycursor.execute("create database if not exists library")

mycursor.execute("use library")

mycursor.execute("create table if not exists student(Roll_Number int(10), Name varchar(30), Date varchar(30), Time varchar(30))")
mycursor.execute("create table if not exists studenthistory(Roll_Number int(10) , Name varchar(30), Date varchar(30), Time varchar(30), Status varchar(10))")
mycursor.execute("create table if not exists login(Roll_Number int(10) , Enrollment varchar(20), Name varchar(30))")

def display():
    print("\n1.ENTER")
    print("2.EXIT")
    print("3.VIEW CURRENT MEMBERS")
    print("4.VIEW HISTORY")
    print("5.CLEAN HISTORY")

def count():
    mycursor.execute("select count(*) from student")
    a=mycursor.fetchall()
    ab=a[-1][-1]
    
    if ab>5:
        print("LIBRARY IS FULL")
    if ab<5:
        left=5-ab
        print("{} SEATS REMAINING".format(left))

def enter():   
    now=datetime.datetime.now()
    date=str(now.strftime("%Y-%m-%d"))
    time=str(now.strftime("%H:%M:%S"))
    roll=str(input("\nEnter your roll number:"))
    mycursor.execute("select count(*) from student where Roll_Number="+roll+"")
    live=mycursor.fetchall()
    live_count=live[-1][-1]
    if live_count==0:
        mycursor.execute("select count(*) from login where Roll_Number="+roll+"")
        exi=mycursor.fetchall()
        exi_count=exi[-1][-1]
        if exi_count == 0:
            name = str(input ("\nEnter your name:"))
            enroll=str(input("\nEnter Your Enrollment Number:"))
            mycursor.execute("insert into student values('"+roll+"','"+name+"','"+date+"','"+time+"')")
            mycursor.execute("insert into login values('"+roll+"','"+enroll+"','"+name+"')")
            mycursor.execute("insert into studenthistory values('"+roll+"','"+name+"','"+date+"','"+time+"','IN')")
            print("WELCOME ",name)
            mydb.commit()
            count()
        else:
            mycursor.execute("select Name from login where Roll_Number="+roll+"")
            name=mycursor.fetchall()
            n=name[-1][-1]
            mycursor.execute("insert into student values('"+roll+"','"+n+"','"+date+"','"+time+"')")
            
            mycursor.execute("insert into studenthistory values('"+roll+"','"+n+"','"+date+"','"+time+"','IN')")
            mydb.commit()
            
            print("WELCOME",n)
            count()
    else:
        print("Already in the library")
def leave():
    now=datetime.datetime.now()
    date=str(now.strftime("%Y-%m-%d"))
    time=str(now.strftime("%H:%M:%S"))

    roll=str(input("\nEnter your roll number:"))

    mycursor.execute("select Name from studenthistory where Roll_Number="+roll+"")
    name=mycursor.fetchall()
    n=name[-1][-1]
    mycursor.execute("insert into studenthistory values('"+roll+"','"+n+"','"+date+"','"+time+"','OUT')")
    mycursor.execute("delete from student where Roll_number="+roll+"")
    print("THANK YOU FOR VISITING")
    mydb.commit()
    count()

def view():
    mycursor.execute("select *from student ")
    rows=mycursor.fetchall()
    mycursor.execute("select count(*) from student")
    a=mycursor.fetchall()
    ab=a[-1][-1]
    print("\nOCCUPANCY:",ab)
    for x in rows:
        print(x)
    
def view_history():
    mycursor.execute("select count(*) from studenthistory")
    a=mycursor.fetchall()
    ab=a[-1][-1]
    if ab==0:
        print("\nNo Records Found!")

    else:
        mycursor.execute("select *from studenthistory ")
        rows=mycursor.fetchall()
        for x in rows:
            print(x)

def clean_history():
    cleanpass="admin"
    cleanpass_input=getpass("Enter the password:")
    if cleanpass_input==cleanpass:
        mycursor.execute("truncate table studenthistory")
        print('History Cleared')
    
    else:
        print('\nWrong Password,Please try again!')
        clean_history()

def decision():
    if ch==1:
        enter()
        
    if ch==2:
        leave()

    elif ch==3:
        view()

    elif ch==4:
        view_history()

    elif ch==5:
        clean_history()
        
while True:
    mycursor.execute("select count(*) from student")
    a=mycursor.fetchall()
    ab=a[-1][-1]

    if ab==0:
        print("\n\n\nCOMPLETLY EMPTY")
        print("1.ENTER")
        print("3.VIEW")
        print("4.VIEW HISTROY")
        print("5.DELETE HISTORY")
        ch=int(input("\nEnter the choice(1/3/4/5):"))
        decision()
        pass

    if ab>=5:
        print("\n\n\nWE ARE FULL")
        print("CANNOT let more members in")
        print("2.EXIT")
        print("3.VIEW")
        print("4.VIEW HISTROY")
        print("5.DELETE HISTORY")
        ch=int(input("\nEnter the choice(2/3/4/5):"))
        decision()
        pass
    
    else:
        display()  
        ch=int(input("\nEnter the choice(1/2/3/4/5):"))
        decision()