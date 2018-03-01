#tictactoe={ 'winner' : ' ', 
 #           'grid' :[' ',' ',' ',' ',' ',' ',' ',' ',' ']
 #           }
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
        ttt['grid'][4] = 'O' 
    elif ttt['grid'][1] == ' ':
        ttt['grid'][1] = 'O' 
    elif ttt['grid'][7] == ' ':
        ttt['grid'][7] = 'O' 
    elif ttt['grid'][0] == ' ':
        ttt['grid'][0] = 'O' 
    elif ttt['grid'][2] == ' ':
        ttt['grid'][2] = 'O' 
    elif ttt['grid'][8] == ' ':
        ttt['grid'][8] = 'O' 
    elif ttt['grid'][6] == ' ':
        ttt['grid'][6] = 'O' 
    elif ttt['grid'][3] == ' ':
        ttt['grid'][3] = 'O' 
    elif ttt['grid'][5] == ' ':
        ttt['grid'][5] = 'O' 
    return ttt
