def tweet(conn):
    if conn.dataN['fool'] not in conn.banned:
        if ("".join(conn.chans[conn.dataN['chan']][len(conn.chans[conn.dataN['chan']])-1].split())) != "":
            if conn.dataN['fool'] == conn.chans[conn.dataN['chan']][len(conn.chans[conn.dataN['chan']])-1].split(':')[0]:
                conn.sendMsg("Can't quote yourself",conn.dataN['chan'])
            else:
                toSend = (conn.chans[conn.dataN['chan']].pop())[:140]
                print(toSend)
                setTwit(toSend,conn.dataN['chan'])
                spaces = ' '*(random.randint(1,5))  
                conn.sendMsg('Sending to twitter!'+spaces,conn.dataN['chan']) 



def last(conn):
    if len(conn.dataN['words']) > 1:
        conn.sendMsg(getTwit(conn.dataN['words'][1]),conn.dataN['chan'])
    else:
        conn.sendMsg(getTwit('Buttsworth_'),conn.dataN['chan'])

def getTwit(user):
    try:
        result = api.GetUserTimeline(user)[0].text
    except:
        result = 'Could not get twitter'
    return result

def setTwit(msg,chan):
    try:
        result = api.PostUpdate(msg)
    except:
        conn.sendMsg( 'Could not update twitter',chan)
 
triggers = {'^^':tweet,'^last':last}
