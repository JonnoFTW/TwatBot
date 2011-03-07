
def scroll(conn):
    if len(conn.dataN['words']) > 1:
        try:
            sendMsg("Scroll at "+ conn.dataN['words'][1] + ": " +list(reversed(conn.chans[dataN['chan']]))[int(words[1])],dataN['chan'])
        except:
            sendMsg("Perhaps if you used a number < 10",dataN['chan'])
    else:
         sendMsg(str(list(conn.chans[dataN['chan']])),dataN['chan'])
triggers = {'^scroll':scroll}



