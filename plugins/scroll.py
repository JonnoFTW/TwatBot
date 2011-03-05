triggers = {'^scroll':scroll}
def scroll(data):
    if len(data['words']) > 1:
        try:
            sendMsg("Scroll at: ".chans[data['chan']][-int(data['words'][1])],data['chan'])
        except:
            sendMsg("Perhaps if you used a number",dataN['chan'])
    else
        sendMsg(str(chans.list()),dataN['chan'])
