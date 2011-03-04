def last(data):
    if len(data['words']) > 1:
        sendMsg(getTwit(data['words'][1]),dataN['chan'])
    else:
        sendMsg(getTwit('Buttsworth_'),dataN['chan'])
