help = "^ban shows current bans. ^ban user bans user if you're and admin"
def banned(conn):
    if len(conn.dataN['words']) > 1 and conn.dataN['fool'] in conn.conn.admins:
        ban(conn.dataN['words'][1])
        conn.conn.banned.append(conn.dataN['words'][1])
        toSend = conn.dataN['words'][1]+' is now banned from tweeting'
        conn.sendMsg(toSend,conn.dataN['chan'])
    else:
        conn.sendMsg('Current bans are: '+(', '.join(conn.conn.banned)),conn.dataN['chan'])

def ban(nick):
    f = open('banned','a')
    f.write(nick+'\n')
    f.close()
    return True

def nickShow(conn):
    #Show users in board
    conn.sendMsg(str(len(conn.conn.users[conn.dataN['words'][1]])) , conn.dataN['fool'])
    conn.sendMsg(str(conn.conn.users[conn.dataN['words'][1]]) , conn.dataN['fool'])
    
def unban(conn):
    conn.sendMsg("test")
    try:
        conn.sendMsg("Unbanning "+conn.dataN['words'][1])
    except IndexError:
        conn.sendMsg("please specify someone to unban")
    f = open('banned','w')
    b = []
    for i in conn.banned:
        if i == conn.dataN['words'][1]:
            continue
        elif i not in b:
            f.write(i+'\n')
            b.append(i)
    f.close()
    conn.conn.banned = b
    
    
triggers = {'^ban':banned,'^bans':banned,'^nicks':nickShow,"^unban":unban}
