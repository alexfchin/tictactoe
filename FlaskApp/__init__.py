import datetime
import sendmail
import keygen
import tictac
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient

client = MongoClient()
db = client.ttt #specify db name
accounts = db.accounts

app = Flask(__name__)
api=Api(app)

@app.route("/ttt/", methods=['GET','POST'])
def start_page(): #session works
    if request.cookies.get('cookiename') is not None:
        un= request.cookies.get('cookiename')
        ttt=db.current.find_one({"username":un},{"_id":0,"username":1,"id":1,"grid":1,"start_date":1,"winner":1})
        return render_template('welcome.html',ttt=ttt)
    return render_template('new.html')

@app.route("/ttt/play", methods=['POST'])
def ticktack():
    #return jsonify({"status":"OK"})
    un= request.cookies.get('cookiename')
    ttt=db.current.find_one({"username":un},{"_id":0,"username":1,"id":1,"grid":1,"start_date":1,"winner":1})
    j=request.get_json()
    mv=j['move']
    ttt['grid'][mv]='O' 
    db.current.update_one({"username":un},{'$set':{'grid':ttt['grid']}})
 # ttt = checkWin(ttt)
   # if 'winner' in ttt and ttt['winner']!=' ':
   #     return jsonify(ttt)
    #ttt= compMove(ttt)
    #ttt= checkWin(ttt)
    return jsonify(ttt)
#Add User to DB
#need to get form data from sign up, create json object, send to db
@app.route("/adduser", methods=['POST'])
def adduser():
    user=request.get_json()
    un=user['username']
    pw=user['password']
    mail=user['email']
    ky= keygen.gen()
    new_user = {"username": un, "password": pw, "email": mail, "key":ky} 
    user_id = accounts.insert_one(new_user).inserted_id
    sendmail.send(mail,un,ky)
    return jsonify({"username": un, "password": pw, "email": mail, "key":ky,"status":"OK"})

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
        user=request.get_json()
        email=user['email']
        key=user['key']
    if db.accounts.find_one({"email":email}) is not None and key=="abracadabra":
        db.accounts.update_many({"email":email},{'$set':{'verified':'true'}})
        return jsonify({"status":"OK"})
    elif db.accounts.find_one({"email":email, "key":key})is not None:
        db.accounts.update_one({"email":email, "key":key},{'$set':{'verified':'true'}})
        return jsonify({"status":"OK"})
    else:
        return jsonify({"status":"ERROR"})
    
@app.route('/login', methods=['POST'])
def login():
    attempt= request.get_json()
    un=attempt['username']
    pw=attempt['password']
    if db.accounts.find_one({"username": un, "password": pw, "verified":"true"}) is not None:
#PUT COOKIE STUFF IN HERE PLs
       # resp=make_response(render_template('welcome.html'))
       # resp.set_cookie('cookiename',un)
        #return jsonify({"status":"OK"})
        out=jsonify({"status":"OK"})
        out.set_cookie('cookiename',un)
        return out
    else:
       # return "Please check your username/ password or verify your account @ /verify"  
        return jsonify({"status":"ERROR"})

@app.route('/logout', methods=['POST'])
def logout():
    out=jsonify({"status":"OK"})
    out.set_cookie('cookiename','',expires=0)
    return out



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
