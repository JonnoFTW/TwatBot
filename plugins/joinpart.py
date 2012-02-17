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
triggers = {'^join':join,'^part':part}
