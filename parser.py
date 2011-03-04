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
                adminOpts[words[0]](dataN)
            else:
                options[words[0]](dataN)            
            elif words[0] == '^quit' and dataN['fool'] in admins:
                close()


options = {
    '^cmds':listcmds,
    '^^':post,
    '^last':getLast,
    '^help':help,
    '^play':play,
    '^chans':listChans,
    '^ban':ban,
    '^todo':todo
}
adminOpts = {
 '^quit':close,
 '^join':join,
 '^part':foo,
 '^ban':bar,
}

def listcmds(data):
    sendMsg(data,data['chan'])
## Be sure to add an option for each available function


