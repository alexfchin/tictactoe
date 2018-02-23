from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
import  datetime
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

@app.route("/ttt/",  methods=['GET'])
def start_page():
    return render_template('ttt.html')

@app.route("/ttt/", methods=['POST'])
def welcome_page():
    date = str(datetime.datetime.now())[:10]
    return render_template("welcome.html",  date = date) 

@app.route("/ttt/tictac", methods=['GET'])
def tictac():
    return render_template('tictac',ttt=tictactoe)

@app.route("/ttt/play", methods=['POST'])
def ticktack():
    ttt = request.get_json()
    ttt = checkWin(ttt)
    if 'winner' in ttt and ttt['winner']!=' ':
        return jsonify(ttt)
    ttt= compMove(ttt)
    ttt= checkWin(ttt)
    return jsonify(ttt)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)