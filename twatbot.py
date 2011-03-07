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

class Connection:
    """A class to hold the connection to the server
    and related information"""
    def __init__(self):
        admins = ['Jonno_FTW','Garfunkel']
        chans = {'#perwl':None,'#futaba':None}
        playing = False
        banned = getFile('banned')
        irc = connect()
        
    def ircCom(self,command,msg):
        tosend = (command +' ' + msg + '\r\n').encode('utf-8','replace')
        result = irc.send (tosend)
        if result == 0:
            print('Send timeout')
        else:
            print (tosend[:-2])

    def sendMsg(self,msg,chan):
        self.ircCom('PRIVMSG '+chan,':'+msg.rstrip('\r\n'))

    def connect(self):
        self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        irc.connect ((network,port))
        self.ircCom ('NICK',nick)
        self.ircCom ('USER',nick+ ' 0 * :Miscellaneous Bot')
        self.sendMsg('identify '+keys[4],'nickserv')
        time.sleep(4)
        for i in chans.keys():
            self.joinChan(i)
        return irc

    def chanOP(self,chan,op):
        self.ircCom (op,chan)

    def close(self):
        self.ircCom('QUIT',':'+nick+' away!')
        print ('Exiting')
        irc.shutdown(1)
        irc.close()
        sys.exit(0)

    def joinChan(self,chan):
        try:
            self.ircCom('JOIN',chan)
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
    
conn = Connection()

while True:
    try:
        dataN = irc.recv(4096)# .decode('utf-8','ignore')
    except:
        conn.connect()
    conn.dataN = line(dataN)
    if conn.dataN['raw'][0] == 'PING':
        conn.ircCom('PONG', dataN.split()[1][1:])
    else:
        parser.parse(conn)
    if conn.dataN['cmd'] == 'PRIVMSG':
        if conn.dataN['words'][0] != '^':
            conn.chans[dataN['chan']].append(conn.dataN['fool']+': '+conn.dataN['msg'])


