def joinpart(dataN):
    jp = dataN['words'][0]
    if len(dataN['words']) > 1:
        chan = dataN['words'][1]
        if chan[0] != '#':
            sendMsg('Please format the channel properly',dataN['chan'])
        if jp == '^part':    
            if chan not in (chans.keys()):
                sendMsg('I\'m not in that channel',dataN['chan'])
            else:
                del chans[chan]
                chanOP(chan,'PART')
        if jp == '^quit':
            if chan in (chans.keys()):
                sendMsg('I\'m already in that channel',dataN['chan'])
            else:
                chans[chan] = ''
                chanOP(chan,'JOIN')  
    else:  
        sendMsg('Please provide a channel to '.jp,dataN['chan'])



