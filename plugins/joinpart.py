def joinpart(dataN):
    jp = dataN['words'][0]
    if len(dataN['words']) > 1:
        chan = dataN['words'][1]
        if chan[0] != '#':
            sendMsg('Please format the channel properly',dataN['chan'])
        elif jp == '^part':    
            if chan not in (chans.keys()):
                sendMsg('I\'m not in that channel',dataN['chan'])
            else:
                del chans[chan]
                chanOP(chan,'PART')
        elif jp == '^quit':
            if chan in (chans.keys()):
                sendMsg('I\'m already in that channel',dataN['chan'])
            else:
                sendMsg(joinChan(chan),dataN['chan'])
    else:  
        sendMsg('Please provide a channel to '.jp,dataN['chan'])


triggers = {'^join':joinpart,'^part':joinpart}
