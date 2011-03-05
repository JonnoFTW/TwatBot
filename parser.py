#Twatbot specific

import plugins.dragon
import plugins.ban
import plugins.help
import plugins.chans
import plugins.joinpart
import plugins.tweet
import plugins.quit
import plugins.scroll

def line(data):
    data = data.rstrip('\r\n')
    msg  = ''.join(data.split(':',2)[2:])
    words= msg.split()
    data = data.split()
    fool = data[0].split('!')[0][1:]
    cmd  = data[1]
    chan = data[2]
    dic = {
        'fool':fool,
        'msg':msg,
        'cmd':cmd,
        'chan':chan,
        'words':words,
        'raw':data
        }
    return dic

def parse(dataN):
        global banned
        global playing
        global chans
        if dataN.split()[0] == 'PING':
            ircCom('PONG', dataN.split()[1][1:]) 
            return
        dataN = line(dataN)
        print (dataN['fool']+' '+dataN['chan']+': '+dataN['msg'])
        if dataN['cmd'] == 'KICK' and nick in dataN['raw']:
            del (chans[dataN['chan']]) 
        if dataN['cmd'] == 'PRIVMSG' and len(words) != 0:
            # Run the function for the given command
            if dataN['fool'] in admins:
                check(dict(pluginList,**adminPlugins),dataN)
            else:
                check(pluginList,dataN)

def check(pl,data):
    for plugin in pl:
        if data['words'][0] in plugin.triggers:
            try:
                plugin.triggers(data)
            except:
                sendMsg("Plugin failed: " + (plugin.__name__) ,data['chan'])

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
