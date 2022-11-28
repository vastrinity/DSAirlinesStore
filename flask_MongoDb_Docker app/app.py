import code
from distutils.debug import DEBUG
from email import message
from time import time
from tkinter import ON
from flask import Flask, render_template, request, url_for, redirect, session


import random
from pymongo import MongoClient

from datetime import date, datetime

# ...


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.secret_key = "testing"
client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
db = client.DSstore
us = db.users
ads=db.admins
flights=db.flights
reservations=db.reservations

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('welcome.html')

#*************************USER*****************************************
@app.route('/register', methods=('GET', 'POST'))
def register():
    message = ''
    
    if request.method=='POST':
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        passport = request.form['passport']

        #if found in database showcase that it's found 
        username_found = us.find_one({"username": username})
        email_found = us.find_one({"email": email})
        passport_found=us.find_one({"passport": passport})


        if username_found:
            message = 'There already is a user by that username'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if passport_found:
            message = 'This passport already exists in database'
            return render_template('register.html', message=message)



        else:
            
            us.insert_one({'fullname': fullname, 'email': email, 'username': username, 'password': password, 'passport': passport,'status_u':True})
            user_data = us.find_one({"email": email})
            new_email = user_data['email']
            return redirect('user_menu')
        
    
    return render_template('register.html')




@app.route('/signin', methods=["POST", "GET"])
def signin():
    if "email" in session:
        return redirect(url_for("user_menu"))
    if request.method == "POST":
        signuser = request.form.get("usernameS")
        password = request.form.get("passwordS")

       

        username_found = us.find_one({"username": signuser})
        email_found = us.find_one({"email": signuser})
        

        



        if email_found :
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
           
            
            
            if password==passwordcheck:
                session["email"] = email_val
                status_e=email_found['status_u']
                if status_e:
                 return redirect(url_for('user_menu'))
                else:
                    message = 'You have to activate your account'
                    return render_template('signin.html', message=message)

            else:
                
                message = 'Wrong password'
                return render_template('signin.html', message=message)
        elif username_found :
            email_val = username_found['email']
            username_val = username_found['username']
            passwordcheck = username_found['password']
            #encode the password and check if it matches
           
            if password==passwordcheck:
            
                session["email"] = email_val
                session["username"] = username_val
                status_u=username_found['status_u']
                if status_u:
                 return redirect(url_for('user_menu'))
                else:
                    message = 'You have to activate your account'
                return render_template('signin.html', message=message)

            else:
                
                message = 'Wrong password'
                return render_template('signin.html', message=message)
       

        else:
            message = 'User not found'
            return render_template('signin.html', message=message)
    return render_template('signin.html')




@app.route('/user_menu', methods=('GET', 'POST'))
def user_menu():
     
       return render_template('user_menu.html')

@app.route('/activate_account', methods=('GET', 'POST'))
def activate_account():
    
         if request.method == "POST":
            activationCode = request.form.get("activationCode")
            code=str(activationCode)
            passport = request.form.get("passport")
           
            passport_found = us.find_one({'passport':passport})
            if passport_found:   
                if code==passport_found['activate']:
                    us.update_one({'passport':passport},{'$set':{'status_u':True,'activate':None}})
                    message='your acoount has been activated'
                    return render_template('activate_account.html',message=message)
                else:
                    message='wrong credentials'+passport
                    return render_template('activate_account.html',message=message)
            else:
                 message='no passport found'
                 return render_template('activate_account.html',message=message)


         return render_template('activate_account.html')

@app.route('/deleteresarvation', methods=('GET', 'POST'))
def deletereservation():
    if request.method == "POST":
         ticketcoded = request.form.get("ticketcoded")
         ticket_found=reservations.find_one({'ticket_code':ticketcoded})
         if ticket_found:
            flight_num=ticket_found['flightCode']
            flightd_found=flights.find_one({'code':flight_num})
            if flightd_found:
                seats_old=flightd_found['seats']
                seats_up=seats_old+1
                flights.update_one({'code':flight_num},{'$set':{'seats':seats_up}})
                credit_val=ticket_found['credit_card']
                reservations.delete_many( { 'ticket_code':  ticketcoded} )

                message='We have return money to your credit card with number:'+credit_val
                return render_template('deleteReservation.html', message=message)
            else:
                message='no flight found:'
                return render_template('deleteReservation.html', message=message)
         else:
            message='no ticket found:'
            return render_template('deleteReservation.html', message=message)







    return render_template('deleteReservation.html')

