#!/usr/bin/python
import socket
import sys
import random
import twitter
import time
from collections import deque

import parser

def getFile(x):
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

def ircCom(command,msg):
    tosend = (command +' ' + msg + '\r\n').encode('utf-8','replace')
    result = irc.send (tosend)
    if result == 0:
        print('Send timeout')
    else:
        print (tosend[:-2])

def sendMsg(msg,chan):
    ircCom('PRIVMSG '+chan,':'+msg.rstrip('\r\n'))

def connect():
    global irc
    irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    irc.connect ((network,port))
    ircCom ('NICK',nick)
    ircCom ('USER',nick+ ' 0 * :Miscellaneous Bot')
    sendMsg('identify '+keys[4],'nickserv')
    time.sleep(4)
    for i in chans.keys():
        joinChan(i)

def chanOP(chan,op):
    ircCom (op,chan)

def close():
    ircCom('QUIT',':'+nick+' away!')
    print ('Exiting')
    irc.shutdown(1)
    irc.close()
    sys.exit(0)

def joinChan(chan):
    try:
        ircCom('JOIN',chan)
        chans[chan] = deque([],10)
        #retrieve the last messge from the server, check if
        #success error code or not, throw error on not
        out = "Successfully joined"
    except:
        out = "Could not join channel"
    return out

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
         
admins = ['Jonno_FTW','Garfunkel']
chans = {'#perwl':''}
playing = False
connect()

while True:
    try:
        dataN = irc.recv(4096)# .decode('utf-8','ignore')
    except:
        connect()
    dataN = line(dataN)
    try:
        dataN['admins'] = newState['admins']
        dataN['chans']  = newState['chans']
        dataN['playing'] = newState['playing']
        print "got here"
    except (NameError,TypeError):
        dataN['admins'] = admins
        dataN['chans']  = chans
        dataN['playing'] = playing
    
    if dataN['raw'][0] == 'PING':
        ircCom('PONG', dataN.split()[1][1:])
    else:
        newState = parser.parse(dataN)
    if dataN['cmd'] == 'PRIVMSG':
        if dataN['words'][0] != '^':
            chans[dataN['chan']].append(dataN['fool']+': '+dataN['msg'])


