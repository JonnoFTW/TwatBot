# coding=utf-8
import re
import random
triggers = {}
regex = re.compile("\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
import cPickle
def default(conn):
    if conn.conn.printAll:
        print conn.dataN
    #Handle 352
    pieces = conn.dataN['raw'].split()
#    print conn.dataN
    if pieces[1] == "352":
        try:    
            print "Adding user: %s" % (pieces[7])
            conn.conn.users[pieces[3]].add(pieces[7]) 
        except:
        
            print "Error adding user, ",conn.dataN
    #handle all other messages
    elif conn.dataN['cmd'] == "JOIN":
        print "A user joined "+conn.dataN['chan']+": "+conn.dataN['fool']
        try:
            if conn.dataN['fool']:
                conn.conn.users[conn.dataN['chan']].add(conn.dataN['fool'])
        except KeyError:
            conn.conn.users[conn.dataN['chan']] = set()
    elif conn.dataN['cmd'] == "PART":
        try:
            print "A user left: "+conn.dataN['chan']+": "+conn.dataN['fool']
            conn.conn.users[conn.dataN['chan']].remove(conn.dataN['fool'])
        except KeyError:
            pass

    # Handle privmsg
    elif '^ÂÊÎÔÛâêîôû????????????????????????????????????????????????????????????????????' in conn.dataN['msg']:
        conn.sendMsg(" ".join(['ban',conn.dataN['chan'],conn.dataN['fool'],'SUCH AN EDGY AND HIP HACKER']),'chanserv')
    elif conn.dataN['cmd'] == "PRIVMSG":
        cleaned = regex.sub("",conn.dataN['msg'])
      #100% MAVERICK  print cleaned
        if not conn.dataN['words']:
            return
        if conn.dataN['chan'] in conn.conn.chans:
            c = 0
            detections = []
            for i in conn.conn.users[conn.dataN['chan']]:
                if i in cleaned:
                    detections.append(i)
                    c += 1
            if detections:
                print "Detected: "+(' '.join(detections))
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
            cmd = conn.dataN['words'][0]
            if cmd == '^nick':
                try:
                    nick = conn.dataN['words'][1]
                    conn.conn.ircCom('NICK',conn.dataN['words'][1])
                    conn.sendMsg("Nick set to "+nick)
                except IndexError:
                    conn.sendMsg("Please specify a nick to use")
            elif cmd == "^who":
                conn.sendMsg("Requesting users")
                conn.conn.whoInit()
            elif cmd == '^log':
                conn.conn.printAll = not conn.conn.printAll
                conn.sendMsg("Logging is now: "+str(conn.conn.printAll))
            elif cmd == '^debug':
                conn.conn.debug = not conn.conn.debug
                conn.sendMsg("Debugging is now: "+str(conn.conn.debug))
            elif cmd == "^nazi":
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
