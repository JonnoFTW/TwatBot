help = "Admin only, joins or parts the specified channel"
def join(conn):
    try:
        chan = conn.dataN['words'][1]
        if chan[0] != '#':
            conn.sendMsg("Channels must start with a #")
        elif chan in conn.chans.keys():
            conn.sendMsg('I\'m already in that channel')
        else:
            conn.joinChan(chan)
    except IndexError:  
        conn.sendMsg('Please provide a channel to join')

def part(conn):
    try:
        chan = conn.dataN['words'][1]
        if chan not in conn.chans.keys():
            conn.sendMsg('I\'m not in that channel')
        else:
            del conn.chans[chan]
            conn.conn.chanOP(chan,'PART')
    except IndexError, e:
        conn.sendMsg("Please specify a joined channel to part from")
        
def msg(conn):
    try:
        conn.conn.connections[int(conn.dataN['words'][1])].conn.sendMsg(' '.join(conn.dataN['words'][3:]),conn.dataN['words'][2])
    except Exception, e:
        conn.sendMsg("Usage is ^msg <serverId> <channel> <message>")
def servers(conn):
    names = []
    for i in conn.conn.connections:
        names.append(i.server)
    conn.sendMsg('Current servers are: '+(', '.join(names)))
triggers = {'^join':join,'^part':part,'^msg':msg,'^servers':servers}
