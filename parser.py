#Twatbot Plugins
#import plugins.tell
import plugins.amigo
import plugins.dragon
import plugins.ban
import plugins.help
import plugins.chans
import plugins.joinpart
import plugins.tweet
import plugins.quit
import plugins.scroll
import plugins.checkem
import plugins.markov
import plugins.markovgenpy
#import plugins.laughter
import plugins.fullwidth
from heapq import merge
import traceback
import sys

def parse(conn):
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    print (conn.dataN['fool']+' '+conn.dataN['chan']+': '+conn.dataN['msg'])
    if conn.dataN['msg'] == "\001VERSION\001":
        conn.sendNotice('VERSION Twatbot, the tweeting bot 1.2',conn.dataN['fool'])
    if conn.dataN['msg'] == "\001PING\001":
        conn.sendNotice('PONG',conn.dataN['fool'])
    if conn.dataN['cmd'] == 'KICK' and conn.nick in conn.dataN['raw']:
        try:
            del (conn.chans[conn.dataN['chan']]) 
        except Exception,e:
            print "Failed to remove; %s" % (str(e)) 
    if conn.dataN['cmd'] == 'PRIVMSG' and len(conn.dataN['words']) != 0:
        if conn.dataN['words'][0] == '^cmds':
           trigs = []
           for i in list(merge(pluginList, adminPlugins)):
               trigs.append(i.triggers.keys())
           conn.sendNot(str(trigs))
           return
        # Run the function for the given command
        if conn.dataN['fool'] in conn.admins:
            check(list(merge(pluginList, adminPlugins)),conn)
        elif conn.dataN['fool'] not in conn.banned:
            check(pluginList,conn)

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
                try:
                    plugin.triggers[conn.dataN['words'][0]](conn)
                    return
                except Exception, err:
                    print >> sys.stderr, str(err)
                    conn.sendMsg("Plugin failed: " + plugin.__name__ + ': '+ str(err) ,conn.dataN['chan'])

pluginList = [
    plugins.amigo,
    plugins.ban,
    plugins.chans,
    plugins.dragon,
    plugins.help,
 #   plugins.tell,
    plugins.scroll,
    plugins.tweet,
    plugins.checkem,
    plugins.markov,
#    plugins.laughter,
    plugins.fullwidth
]
adminPlugins = [
    plugins.joinpart,
    plugins.ban,
    plugins.quit
]
