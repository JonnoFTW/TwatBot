#Twatbot Plugins
import plugins.dragon
import plugins.ban
import plugins.help
import plugins.chans
import plugins.joinpart
import plugins.tweet
import plugins.quit
import plugins.scroll
from heapq import merge
import traceback
import sys

def parse(conn):
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    print (conn.dataN['fool']+' '+conn.dataN['chan']+': '+conn.dataN['msg'])
    if conn.dataN['cmd'] == 'KICK' and nick in conn.dataN['raw']:
        del (conn.chans[conn.dataN['chan']]) 
    if conn.dataN['cmd'] == 'PRIVMSG' and len(conn.dataN['words']) != 0:
        # Run the function for the given command            
        if conn.dataN['fool'] in conn.admins:
            check(list(merge(pluginList, adminPlugins)),conn)
        else:
            check(pluginList,conn)

def check(pl,conn):
    for plugin in pl:
        if conn.dataN['words'][0] in plugin.triggers:
            try:
                plugin.triggers[conn.dataN['words'][0]](conn)
            except Exception, err:
                conn.sendMsg("Plugin failed: " + plugin.__name__ + ': '+ str(err) ,conn.dataN['chan'])
            return

pluginList = [
    plugins.ban,
    plugins.chans,
    plugins.dragon,
    plugins.help,
    plugins.scroll,
    plugins.tweet
]
adminPlugins = [
    plugins.joinpart,
    plugins.ban,
    plugins.quit
]
