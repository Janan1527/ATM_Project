import datetime
import time
import psycopg2
import sys
import random


conn = psycopg2.connect(database="pdf_db", 
                        user="postgres", 
                        password="1234", host="localhost")

c = conn.cursor()

def createAccount():
    counter = 1
    while counter == 1:
        cardNumber = (random.randrange(10000,99999))
        c.execute("select Number from Account where Number = %s",(cardNumber,))
        check = c.fetchall()
        if check == []:
            counter = 0
            c.execute('INSERT INTO Account VALUES (%s,0,0)',(cardNumber,))
            pin(cardNumber)
        else:
            counter = 1


def checkBalance(cardNumber):
    c.execute("SELECT Balance FROM Account WHERE Number = %s", (cardNumber,))
    new_balance = c.fetchall()
    new_balance1 = new_balance[0]
    new_balance2 = new_balance1[0] 
    time.sleep(1)
    print('\nBalance : ' + str(new_balance2))

def deposit(cardNumber):
    time.sleep(1)
    deposit_value = float(input("\nEnter the amount you want to deposit :"))
    c.execute("SELECT Balance FROM Account WHERE Number =%s", (cardNumber,))
    new_balance = list(c.fetchall())
    new_balance = ''.join(str(e) for e in new_balance)
    new_balance = float(new_balance[1:-2])
    new_balance += deposit_value
    c.execute('UPDATE Account SET Balance = %s WHERE Number =%s', (new_balance, cardNumber))
    conn.commit()
    time.sleep(2)
    print("\nNew balance : " + str(new_balance))
    now = datetime.datetime.now()
    a = input("\nIf you want to print the bill (Yes/No) : ")
    if a == 'yes' :
        c.execute("SELECT Number,Balance FROM Account where Number =%s", (cardNumber,))
        bill = c.fetchall()
        bill = bill[0]
        Number,Balance = bill
        f = open("C:\\Users\\KB JAGADEESH\\Desktop\\atm\\"+str(Number)+'dep.txt',"w")
        f.write(f"\n\t\tDate : {now} \n\t\t Account Number : {Number}\n\n\t\tYour debited value is {deposit_value} \n\n\t\tCurrent Balance : {Balance}")
        f.close()
    else:
        time.sleep(2)
        print("\nThank you")    

def withdraw(cardNumber):
    time.sleep(2)
    deposit_value = float(input("\nEnter the amount you want to withdraw : "))
    c.execute("SELECT Balance FROM Account WHERE Number = %s", (cardNumber,))
    new_balance = list(c.fetchall())
    new_balance = ''.join(str(e) for e in new_balance)
    new_balance = float(new_balance[1:-2])
    if new_balance > deposit_value:
        new_balance -= deposit_value
        c.execute('UPDATE Account SET Balance = %s WHERE Number =%s', (new_balance, cardNumber))
        conn.commit()
        time.sleep(1)
        print("\nNew balance : " + str(new_balance))
        now = datetime.datetime.now()
        a = input("\nIf you want to print the bill (Yes/No) : ")
        if a == 'yes':
            c.execute("SELECT Number,Balance FROM Account where Number =%s", (cardNumber,))
            bill = c.fetchall()
            bill = bill[0]
            Number,Balance = bill
            f = open("C:\\Users\\KB JAGADEESH\\Desktop\\atm\\"+str(Number)+'wit.txt',"w")
            f.write(f"\n\t\tDate : {now}\n\t\t Account Number : {Number}\n\n\t\tYour debited value is {deposit_value} \n\n\t\tCurrent Balance : {Balance}")
            f.close()
        else:
            time.sleep(2)
            print("\nThank you")
    else:
        time.sleep(2)
        print("\nError: Not enough balance in your account")

def pin(cardNumber):
    pin_counter = 0
    while pin_counter == 0:
        new_pin = int(input("\nEnter four digit PIN code "))
        time.sleep(1)
        check_pin = int(input("\nEnter PIN code once more "))
        if new_pin == check_pin and len(str(new_pin)) == 4:
            c.execute("SELECT PIN FROM Account WHERE Number = %s", (cardNumber,))
            new_pin = str(new_pin)
            c.execute("SELECT PIN FROM Account WHERE Number = %s", (cardNumber,))
            c.execute('UPDATE Account SET PIN =%s WHERE Number = %s', (new_pin, cardNumber))
            conn.commit()
            print("Wait PIN updating.....")
            time.sleep(3)
            print("PIN updated")
            pin_counter = 1
            time.sleep(2)
            print("\nCreated account")
            print("\nYour account number is: " + str(cardNumber))
        else:
          time.sleep(1)
          print("\nPlease try again")        

def checkCard(cardNumber):
    c.execute("SELECT Number, PIN FROM account WHERE Number = %s", (cardNumber,))
    row = c.fetchall()
    if row != []:
        raw = row[0]
        raw1 = str(raw[1])
        k = 1
        while k < 3:
            time.sleep(1)
            pin = str(input("\nPlease enter your four digit pin: "))
            if pin == raw1:
                print ('\nCORRECT!')
                return 1
            else:
                print("\nWrong Pin\nEnter again")
                k += 1
        time.sleep(2)        
        print("\nAccess Denied!")
        sys.exit()
    else:
        print("This card does not exist, please try again.")
        return 0

print("**********************************************\n*********** Welcome to ATM ***********\n**********************************************")
cardExists = 0
while cardExists == 0:
    cardNumber = input("\nPlease enter your credit card number or '2' to create a new account or '1' to exit: ")
    if int(cardNumber) == 1:
        sys.exit()
    elif int(cardNumber) == 2:
        createAccount()
    else:
        cardExists = checkCard(cardNumber)

selection = 0  
while int(selection) < 5:
    selection = input("\nEnter the number like to do : \n 1. Check balance\n 2. Deposit Money\n 3. Withdraw Money\n 4. Create PIN number\n 5. Exit\n")
    if int(selection) == 1:  
        checkBalance(cardNumber)
    elif int(selection) == 2:  
        deposit(cardNumber)
    elif int(selection) == 3:  
        withdraw(cardNumber)
    elif int(selection) == 4: 
        pin(cardNumber)
    elif int(selection) == 5: 
        time.sleep(3)
        print("\nThank you, and have a nice day!")

c.close()
conn.close()
sys.exit()



