def banned(dataN):
    if len(dataN['words']) > 1 and dataN['fool'] in admins:
        ban(words[1])
        banned.append(dataN['words'][1])
        toSend = dataN['words'][1]+' is now banned from tweeting'
        sendMsg(toSend,dataN['chan'])
        setTwit(toSend)
    else:
        sendMsg('Current bans are: '+(', '.join(banned)),dataN['chan'])

def ban(nick):
    global banned
    f = open('banned','a')
    f.write(nick+'\n')
    f.close()
    return True
