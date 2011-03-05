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
                check(dict(plugins,**adminPlugins),dataN) #adminOpts[words[0]](dataN)
            else:
                check(plugins,dataN) #options[words[0]](dataN)

def check(pl,data):
    for plugin in pl:
        if data['words'][0] in plugin.triggers:
            plugin.triggers(data)


plugins = [
    plugins.ban,
    plugins.chans,
    plugins.dragon,
    plugins.help,
    plugins.last,
    plugins.scroll,
    plugins.tweet
]
admingPlugins = [
    plugins.joinpart,
    plugins.ban,
    plugins.quit
]
## Be sure to add an option for each available function


