def tweet(conn):
    if conn.dataN['fool'] not in conn.banned:
        if ("".join(conn.chans[conn.dataN['chan']][len(conn.chans[conn.dataN['chan']])-1].split())) != "":
            if conn.dataN['fool'] == conn.chans[conn.dataN['chan']][len(conn.chans[conn.dataN['chan']])-1].split(':')[0]:
                conn.sendMsg("Can't quote yourself",conn.dataN['chan'])
            else:
                toSend = (conn.chans[conn.dataN['chan']].pop())[:140]
                print(toSend)
                conn.setTwit(toSend,conn.dataN['chan'])
                spaces = ' '*(random.randint(1,5))  
                conn.sendMsg('Sending to twitter!'+spaces,conn.dataN['chan']) 

def last(conn):
    if len(conn.dataN['words']) > 1:
        conn.sendMsg(conn.getTwit(conn.dataN['words'][1]),conn.dataN['chan'])
    else:
        conn.sendMsg(conn.getTwit('Buttsworth_'),conn.dataN['chan'])


triggers = {'^^':tweet,'^last':last}
