import random
help = "Displays the scrollback for use with ^^. Starts at index 0 on the left. Stores 10 last quotes per channel"
def scroll(conn):
    if len(conn.dataN['words']) > 1:
        try:
            conn.sendNot("Scroll at "+ conn.dataN['words'][1] + ": " + conn.chans[conn.dataN['chan']][int(conn.dataN['words'][1])])
        except Exception, err:
            conn.sendNot("Perhaps if you used a number < 10, "+str(err)+ (' '*(random.randint(1,5))))
    else:
        count = 0
        tosend = ''
        for i in list(conn.chans[conn.dataN['chan']]):
            tosend+= str(count)+': '+i.decode('utf-8','replace')+' | '
            count +=1
        conn.sendNot(tosend)
triggers = {'^scroll':scroll}



