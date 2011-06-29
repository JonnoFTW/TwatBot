help = "Shows how many times the specified user has been 'studio laughter'd"

def report(conn):
    try:
        fool = conn.dataN['words'][1]
    except IndexError, e:
        fool = conn.dataN['fool']
    try:
        conn.sendMsg(fool+" has been laughed at %d times" % (conn.laughter[fool]),conn.dataN['chan'])
    except:
        conn.sendMsg(fool+' has not been laughed at',conn.dataN['chan'])

triggers = { '^studio':report}
