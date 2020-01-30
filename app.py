from flask import Flask, jsonify, request, render_template, url_for
from flask_pymongo import MongoClient
import hashlib
import os
import yagmail
from random import random
# Module for password validation 
import bcrypt

array = []

# connecting to my local database address
client= MongoClient('mongodb://localhost:27017')

# Creating a new mongo database
db= client['Users']

# create a collection withn the database
Signup_Passwords= db.Signup_Passwords

# Setting up the flask server 
app = Flask(__name__)

# Create the index route
@app.route('/')
def index():
    # render the index page
    return render_template("login.html")

# Route to sigup for an account
@app.route('/signup')
def signup():
    # return signup page for user to signup for an account
    return render_template("signup.html") 

# After they have signup: save in the database and redirect them to login
@app.route('/create', methods = ['POST', 'GET'])
def create():
    # Getting user input form the form
    firstname= request.form.get("firstname")
    lastname= request.form.get("lastname")
    username= request.form.get("username")
    password= request.form.get("password")
    email= request.form.get("email")

    # changing the first letter in the input to capital if it is alphabatical
    if lastname.isalpha():
        last_name=lastname.capitalize()
      
    if firstname.isalpha():
        first_name=firstname.capitalize()
    
    # simple validation for user name to !=null
    if (len(username) <1):
        return render_template("error.html")

    # simple password length validation 
    if (len(password) <6):
        return render_template('passerror.html')   
    else:

        # Advoidance of repeated user name in the database.
        username_validate = Signup_Passwords.find()

        # Searching database for similarity in user name
        for item in username_validate:
            db_username = (item["User Name"])
            if username == db_username:
                # render a simple html error page
                return render_template('username_error.html')

        # Advoidance of repeated emails in the database.
        email_validate = Signup_Passwords.find()

        # Searching database for similarity in emails
        for item in email_validate:
            db_email = (item['email'])
            if email == db_email:
                # render a simple html error page
                return render_template('email_error.html')

        # encode the password to utf standards 
        passwords =password.encode('utf-8')
        # the hashed fomula
        salt = bcrypt.gensalt()
        # hashed the password
        hashed = bcrypt.hashpw(passwords, salt)

        signups= {
            'First Name': first_name,
            'Last Name': last_name,
            'User Name': username,
            'Password': hashed,
            'email': email
        }
        result= Signup_Passwords.insert_one(signups)
        
        # Return the sucess after all validation has been done
        return render_template('signupsucess.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    # Getting user login username or email
    name= request.form.get("name")
    password= request.form.get("password")
    
    # Searching in the signup collection in the database for login validation 
    username_validate = Signup_Passwords.find()

    for item in username_validate:
       username = (item["User Name"])
       email = (item["email"])
       if name == username or name == email:
            pas= (item["Password"])
            if bcrypt.checkpw(password.encode('utf-8'), pas.encode('utf-8')):
            # Here you can return to the user the home page/but for now we are just returning a simple message
                return "You have sucessfully login"
            else:
                return "it does not match"
    return 'worng password' 

@app.route('/forget', methods = ['GET','POST'])
def forget():
    
    return render_template("forget.html")   
@app.route('/generate', methods = ['GET','POST'])
def generate():
    email= request.form.get("email")

    email_validate = Signup_Passwords.find()

    for item in email_validate:
        db_email = (item['email'])
        if email == db_email:
            array.append(email)
            # Generating random pin for verification email
            # value = random()

            # Type your server email id here, to be able to sent message to client
            yag = yagmail.SMTP("your_email@gmail.com")
            contents = [
                "your verification pin is 0773445258757",
            ]

            # Send verify pin to user email, replace the user_email@gmail.com with a actual email.
            yagmail.SMTP('your_email@gmail.com').send('user_email@gmail.com', 'subject', contents)
            return render_template("verify.html")
        else:
            return render_template("failure.html")

@app.route('/verify', methods = ['GET','POST'])
def verify():
    # Geting verification pin from user input
    verify = request.form.get("verify")

    if verify == "0773445258757":
        return render_template ("reset.html")
   
@app.route('/reset', methods = ['GET','POST'])
def reset():
    # Get the user reset password from input
    password = request.form.get("password")

    email_validate = Signup_Passwords.find()

    for item in email_validate:
        db_email = (item['email'])
        if array[0] == db_email:
            pas= (item["Password"])
            passwords = password.encode('utf-8')
            # the hashed fomula
            salt = bcrypt.gensalt()
            # hashed the password
            hashed = bcrypt.hashpw(passwords, salt)
           
        #    reseting user password from database end
            myquery = { "email": array[0]}
            # setting new hashed password 
            newvalues = { "$set": { "Password": hashed } }
            # updating the database
            Signup_Passwords.update_one(myquery, newvalues)
            array.remove(0)

            # redirecting to login page
            return render_template ("pass_reset.html")

    return render_template ("login.html")        

if __name__ == "__main__":
    app.run()
