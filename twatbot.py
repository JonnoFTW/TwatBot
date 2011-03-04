#!/usr/bin/python
import socket
import sys
import random
import twitter
import time

def getFile(x)
    f = open(x,'r')
    result = f.readlines()
    f.close()
    result = map(lambda x: x.rstrip('\n'),result)
    return result
keys = getFile('keys')

api = twitter.Api(
    keys[0],
    keys[1],
    keys[2],
    keys[3]
    )

print (api.VerifyCredentials())

network = 'irc.rizon.net'
port = 6667
nick = 'TwatBot'
global irc
global playing
def ircCom(command,msg):
    global irc
    tosend = (command +' ' + msg + '\r\n').encode('utf-8','replace')
    result = irc.send (tosend)
    if result == 0:
        print('Send timeout')
    else:
        print (tosend[:-2])
def sendMsg(msg,chan):
    ircCom('PRIVMSG '+chan,':'+msg)
def connect():
    global irc
    global playing
    irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    irc.connect ((network,port))
    ircCom ('NICK',nick)
    ircCom ('USER',nick+ ' 0 * :Miscellaneous Bot')
    playing = False
    sendMsg('identify '+keys[4],'nickserv')
    time.sleep(4)
    for i in chans.keys():
        joinChan(i)
def joinChan(chan):
    ircCom ('JOIN',chan)

def close():
    global irc
    ircCom('QUIT',':'+nick+' away!')
    print ('Exiting')
    irc.shutdown(1)
    irc.close()
    sys.exit(0)
        
def line(data):
    data = data.rstrip('\r\n')
    msg  = ''.join(data.split(':',2)[2:])
    data = data.split()
    fool = data[0].split('!')[0][1:]
    cmd  = data[1]
    chan = data[2]
    dic = {
        'fool':fool,
        'msg':msg,
        'cmd':cmd,
        'chan':chan,
        'raw':data
        }
    return dic
    
def play(chan,msg):
    global playing
    if msg.find("You have already played today") != -1 or msg.find("1... A dragon eats you.") != -1:
        playing = False 
    elif msg.find('Type !roll') != -1 or  msg.find('You are already playing') != -1:
        sendMsg('!roll',chan)
        
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
        
def ban(nick):
    global banned
    f = open('banned','a')
    f.write(nick+'\n')
    f.close()
    return True
        
def parse(dataN):
  #  try:
        global banned
        global playing
        global chans
        if dataN.split()[0] == 'PING':
            ircCom('PONG', dataN.split()[1][1:]) 
            return
        dataN = line(dataN)
        words = dataN['msg'].split()
        print (dataN['fool']+' '+dataN['chan']+': '+dataN['msg'])
        if dataN['cmd'] == 'KICK' and nick in dataN['raw']:
            del (chans[dataN['chan']]) 
        if dataN['cmd'] == 'PRIVMSG' and len(words) != 0:
            if words[0] == '^^' and dataN['fool'] not in banned:
                if (''.join(chans[dataN['chan']].split())) != "":
                    if dataN['fool'] == chans[dataN['chan']].split(':')[0]:
                        sendMsg("Can't quote yourself",dataN['chan'])
                    else:
                        toSend = chans[dataN['chan']][:140]
                        print(toSend)
                        setTwit(toSend,dataN['chan'])
                        spaces = ' '*(random.randint(1,5))  
                        sendMsg('Sending to twitter!'+spaces,dataN['chan']) 
            if words[0] == '^last':
                if len(words) > 1:
                    sendMsg(getTwit(words[1]),dataN['chan'])
                else:
                    sendMsg(getTwit('Buttsworth_'),dataN['chan'])
            elif words[0] == '^help':
                sendMsg('Send the the line preceeding ^^ to @Buttsworth_ on twitter. Most recent update with ^last. View channels with ^chans. http://twitter.com/#!/Buttsworth_',dataN['chan'])
            elif words[0] == '^quit' and dataN['fool'] in admins:
                close()
            elif words[0] == '^ban':
                if len(words) > 1 and dataN['fool'] in admins:
                    ban(words[1])
                    banned.append(words[1])
                    toSend = words[1]+' is now banned from tweeting'
                    sendMsg(toSend,dataN['chan'])
                    setTwit(toSend)
                else:
                    sendMsg('Current bans are: '+(', '.join(banned)),dataN['chan'])
            elif words[0] == '^part' and dataN['fool'] in admins:
                if len(words) > 1:
                    chan = words[1]
                    if chan not in (chans.keys()):
                        sendMsg('I\'m not in that channel',dataN['chan'])
                    elif chan[0] == '#':
                        del chans[chan]
                        ircCom('PART',chan)
                    else:
                        sendMsg('Please format the channel properly',dataN['chan'])
                else:  
                    sendMsg('Please provide a channel to leave',dataN['chan'])
            elif words[0] == '^join' and dataN['fool'] in admins: 
                if len(words) > 1:
                    chan = words[1]
                    if chan in (chans.keys()):
                        sendMsg('I\'m already in that channel',dataN['chan'])
                    elif chan[0] == '#':
                        chans[chan] = ''
                        joinChan(words[1])
                    else:
                        sendMsg('Please format the channel properly',dataN['chan'])
                else:
                    sendMsg('Please provide a channel to join',dataN['chan'])
            elif words[0] == '^chans':
                sendMsg('Currently in: '+(', '.join(chans.keys())),dataN['chan'])
            elif words[0] == '^play' or playing:
                if words[0] != '^play':
                    play(dataN['chan'],dataN['msg'])                    
                else:
                    sendMsg('!play',dataN['chan'])
	            playing = True
    # except :
        # pass

admins = ['Jonno_FTW','Garfunkel']
global banned
banned = getFile('banned')
global chans
chans = {'#futaba':'','#perwl':''}


connect()
while True:
    try:
        dataN = irc.recv(4096)# .decode('utf-8','ignore')
    except:
        connect()
    parse(dataN)
    if dataN.split()[1] == 'PRIVMSG' :
        dataN = line(dataN)
        #if len(dataN['msg'].split()) != 0:
        try:
            if dataN['msg'].split()[0][0] != '^':
                chans[dataN['chan']] = dataN['fool']+': '+dataN['msg']
        except (IndexError):
            pass

