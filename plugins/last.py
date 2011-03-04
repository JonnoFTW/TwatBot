def last(data):
    if len(words) > 1:
        sendMsg(getTwit(words[1]),dataN['chan'])
    else:
        sendMsg(getTwit('Buttsworth_'),dataN['chan'])
