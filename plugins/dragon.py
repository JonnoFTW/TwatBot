def play(dataN):
    if not dataN['playing']:
        sendMsg('!play',dataN['chan'])
        dataN['playing'] = True
    else:
        msg = dataN['msg']
        if msg.find("You have already played today") != -1 or msg.find("1... A dragon eats you.") != -1:
            dataN['playing'] = False 
        elif msg.find('Type !roll') != -1 or  msg.find('You are already playing') != -1:
            sendMsg('!roll',dataN['chan'])
    return dataN
triggers = {'^play':play}     

