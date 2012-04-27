#Twatbot Plugins
from plugins import *
from heapq import merge
import traceback
import sys, os
from threading import Thread
import MySQLdb
import MySQLdb.cursors
from urllib2 import URLError
        
def parse(conn):
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
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
    #everything else is passed to the default plugin
            
    p = PluginRunner(conn,default)
    p.start()
    
class ircState:
    def __init__(self,conn):
        self.conn = conn
        self.banned = conn.banned
        self.api = conn.api
        self.tells = conn.tells
        self.ignores = conn.ignores
        self.uptime = conn.uptime
        self.chans = conn.chans
        self.dataN = dict(conn.dataN)
        self.server = conn.server
    def sendNotice(self,msg,fool):
        self.conn.sendNotice(msg,fool)
    def sendMsg(self,msg,chan = None):
        if chan == None:
            chan = self.dataN['chan']
        self.conn.sendMsg(msg,chan)
    def sendNot(self,msg):
        self.conn.sendNot(msg)
    def decon(self):
        self.conn.decon()
    def joinChan(self,chan):
        self.conn.joinChan(chan)
    def close(self):
        self.conn.close()
    def setName(self,field):   
        return names.setName(self.conn,field)
    def getName(self,field):
        return names.getName(self.conn,field)
class PluginRunner(Thread):
    def __init__(self,conn,plugin):
        self.conn = ircState(conn)
        self.plugin = plugin
        Thread.__init__(self)
    def run(self):
        try:
           # print (self.conn.dataN['fool']+' '+self.conn.server+'/'+self.conn.dataN['chan']+': '+self.conn.dataN['msg'])
            if self.plugin == default:
                self.plugin.default(self.conn)
            elif self.conn.dataN['fool'] in (self.conn.ignores + self.conn.banned):
                return
            else:
                self.plugin.triggers[self.conn.dataN['words'][0]](self.conn)
        except URLError, err :
            conn.sendMsg("Plugin failed"+ self.plugin.__name__ + ': '+str(err))
        except Exception, err:
            print >> sys.stderr, str(err)
           # exc_type, exc_obj, exc_tb = sys.exc_info()
           # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
           # self.conn.sendMsg("Plugin failed: " + self.plugin.__name__ + ': '+type(err).__name__+" "+(' '.join([str(fname), str(exc_tb.tb_lineno)]))+": "+ str(err) ,self.conn.dataN['chan'])
            fln = traceback.format_exc().splitlines()
          #  print fln
            debugMsg = "Plugin failed: " + self.plugin.__name__ + ': '+type(err).__name__+" "+str(err)+(' '.join(fln[3:5]))
            if self.conn.conn.debug:
                self.conn.sendMsg(debugMsg)
            else:
                self.conn.sendMsg(debugMsg,self.conn.conn.admins[0])
        
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
    mueval,
    amigo,
    ban,
    chans,
    dragon,
    help,
    tell,
    scroll,
    tweet,
    checkem,
#    markov,
    lastfm,
#    laughter,
    fullwidth,
    counterstrike,
    steam
]
adminPlugins = [
    joinpart,
    ban,
    quit
]
