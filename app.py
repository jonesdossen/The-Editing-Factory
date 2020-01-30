from flask import Flask, jsonify, request, render_template, url_for
from flask_pymongo import PyMongo
from flask_pymongo import MongoClient

# connecting to my local database address
client= MongoClient('mongodb://localhost:27017')

# Creating a new database

db= client['test-database']
print(db)

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)

# RETURN THE LOGIN PAGE TO THE USER
@app.route('/')
def index():
    # mongo.save
    # online_users = mongo.db.use
    return render_template("index.html")

# GETING INPUT FROM THE LOGIN PAGE.
@app.route("/submit", methods=['GET'])
def login():
    # GET THE SUBMITED USER LOGIN NAME AND PASSWORD
    name= request.form.get("name")
    # name= request.form.get("name")
    # password=request.form.get("password")
    # result=  name+name
    # print(result)

    # VALIDATE USER INPUT HERE TO CHECK IF IT'S CORRECT(ADMIN) 

    # RETURN THE DATABASE IN A TABULAR FORM
    return render_template("main.html")

# GETING AND STORING INFOMATION IN THE DATABASE
@app.route('/student_info', methods=['GET'])
def info():
    # GET STUDENT MANE, COURSE AND SCHEDULE  
    name= request.form.get("name")
    course= request.form.get("course")
    schedule= request.form.get("schedule")

if __name__ == "__main__":
    app.run()