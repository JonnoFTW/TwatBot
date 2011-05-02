import random
help = """^^ sends the previous line to twitter. Can't quote yourself either. ^^ n sends the nth line from the scrollback twitter. View with ^scroll. n is n places from the start of the scroll starting at 0. ^last gets the last tweet from Buttsworth. '^last user' gets the last tweet from user."""

def tweet(conn):
    if conn.dataN['fool'] not in conn.banned:
        if ("".join(conn.chans[conn.dataN['chan']][len(conn.chans[conn.dataN['chan']])-1].split())) != "":
            if conn.dataN['fool'] == conn.chans[conn.dataN['chan']][len(conn.chans[conn.dataN['chan']])-1].split(':')[0]:
                conn.sendMsg("Can't quote yourself",conn.dataN['chan'])
            else:
                if len(conn.dataN['words']) > 1:
#		   if conn.chans[conn.dataN['words']][int(conn.dataN['words'][1])] = 
                   toSend = conn.chans[conn.dataN['chan']][int(conn.dataN['words'][1])]
		else:
                    toSend = (conn.chans[conn.dataN['chan']].pop())[:140]
                print(toSend)
                conn.setTwit(toSend,conn.dataN['chan'])
                spaces = '!'*(random.randint(0,2))  
                conn.sendMsg('Sending to twitter'+spaces,conn.dataN['chan']) 

def last(conn):
    if len(conn.dataN['words']) > 1:
        conn.sendMsg(conn.getTwit(filter(lambda x: ord(x) > 16,conn.dataN['words'][1])) ,conn.dataN['chan'])
    else:
        conn.sendMsg(conn.getTwit('Buttsworth_').replace('/\r\n|\r|\n/g',''),conn.dataN['chan'])


triggers = {'^^':tweet,'^last':last}
