#Twatbot Plugins
import plugins.dragon
import plugins.ban
import plugins.help
import plugins.chans
import plugins.joinpart
import plugins.tweet
import plugins.quit
import plugins.scroll
import plugins.checkem
from heapq import merge
import traceback
import sys

def parse(conn):
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    print (conn.dataN['fool']+' '+conn.dataN['chan']+': '+conn.dataN['msg'])
   # if conn.dataN['cmd'] == 'KICK' and conn.nick in conn.dataN['raw']:
   #     try:
   #         del (conn.chans[conn.dataN['chan']]) 
   #     except Exception,e:
   #         print "Failed to remove; %s" % (str(e)) 
    if conn.dataN['cmd'] == 'PRIVMSG' and len(conn.dataN['words']) != 0:
        if conn.dataN['words'][0] == '^cmds':
           trigs = []
           for i in list(merge(pluginList, adminPlugins)):
               trigs.append(i.triggers.keys())
           conn.sendMsg(str(trigs),conn.dataN['chan'])
           return
        # Run the function for the given command
        if conn.dataN['fool'] in conn.admins:
            check(list(merge(pluginList, adminPlugins)),conn)
        elif conn.dataN['fool'] not in conn.banned:
            check(pluginList,conn)

def check(pl,conn):
    for plugin in pl:
        if conn.dataN['words'][0] in plugin.triggers:
            if conn.dataN['msg'].find('help') != -1:
                try:
                    conn.sendMsg(plugin.help,conn.dataN['chan'])
                    return
                except: 
                    conn.sendMsg("No help available",conn.dataN['chan'])
		    return
            else:            
                try:
                    plugin.triggers[conn.dataN['words'][0]](conn)
                except Exception, err:
                    conn.sendMsg("Plugin failed: " + plugin.__name__ + ': '+ str(err) ,conn.dataN['chan'])

pluginList = [
    plugins.ban,
    plugins.chans,
    plugins.dragon,
    plugins.help,
    plugins.scroll,
    plugins.tweet,
    plugins.checkem
]
adminPlugins = [
    plugins.joinpart,
    plugins.ban,
    plugins.quit
]
