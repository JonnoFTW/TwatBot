#Twatbot Plugins
from plugins import *
from heapq import merge
import traceback
import sys
from threading import Thread

        
def parse(conn):
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    print (conn.dataN['fool']+' '+conn.server+'/'+conn.dataN['chan']+': '+conn.dataN['msg'])
    if conn.dataN['msg'] == "\001VERSION\001":
        conn.sendNotice('VERSION Twatbot, the tweeting bot 1.2',conn.dataN['fool'])
    if conn.dataN['msg'] == "\001PING\001":
        conn.sendNotice('PONG',conn.dataN['fool'])
    if conn.dataN['fool'] in conn.tells:
        conn.sendNot(conn.dataN['fool']+": You have unread messages! Type ^read to read them")
        conn.tells.remove(conn.dataN['fool'])
    if conn.dataN['cmd'] == 'KICK' and conn.nick in conn.dataN['raw']:
        try:
            del (conn.chans[conn.dataN['chan']]) 
        except Exception,e:
            print "Failed to remove; %s" % (str(e)) 
#    if conn.dataN['cmd'] == 'JOIN' and len(conn.dataN['fool']) > 15:
#        conn.sendMsg(".k "+conn.dataN['fool']+' We have a strict no long nick (15 chars) policy here')
    if conn.dataN['cmd'] == 'PRIVMSG' and len(conn.dataN['words']) != 0:
        if conn.dataN['words'][0] == '^cmds':
           trigs = []
           for i in list(merge(pluginList, adminPlugins)):
               trigs.append(i.triggers.keys())
           conn.sendNot(str(trigs))
           return
        # Run the function for the given command
        if conn.dataN['fool'] in conn.admins:
            if conn.dataN['words'][0] == '^reload':
                try:
                    g = dict(globals())
                    for i in g:
                      if conn.dataN['words'][1] == i:
                          reload(globals()[conn.dataN['words'][1]])
                          conn.sendMsg("Module reloaded")
                except Exception, e:
                    conn.sendMsg(str(e))
            check(list(merge(pluginList, adminPlugins)),conn)
        elif conn.dataN['fool'] not in conn.banned:
            check(pluginList,conn)

class PluginRunner(Thread):
    def __init__(self,conn,plugin):
        self.conn = conn
        self.chan = conn.dataN['chan']
        self.plugin = plugin
        Thread.__init__(self)
    def run(self):
        try:
            self.plugin.triggers[self.conn.dataN['words'][0]](self.conn)
        except Exception, err:
            print >> sys.stderr, str(err)
            self.conn.sendMsg("Plugin failed: " + self.plugin.__name__ + ': '+ str(err) ,self.chan)
        
def check(pl,conn):
    for plugin in pl:
        if conn.dataN['fool'] not in (conn.ignores+conn.banned) and conn.dataN['words'][0] in plugin.triggers:
            if conn.dataN['msg'].find('help') != -1:
                try:
                    conn.sendNot(plugin.help)
                    return
                except: 
                    conn.sendNot("No help available")
		    return
            else:
                p = PluginRunner(conn,plugin)
                p.start()                   
                return
            


pluginList = [
    web,
    stat,
    amigo,
    ban,
    chans,
    dragon,
    help,
    tell,
    scroll,
    tweet,
    checkem,
    markov,
#    laughter,
    fullwidth
]
adminPlugins = [
    joinpart,
    ban,
    quit
]
