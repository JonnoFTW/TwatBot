def banned(conn):
    if len(conn.dataN['words']) > 1 and conn.dataN['fool'] in conn.admins:
        ban(words[1])
        conn.banned.append(conn.dataN['words'][1])
        toSend = conn.dataN['words'][1]+' is now banned from tweeting'
        conn.sendMsg(toSend,conn.dataN['chan'])
        setTwit(toSend)
    else:
        conn.sendMsg('Current bans are: '+(', '.join(conn.banned)),conn.dataN['chan'])

def ban(nick,conn):
    f = open('banned','a')
    f.write(nick+'\n')
    f.close()
    return True

triggers = {'^ban':banned,'^bans':banned}
