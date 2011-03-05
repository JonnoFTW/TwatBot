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

network = 'localhost'
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
    ircCom('PRIVMSG '+chan,':'+msg.rstrip('\r\n'))

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
        ircCom(chan,'JOIN')
        chans[chan] = deque([],10)
        #retrieve the last messge from the server, check if
        #success error code or not, throw error on not
        out = "Successfully joined"
    except:
        out = "Could not join channel"
    return out
               
admins = ['Jonno_FTW','Garfunkel']
global banned
banned = getFile('banned')
global chans
chans = {'#galaxy':''}

connect()
while True:
    try:
        dataN = irc.recv(4096)# .decode('utf-8','ignore')
    except:
        connect()
    parser.parse(dataN)
    if dataN.split()[1] == 'PRIVMSG' :
    #Store the last 10 messages in an array
        dataN = line(dataN)
        #if len(dataN['msg'].split()) != 0:
        try:
            if dataN['msg'].split()[0][0] != '^':
                chans[dataN['chan']].append(dataN['fool']+': '+dataN['msg'])
        except (IndexError):
            pass

