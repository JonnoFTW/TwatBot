def tweet(dataN):
    if dataN['fool'] not in banned:
        if (''.join(chans[dataN['chan']].split())) != "":
            if dataN['fool'] == chans[dataN['chan']].split(':')[0]:
                sendMsg("Can't quote yourself",dataN['chan'])
            else:
                toSend = (chans[dataN['chan']].pop())[:140]
                print(toSend)
                setTwit(toSend,dataN['chan'])
                spaces = ' '*(random.randint(1,5))  
                sendMsg('Sending to twitter!'+spaces,dataN['chan']) 
def getTwit(user):
    try:
        result = api.GetUserTimeline(user)[0].text
    except:
        result = 'Could not get twitter'
    return result

def setTwit(msg,chan):
    try:
        result = api.PostUpdate(msg)
    except:
        sendMsg( 'Could not update twitter',chan)
 
