import  datetime
import sendmail
import keygen
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient

client = MongoClient()
db = client.ttt #specify db name
accounts = db.accounts

app = Flask(__name__)
api=Api(app)



tictactoe={ 'winner' : ' ', 
            'grid' :[' ',' ',' ',' ',' ',' ',' ',' ',' ']
            }
def checkWin(ttt):
    if ttt['grid'][0]==ttt['grid'][1] and ttt['grid'][0]==ttt['grid'][2] and (ttt['grid'][0]=="O" or ttt['grid'][0]=="X"):
        ttt['winner']= ttt['grid'][0]
    elif ttt['grid'][3]==ttt['grid'][4] and ttt['grid'][3]==ttt['grid'][5] and (ttt['grid'][3]=="O" or ttt['grid'][3]=="X"):
        ttt['winner']= ttt['grid'][3]
    elif ttt['grid'][6]==ttt['grid'][7] and ttt['grid'][6]==ttt['grid'][8] and (ttt['grid'][6]=="O" or ttt['grid'][6]=="X"):
        ttt['winner']= ttt['grid'][6]
    elif ttt['grid'][0]==ttt['grid'][3] and ttt['grid'][0]==ttt['grid'][6] and (ttt['grid'][0]=="O" or ttt['grid'][0]=="X"):
        ttt['winner']= ttt['grid'][0]
    elif ttt['grid'][1]==ttt['grid'][4] and ttt['grid'][1]==ttt['grid'][7] and (ttt['grid'][1]=="O" or ttt['grid'][1]=="X"):
        ttt['winner']= ttt['grid'][1]
    elif ttt['grid'][2]==ttt['grid'][5] and ttt['grid'][2]==ttt['grid'][8] and (ttt['grid'][2]=="O" or ttt['grid'][2]=="X"):
        ttt['winner']= ttt['grid'][2]
    elif ttt['grid'][0]==ttt['grid'][4] and ttt['grid'][0]==ttt['grid'][8] and (ttt['grid'][0]=="O" or ttt['grid'][0]=="X"):
        ttt['winner']= ttt['grid'][0]
    elif ttt['grid'][2]==ttt['grid'][4] and ttt['grid'][2]==ttt['grid'][6] and (ttt['grid'][2]=="O" or ttt['grid'][2]=="X"):
        ttt['winner']= ttt['grid'][2]
    
    return ttt
def compMove(ttt):
    if ttt['grid'][4] == ' ':
        ttt['grid'][4] = 'X' 
    elif ttt['grid'][1] == ' ':
        ttt['grid'][1] = 'X' 
    elif ttt['grid'][7] == ' ':
        ttt['grid'][7] = 'X' 
    elif ttt['grid'][0] == ' ':
        ttt['grid'][0] = 'X' 
    elif ttt['grid'][2] == ' ':
        ttt['grid'][2] = 'X' 
    elif ttt['grid'][8] == ' ':
        ttt['grid'][8] = 'X' 
    elif ttt['grid'][6] == ' ':
        ttt['grid'][6] = 'X' 
    elif ttt['grid'][3] == ' ':
        ttt['grid'][3] = 'X' 
    elif ttt['grid'][5] == ' ':
        ttt['grid'][5] = 'X' 
    return ttt

@app.route("/ttt/", methods=['GET','POST'])
def start_page():
    if request.method == 'POST' and request.form['email'] is not None: #signup form
        return redirect(url_for('adduser'))
    elif request.method == 'POST' and request.form['email'] is None: #login
        return redirect(url_for('login'))
    else:
        return render_template('new.html')
# @app.route("/ttt/", methods=['POST'])
# def welcome_page():
#     date = str(datetime.datetime.now())[:10]
#     return render_template("welcome.html",  date = date) 

@app.route("/ttt/play", methods=['POST'])
def ticktack():
    ttt = request.get_json()
    ttt = checkWin(ttt)
    if 'winner' in ttt and ttt['winner']!=' ':
        return jsonify(ttt)
    ttt= compMove(ttt)
    ttt= checkWin(ttt)
    return jsonify(ttt)

#Add User to DB
#need to get form data from sign up, create json object, send to db
@app.route("/adduser", methods=['POST'])
def adduser():
    un = str(request.form.get('name'))
    pw = str(request.form.get('pass'))
    mail = str(request.form.get('email'))
    ky= keygen.gen()
    new_user = {"username": un, "password": pw, "email": mail, "key":ky} 
    user_id = accounts.insert_one(new_user).inserted_id
    sendmail.send(mail,un,ky)
    return render_template('new.html') 
@app.route("/verify", methods=['POST','GET'])
def verify():
    #sendmail.send("iiacherry@aim.com", "veriifying")
   # return request.args.get('email')+request.args.get('key')
    if request.method =='GET':
        email=request.args.get('email')
        key=request.args.get('key')
        if email is None or key is None:
            return render_template('verify.html')
    else:
        email= str(request.form.get('email'))
        key= str(request.form.get('key'))
    if db.accounts.find_one({"email":email}) is not None and key=="abracadabra":
        db.accounts.update_many({"email":email},{'$set':{'verified':'true'}})
        return email+", you have been verified"
    elif db.accounts.find_one({"email":email, "key":key})is not None:
        db.accounts.update_one({"email":email, "key":key},{'$set':{'verified':'true'}})
        return email+", you have been verified"
    else:
        return "key or email was invalid"
    
@app.route('/login', methods=['POST'])
def login():
    un = str(request.form.get('name'))
    pw = str(request.form.get('pass'))
    if db.accounts.find_one({"username": un, "password": pw, "verified":"true"}) is not None:
#PUT COOKIE STUFF IN HERE PLS
        return render_template('welcome.html')
    else:
        return "Please check your username/ password or verify your account @ /verify"  


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
