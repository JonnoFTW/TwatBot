help = "Plays a dragon eats you on #futaba@rizon"
def play(conn):    
    if not conn.playing:
        conn.sendMsg('!play',conn.dataN['chan'])
        conn.dataN['playing'] = True
    else:
        msg = conn.dataN['msg']
        if msg.find("You have already played today") != -1 or msg.find("1... A dragon eats you.") != -1:
            conn.playing = False 
        elif msg.find('Type !roll') != -1 or  msg.find('You are already playing') != -1:
            conn.sendMsg('!roll',conn.dataN['chan'])

triggers = {'^play':play}     

