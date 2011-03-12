help ="Send the the line preceeding ^^ to @Buttsworth_ on twitter. List all cmds with ^cmds, specific help with ^xyz help .http://twitter.com/#!/Buttsworth_"

def shelp(conn):
    conn.sendMsg(help,conn.dataN['chan'])
triggers = { '^help':shelp,'^about':shelp}