@app.route('/flightSearch', methods=('GET', 'POST'))
def flightSearch():
     if request.method == "POST":
        
        departU = request.form.get("departU")
        arrivalU = request.form.get("arrivalU")
        dateU = request.form.get("dateU")
        
        flightResult = flights.find({'depart':departU,'arrival':arrivalU,'date':dateU})
        total_count = flights.count_documents({'depart':departU,'arrival':arrivalU,'date':dateU,'seats':{'$gt':0}})
        if total_count==0:
            message='sorry there is no flight with these arguments'
            return render_template('flightsSearch.html',message=message)
        

        return render_template('flightsSearch.html',flights=flightResult)
     

     return render_template('flightsSearch.html')

@app.route('/myaccount', methods=('GET', 'POST'))
def myaccount():
    if "email" in session:
      acc_mail=session['email'] 
      em_found=us.find_one({'email':acc_mail})
    if em_found:
        activationCode = str(random.randint(100000000000, 999999999999))
        us.update_one({'email':acc_mail},{'$set':{'status_u':False,'activate':activationCode}})
        message='user with mail:'+acc_mail+' ,your account deactivated,activation code:'+activationCode
        session["email"] = None

        return render_template('myaccount.html',message=message)
    else:
        message='you have to sign in first'
        return render_template('myaccount.html',message=message)



@app.route('/myreservations', methods=('GET', 'POST'))
def myreservations():
    return render_template('myreservations.html')

@app.route('/searchByDepart', methods=('GET', 'POST'))
def searchByDepart():
    if request.method == "POST":
        departR=request.form.get("departR")
        reserve_found= reservations.find({"departT": departR})
        if reserve_found:
            return render_template('searchByDepart.html',reserve_found=reserve_found)
        else:
            message='no reservation from:'+departR
            return render_template('searchByDepart.html',message=message)


       
    return render_template('searchByDepart.html')

@app.route('/showReservationsByPrice', methods=('GET', 'POST'))
def showReservationsByPrice():
    highestPrice=reservations.find().sort('price',-1).limit(1)
    lowestPrice=reservations.find().sort('price',1).limit(1)
    return render_template('showReservationsByPrice.html',highestPrice=highestPrice,lowestPrice=lowestPrice)

@app.route('/newestfirst', methods=('GET', 'POST'))
def newestfirst():
    reservnew=reservations.find().sort('dateT',-1)
    if reservnew:
     return render_template('newestfirst.html',reservnew=reservnew)
    else:
        message='you have no reservations'
        return render_template('newestfirst.html',message=message)

@app.route('/oldestfirst', methods=('GET', 'POST'))
def oldestfirst():
    reservold=reservations.find().sort('dateT',1)
    if reservold:
     return render_template('oldestfirst.html',reservold=reservold)
    else:
        message='you have no reservations'
        return render_template('oldestfirst.html',message=message)
    

@app.route('/reservationTicket', methods=('GET', 'POST'))
def reservationTicket():
    if request.method == "POST":
        codeT = request.form.get("codeT")
        nameT = request.form.get("nameT")
        passportT = request.form.get("passportT")
        creditT = request.form.get("creditT")
     
        user_found = us.find_one({"fullname": nameT})
       
        
        flight_found= flights.find_one({"code": codeT})
       

        if user_found:
            user_val=user_found['username']
            if flight_found:
                price_val=flight_found['price']
                flight_val=flight_found['seats']
                departT=flight_found['depart']
                arrivalT=flight_found['arrival']
                dateT=flight_found['date']
                TimeT=flight_found['time']
                new_seats=flight_val-1
                flights.update_one({'code':codeT},{'$set':{'seats':new_seats}})
                ticketCode=str(random.randint(10000, 100000))
                reservations.insert_one({'username':user_val,'price':price_val,'flightCode':codeT,'ticket_code':ticketCode,'name':nameT,'passport':passportT,'credit_card':creditT,"created_date": datetime.today().replace(microsecond=0),
                'departT':departT,'arrivalT':arrivalT,'dateT':dateT,'timeT':TimeT})
                message="You successfully reserve a ticket ,your ticket code is " + str(ticketCode)
                reservationT=reservations.find({'ticket_code':ticketCode})
              
                return render_template('reservationTicket.html', message=message,reservationT=reservationT)
                

            else:
                message='No flight found with this code'
                return render_template('reservationTicket.html', message=message)
        else:
             message='No user found with this  name'
             return render_template('reservationTicket.html', message=message)

    return render_template('reservationTicket.html')


