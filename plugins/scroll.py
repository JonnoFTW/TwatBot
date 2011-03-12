import random
help = "Displays the scrollback for use with ^^. Starts at index 0 on the left. Stores 10 last quotes per channel"
def scroll(conn):
    if len(conn.dataN['words']) > 1:
        try:
            conn.sendMsg("Scroll at "+ conn.dataN['words'][1] + ": " + conn.chans[conn.dataN['chan']][int(conn.dataN['words'][1])],conn.dataN['chan'])
        except Exception, err:
            conn.sendMsg("Perhaps if you used a number < 10, "+str(err)+ (' '*(random.randint(1,5))),conn.dataN['chan'])
    else:
         conn.sendMsg(str(list(conn.chans[conn.dataN['chan']])),conn.dataN['chan'])
triggers = {'^scroll':scroll}



