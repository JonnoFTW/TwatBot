import re
import random
triggers = {}
regex = re.compile("\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)

def default(conn):
    #Handle 352
    pieces = conn.dataN['raw'].split()
    if pieces[1] == "352":
        conn.conn.users[pieces[3]].add(pieces[7])
    #handle all other messages
    
    # Handle privmsg
    #print "got here"
    #print conn.dataN
    if conn.dataN['cmd'] == "PRIVMSG":
        cleaned = regex.sub("",conn.dataN['msg'])
      #100% MAVERICK  print cleaned
        c = 0
        for i in conn.conn.users[conn.dataN['chan']]:
            if i in cleaned:
                c += 1
        if c > 5:
            msgs = ["100% MAVERICK",
                    "I TOLD YOU DAWG, I TOLD YOU ABOUT THE HERSY",
                    "You're attitude is not conductive too the acquired stratosphere",
                    "You will pass with flying carpets like it's a peach of cake",
                    "I cannot turn a blonde eye to these glaring flaws in your rhetoric",
                    "I have zero taller ants to you're ant ticks"]
            conn.sendMsg(" ".join([".kb",conn.dataN['fool'],random.choice(msg)]))
