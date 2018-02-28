import  datetime
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
    new_user = {"username": un, "password": pw, "email": mail} 
    user_id = accounts.insert_one(new_user).inserted_id
    if db.accounts.find_one({"email": "john@gmail.com"}):
        return render_template('welcome.html')
    return render_template('new.html')
    
@app.route('/login', methods=['POST'])
def login():
    # if db.acccounts.find_one({"username": "John", "password": "pass"}):
    #     return render_template('new.html')
    return render_template('welcome.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
