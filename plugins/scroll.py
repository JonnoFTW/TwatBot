import random
def scroll(conn):
    if len(conn.dataN['words']) > 1:
        try:
            conn.sendMsg("Scroll at "+ conn.dataN['words'][1] + ": " +list(reversed(conn.chans[conn.dataN['chan']]))[int(words[1])],conn.dataN['chan'])
        except:
            conn.sendMsg("Perhaps if you used a number < 10"+ (' '*(random.randint(1,5))),conn.dataN['chan'])
    else:
         conn.sendMsg(str(list(conn.chans[conn.dataN['chan']])),conn.dataN['chan'])
triggers = {'^scroll':scroll}



