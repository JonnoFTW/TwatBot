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

def parse(dataN):
        print (dataN['fool']+' '+dataN['chan']+': '+dataN['msg'])
        if dataN['cmd'] == 'KICK' and nick in dataN['raw']:
            del (chans[dataN['chan']]) 
        if dataN['cmd'] == 'PRIVMSG' and len(dataN['words']) != 0:
            # Run the function for the given command
                dataN = check(list(merge(pluginList, adminPlugins)),dataN)
            if dataN['fool'] in dataN['admins']:
            else:
                dataN = check(pluginList,dataN)
            return dataN

def check(pl,data):
    for plugin in pl:
        if data['words'][0] in plugin.triggers:
            try:
                out = plugin.triggers(data)
            except:
                sendMsg("Plugin failed: " + (plugin.__name__) ,data['chan'])
            return out

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
