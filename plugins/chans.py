def chans(dataN):
    sendMsg('Currently in: '+(', '.join(chans.keys())),dataN['chan'])
    
triggers = {'^chans':chans}
