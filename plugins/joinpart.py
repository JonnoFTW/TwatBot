help = "Admin only, joins or parts the specified channel"
def joinpart(conn):
    jp = conn.dataN['words'][0]
    if len(conn.dataN['words']) > 1:
        chan = conn.dataN['words'][1]
        if chan[0] != '#':
            conn.sendMsg('Please format the channel properly',conn.dataN['chan'])
        elif jp == '^part':    
            if chan not in (conn.chans.keys()):
                conn.sendMsg('I\'m not in that channel',conn.dataN['chan'])
            else:
                del conn.chans[chan]
                conn.chanOP(chan,'PART')
        elif jp == '^join':
            if chan in (conn.chans.keys()):
                conn.sendMsg('I\'m already in that channel',conn.dataN['chan'])
            else:
                conn.joinChan(chan)
    else:  
        conn.sendMsg('Please provide a channel to '+jp[1:],conn.dataN['chan'])


triggers = {'^join':joinpart,'^part':joinpart}
