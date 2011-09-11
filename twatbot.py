#!/usr/bin/python2.7
import socket
import sys
import random
import twitter
import time
import plugins.markov
from collections import deque
import parser
import datetime
import SocketServer
from threading import Thread

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
#network = '65.23.158.132'
port = 6667
nick = 'TwatBot'

class GitHandler(SocketServer.StreamRequestHandler):
    def handle(self):
      try:
        if self.client_address[0] != '127.0.0.1':
            return
        self.data = self.request.recv(1024).strip().replace('\n','')
        conn.sendMsg(self.data,"#perwl")    
      except Exception, e:
        print >> sys.stderr, str(e)
class GitServ(Thread): #SocketServer.ThreadingMixIn,SocketServer.TCPServer):
   def __init__(self):
     try:
        self.server = SocketServer.TCPServer(("localhost",6666),GitHandler)
        #self.server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        Thread.__init__(self)
     except Exception, e:
        print >> sys.stderr, str(e)
   def run(self):
        self.server.serve_forever()
   def stop(self):
        self.server.shutdown()
        #self.server.close()

class Connection:
    """A class to hold the connection to the server
    and related information"""
    def __init__(self):
        self.api = api
        self.admins = ['Jonno_FTW','Garfunkel']
        self.chans = {'#perwl':None,'#futaba':None}
        self.playing = False
        self.banned = getFile('banned')
        self.ignores = getFile('ignore')
        self.irc = self.connect()
        self.nick = nick
        self.log = open('text.log','a+')
        self.uptime = datetime.datetime.now()
#        self.srvthread = GitServ()
#        self.srvthread.start()
        
    def ircCom(self,command,msg):
      try:
        tosend = (command +' ' + msg.replace('\n',"") + '\r\n').encode('utf-8','replace')
        result = self.irc.send (tosend)
        if result == 0:
            print('Send timeout')
        else:
            print (tosend[:-2])
      except:
        self.errs+= 1
        if (self.errs >=  3):
          self.decon()
          self.connect()
        print "Sending error"
            
    def sendNotice(self,msg,fool):
        self.ircCom('NOTICE '+fool,":\001"+msg+"\001")
        
    def sendMsg(self,msg,chan = None):
        if chan == None: chan = self.dataN['chan']
        self.ircCom('PRIVMSG '+chan,':'+msg.rstrip('\r\n'))
    def sendNot(self,msg):
        self.ircCom('NOTICE '+self.dataN['fool'],':'+msg.rstrip('\r\n'))
 
    def connect(self):
     self.errs = 0
     while True:
      try:
        self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.irc.settimeout(300)
        self.irc.connect ((network,port))
      except:
        time.sleep(10)
        continue
      finally:
        self.ircCom ('NICK',nick)
        self.ircCom ('USER',nick+ ' x * :Segwinton Buttsworthy')
        self.sendMsg('identify '+keys[4],'nickserv')
        time.sleep(4)
        for i in self.chans.keys():
            self.joinChan(i)
        return self.irc

    def chanOP(self,chan,op):
        self.ircCom (op,chan)
    def decon(self):
      try:
        self.irc.shutdown(1)
        self.irc.close()
      except Exception, e:
        print str(e)
    def close(self):
        self.ircCom('QUIT',":I don't quit, I wait")
        time.sleep(2)
        print ('Exiting')
        self.decon()
        self.log.close()
 #       self.srvthread.stop()        
        sys.exit(1)

    def joinChan(self,chan):
        self.ircCom('JOIN',chan)
        self.chans[chan] = deque([],10)
        
    def getTwit(self,user):
        try:
            result = self.api.GetUserTimeline(user)[0].text
        except:
            result = 'Could not get twitter'
        return result

    def setTwit(self,msg,chan):
        try:
            result = self.api.PostUpdate(msg)
            return result
        except:
            self.sendMsg( 'Could not update twitter',chan)
    def setMarkov(self,obj):
        self.markov = obj


def line(data):
    verbose = open('verbose.log','a')
    verbose.write(data)
    verbose.close()
    data = data.rstrip('\r\n')
    try:
        p    = data[data.find('@'):].split()
        msg  = ' '.join(p[3:])[1:]
        cmd  = p[1]
        chan = p[2]
        data = data.split()
    except: #horrible
        try:
          msg  = ''.join(data.split(':',2)[2:])
          data = data.split()
          cmd  = data[1]
          chan = data[2]
        except:
          return False
    fool = data[0].split('!')[0][1:]
    words= msg.split()
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
        dataN = conn.irc.recv(4096)# .decode('utf-8','ignore')
        if dataN.split()[0] == 'PING':
            conn.ircCom('PONG', dataN.split()[1][1:])
            continue
    except KeyboardInterrupt:
        conn.close()
    except Exception, e:
        print >> sys.stderr, str(e)
        conn.decon()
        conn = Connection()
        continue
    conn.dataN = line(dataN)
    if not conn.dataN: continue
    parser.parse(conn)
    if conn.dataN['cmd'] == 'PRIVMSG' and conn.dataN['chan'] in conn.chans.keys() or conn.dataN['chan'] == nick:
        try:
            if conn.dataN['words'][0][0] != '^':
                if conn.dataN['msg'].find('http') == -1 and conn.dataN['msg'].count('.') < 8:
                    conn.log.write(conn.dataN['msg']+'\n')
                if conn.dataN['chan'] != nick and conn.dataN['fool'] not in conn.ignores: conn.chans[conn.dataN['chan']].append(conn.dataN['fool']+': '+conn.dataN['msg'])
        except IndexError:
            pass


