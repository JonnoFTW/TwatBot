help = "List channels currently in"
def chans(conn):
    conn.sendMsg('Currently in: '+(', '.join(conn.chans.keys())),conn.dataN['chan'])
    
triggers = {'^chans':chans}