#************************ADMINISTRATOR**********************************
@app.route('/adminSignIn', methods=('GET', 'POST'))
def adminSignIn():
      
    if request.method == "POST":
        usernameA = request.form.get("usernameA")
        emailA= request.form.get("emailA")
        passwordA = request.form.get("passwordA")

        #check if email exists in database
        
        email_found = ads.find_one({"emailA": emailA})

        if email_found :
           
            username_valA =email_found['usernameA']
            passwordcheckA = email_found['passwordA']
            statusA=email_found['status']
           
            
            if passwordA==passwordcheckA and username_valA==usernameA:
                if statusA :
                 return redirect(url_for('admin_menu'))
                else :
                 return redirect(url_for('admin_changePW'))
            else:
                
                message = 'Wrong credentials'
                return render_template('adminSignIn.html', message=message)
       
       

        else:
            message = 'Administratow not found not found'
            return render_template('adminSignIn.html', message=message)
    return render_template('adminSignIn.html')


@app.route('/admin_changePW', methods=('GET', 'POST'))
def admin_changePW():
      if request.method == "POST":
       
        emailA= request.form.get("emailA")
        passwordA = request.form.get("passwordA")

        #check if email exists in database
        
        email_found = ads.find_one({"emailA": emailA})

        if email_found :
           
            username_valA =email_found['usernameA']
            statusA=True
            ads.update_one({'usernameA':username_valA},{'$set':{'status':statusA,'passwordA':passwordA}})
            message='welcome on board'
            return render_template(admin_menu.html,message=message)
       
       
       

        else:
            message = 'Wrong Crentetials'
            return render_template('adminSignIn.html', message=message)


      return render_template('admin_changePW.html')


@app.route('/admin_menu', methods=('GET', 'POST'))
def admin_menu():
    return render_template('admin_menu.html')

@app.route('/createadministrator', methods=('GET', 'POST'))
def createadministrator():
     message = ''
    
     if request.method=='POST':
        
        emailA = request.form['emailA']
        usernameA = request.form['usernameA']
        passwordA = request.form['passwordA']
        

        #if found in database showcase that it's found 
        username_found = ads.find_one({"usernameA": usernameA})
        email_found = ads.find_one({"emailA": emailA})
        

        if username_found:
                message = 'There already is an administrator by that username'
                return render_template('createadministrator.html', message=message)
        if email_found:
                message = 'There already is an administrator by that email'
                return render_template('createadministrator.html', message=message)
        



        else:
           
            ads.insert_one({'emailA': emailA, 'usernameA': usernameA, 'passwordA': passwordA,'status':False})
            
            return redirect('admin_menu')

     return render_template('createadministrator.html')

@app.route('/newFlight', methods=('GET', 'POST'))
def newFlight():

     if request.method=='POST':
        
        depart = request.form['depart']
        arrival = request.form['arrival']
        price = request.form['price']
        duration = request.form['duration']
        timedep = request.form['time']
      
        datedep = request.form['date']
        code = depart[0]+arrival[0]+datedep[2:4]+datedep[5:7]+datedep[8:]+timedep[:2]
        seats=220

        flights.insert_one({'depart': depart, 'arrival': arrival, 'price': price,'duration':duration,'date':datedep,'time':timedep,'code':code,'seats':seats})
        message='Flight is registered with FlightCode: '+code
        return render_template('newFlight.html',message=message)
        
     return render_template('newFlight.html')

@app.route('/flightHandle', methods=('GET', 'POST'))
def flightHandle():
     if request.method=='POST':
        
        codeC = request.form['codeC']
        priceC = request.form['priceC']
        priceInt=int(priceC)
        if priceInt<=0:
             message="You can't give this price"
             return render_template('flightHandle.html',message=message)

        code_found = flights.find_one({"code": codeC})
        if code_found:
           seats_found=code_found['seats']
           if seats_found==220:
                 flights.update_one({'code':codeC},{'$set':{'price':priceC}})
                 message='you have succesfully change the price to: '+priceC
                 return render_template('flightHandle.html',message=message)


           else:
                message='this flight has allready reservations'
                return render_template('flightHandle.html',message=message)
        else:
            message='There is no flight with this code'
            return render_template('flightHandle.html',message=message)

     return render_template('flightHandle.html')

@app.route('/deleteFlight', methods=('GET', 'POST'))
def deleteFlight():
     if request.method=='POST':
        
        codeC = request.form['codeC']
       
        code_found = flights.find_one({"code": codeC})
        if code_found:
           seats_found=code_found['seats']
           if seats_found==220:
                 flights.delete_one({'code':codeC})
                 message='you have succesfully delete the flight'+codeC
                 return render_template('admin_menu.html',message=message)


           else:
                message='this flight has allready reservations'
                return render_template('deleteFlight.html',message=message)
        else:
            message='There is no flight with this code'
            return render_template('deleteFlight.html',message=message)

     return render_template('deleteFlight.html')

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)