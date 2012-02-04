# coding=utf-8
import re
import random
triggers = {}
regex = re.compile("\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
import cPickle
def default(conn):
    #Handle 352
    pieces = conn.dataN['raw'].split()
#    print conn.dataN
    if pieces[1] == "352":
        try:
            conn.conn.users[pieces[3]].add(pieces[7])
        except:
            print conn.dataN
    #handle all other messages
    # Handle privmsg
    if '^ÂÊÎÔÛâêîôû????????????????????????????????????????????????????????????????????' in conn.dataN['msg']:
        conn.sendMsg(" ".join(['ban',conn.dataN['chan'],conn.dataN['fool'],'SUCH AN EDGY AND HIP HACKER']),'chanserv')
    if conn.dataN['cmd'] == "PRIVMSG":
        cleaned = regex.sub("",conn.dataN['msg'])
      #100% MAVERICK  print cleaned
        if conn.dataN['chan'] in conn.conn.chans:
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
                        "I have zero taller ants to you're ant ticks",
                        "For you even to imply that one has to have seen insane, a ridiculous grasp at straws to try and make my point less",
                        "TRY GETTING A RESERVATION AT #PERWL NOW YOU STUPID FUCKING BASTARD!",
                        "TRY GETTING A RESERVATION AT PERWLCON NOW YOU STUPID FUCKING BASTARD!"]
                
                conn.sendMsg(" ".join(["ban",conn.dataN['chan'],conn.dataN['fool'],random.choice(msgs)]),'chanserv')
        if conn.dataN['fool'] in conn.conn.admins:
            if conn.dataN['words'][0] == "^nazi":
              try:
                if conn.dataN['words'][1] == "on":
                  conn.conn.nazi = True
                  conn.sendMsg("Spelling nazi mode engaged")
                elif conn.dataN['words'][1] == "off":
                  conn.conn.nazi = False
                  conn.sendMsg("Spelling nazi mode disengaged")
                else:
                  conn.sendMsg("^nazi on|off")
              except IndexError, e:
                  conn.sendMsg("^nazi on|off")
                 
                   
        if conn.conn.nazi:
            try:
                for i in cleaned.split():
                    if i in conn.conn.mistakes:
                        conn.sendMsg(conn.dataN['fool']+ ": it's spelt '"+conn.conn.mistakes[i]+"' ")
                        break
            except AttributeError, e:
                conn.conn.mistakes = None
                pkl = open('plugins/mistakes.pkl','rb')
                conn.conn.mistakes = cPickle.load(pkl)
                conn.sendMsg("loaded spellings")
                pkl.close()
