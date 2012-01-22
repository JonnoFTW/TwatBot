#!/usr/bin/python2.7
# coding=utf-8
import socket
import os
import sys, traceback
import gc

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

pid = str(os.getpid())
pidfile = "/tmp/twatbot.pid"

if os.path.isfile(pidfile):
    try:
        os.kill(int(file(pidfile).read()), 0)
        print "%s already exists, exiting" % pidfile
        sys.exit()
    except OSError:
        pass
else:
    file(pidfile, 'w').write(pid)

import random
import twitter
import time
import plugins.markov
import plugins.tell
from collections import deque
import parser
import datetime
import SocketServer
from threading import Thread,Lock

def getFile(x):
    with open(x) as f:
        result = f.readlines()
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

servers = [
 {'server': 'irc.rizon.net',
  'channels':['#perwl','#futaba']
  }
 ]



class GitHandler(SocketServer.StreamRequestHandler):
    def handle(self):
      try:
        print "Incoming on socket: "+str(self.client_address)
        if self.client_address[0] not in ['127.0.0.1', '192.168.2.1','192.168.1.133']:
            return

        data = self.request.recv(1024).strip().replace('\n','')
        words = data.split()
        if(words[0][0] == '#'):
          try:
            connections[0].conn.sendMsg(' '.join(words[1:]),words[0])
          except:
            pass
        else:
            connections[0].conn.sendMsg(data,"#perwl")    
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


listener = GitServ()
listener.start()
log = open('text.log','a+')
logLock = Lock()

class WhoThread(Thread):
    def __init__(self,conn):
        self.conn = conn
        Thread.__init__(self)
    def run(self):
        for i in self.conn.chans:
            self.conn.ircCom('WHO',i)

class Connection:
    """A class to hold the connection to the server
    and related information"""
    def __init__(self,server,channels,port = 6667,nick='TwatBot'):
        self.quitting = False
        self.printAll = False
        self.server = server.lower()
        self.port = port
        self.nick = nick
        self.api = api
        self.steamKey = keys[5]
        self.srvthread = listener
        db = plugins.tell.getDB()
        cu = db.cursor()
        cu.execute("SELECT `to` FROM tell")
        s = cu.fetchall()
        self.tells = set()
        for i in s:
            self.tells.add(i[0])
        print self.tells
        cu.close()
        db.close()
        self.admins = ['Jonno_FTW','Garfunkel',"Garfunk"]
        self.nazi = False
        self.chans = dict()
        for i in channels:
            self.chans[i] = None
        #Mapping of channel to list of users
        self.users = dict()
        self.playing = False
        self.banned = getFile('banned')
        self.ignores = getFile('ignore')
        self.irc = self.connect()
        self.uptime = datetime.datetime.now()
        self.who = WhoThread(self)
        self.who.start()
        
        
    def ircCom(self,command,msg):
      try:
        tosend = (unicode(' '.join(msg.splitlines())) + '\r\n').encode('utf-8','replace')

        
        chunks = []
        if command[-1] != ":":
            command = command+' '
        tosend = tosend.lstrip()
        while tosend:
            chunks.append(command+(tosend[:510-len(command)]))
            tosend = tosend[510-len(command):]
        for i in chunks:
            result = self.irc.send(i)
            time.sleep(1)
            if result == 0:
                print 'Send timeout'
            else:
                print i.rstrip()
      except socket.timeout, e :
        print str(e)
        self.decon()
        time.sleep(10)
        self.connect()
            
    def sendNotice(self,msg,fool):
        self.ircCom('NOTICE '+fool+':',"\001"+msg+"\001")
        
    def sendMsg(self,msg,chan = None):
        if chan == None: chan = self.dataN['chan']
        self.ircCom('PRIVMSG '+chan+' :',msg)
        
    def sendNot(self,msg):
        self.ircCom('NOTICE '+self.dataN['fool']+ ' :',msg.rstrip('\r\n'))
 
    def connect(self): 
     self.errs = 0
     while True:
      try:
        self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.irc.settimeout(300)
        print "Connecting to %s:%d" % (self.server,self.port)
        self.irc.connect ((self.server,self.port))
      except Exception, e:
        print str(e)
        time.sleep(10)
        continue
      finally:
        self.ircCom ('NICK',self.nick)
        self.ircCom ('USER',self.nick + ' x * :Segwinton Buttsworthy')
        self.sendMsg('identify '+keys[4],'nickserv')
        time.sleep(4)
        for i in self.chans.keys():
            self.joinChan(i)
        return self.irc

    def chanOP(self,chan,op):
        self.ircCom (op,chan)
    def decon(self):
      try:
        self.irc.close()
      except Exception, e:
        print str(e)
    def close(self): 
        self.ircCom('QUIT',":I don't quit, I wait")
        time.sleep(2)
        print ('Exiting')
        self.decon()
        try:
            listener.stop()
            logLock.acquire()
            log.close()
            logLock.release()
            os.unlink(pidfile)
        except:
            pass
        sys.exit(0)
        
    def joinChan(self,chan):
        self.ircCom('JOIN',chan)
        self.chans[chan] = deque([],10)
        self.users[chan] = set()
        self.ircCom('WHO',chan)

    def setMarkov(self,obj):
        self.markov = obj


def line(data):
    raw = data
    try:
        if data.split()[0] == "ERROR":
            return None
        
        data = data.rstrip('\r\n').split()
        fool = data[0].split('!')[0][1:]
        cmd  = data[1]
        if cmd == 'QUIT':
            chan = ''
            msg = ' '.join(data[2:])
        else:
            chan = data[2].replace(':','')
            msg  = ' '.join(data[3:])[1:]
    except Exception, e:
        print  ("An error occurred when parsing: "+raw)
        print >> sys.stderr, str(e)
        return None
    
    dic = {
        'fool':fool,
        'msg':msg,
        'cmd':cmd,
        'chan':chan,
        'words':msg.split(),
        'raw':raw
        }
    return dic
    
class ConnectionServer(Thread):
  def __init__(self,server,channels,port = 6667,nick = 'TwatBot'):
      Thread.__init__(self)
      self.m = 1
      for i in connections:
        if i.conn.server == server:
          self.m = 0
          break
      if self.m != 0:
        self.conn = Connection(server,channels,port,nick)
  def run(self):
    while True:
        gc.collect()
        try:
            dataN = self.conn.irc.recv(4096)# .decode('utf-8','ignore')
            if self.conn.printAll:
                print dataN
        except socket.timeout, e:
            print str(e)
            self.conn.decon()
            time.sleep(2)
            self.conn.irc = self.conn.connect()
        except KeyboardInterrupt:
            self.conn.close()
            break
        for i in dataN.splitlines():
          try:
              if i.split()[0] == 'PING':
                self.conn.ircCom('PONG', i.split(':')[1])
                continue
          except IndexError:
            return
          except Exception, e:
            if self.conn.quitting:
                os.unlink(pidfile)
                listener.stop()
                sys.exit(0)
            print >> sys.stderr, str(e)
            self.conn.decon()
            time.sleep(2)
            self.conn.irc = self.conn.connect()
            continue
          self.conn.dataN = line(i)
          if not self.conn.dataN: continue
          parser.parse(self.conn)
          if "Ping timeout" in i and self.conn.nick in i and "ERROR" in i:
            self.conn.decon()
            time.sleep(5)
            self.conn.connect()
            break
          if self.conn.dataN['cmd'] == 'PRIVMSG' and self.conn.dataN['chan'] in self.conn.chans.keys() or self.conn.dataN['chan'] == self.conn.nick:
            try:
                if self.conn.dataN['fool'] in self.conn.admins:
                  try:
                    if len(self.conn.dataN['words']) > 0 and self.conn.dataN['words'][0] == '^connect':
                      connections.append(ConnectionServer(self.conn.dataN['words'][1],[self.conn.dataN['words'][2]],nick='Tw4tb0t'))
                      if connections[-1].m == 1:
                        self.conn.sendMsg("Successfully connected")
                        connections[-1].start()
                      else:
                        self.conn.sendMsg("A connection to that server already exists!")
                  except IndexError,e :
                    self.conn.sendMsg("Usage is: ^connect server channel")
                if self.conn.dataN['words'][0][0] != '^':
                    if self.conn.dataN['msg'].find('http') == -1 and self.conn.dataN['msg'].count('.') < 8:
                      try:
                        logLock.acquire()
                        log.write(self.conn.dataN['msg']+'\n')
                        logLock.release()
                      except Exception, e:
                        print e
                    if self.conn.dataN['chan'] != self.conn.nick and self.conn.dataN['fool'] not in self.conn.ignores: self.conn.chans[self.conn.dataN['chan']].append(self.conn.dataN['fool']+': '+self.conn.dataN['msg'])
            except IndexError:
                pass
            
connections = []
for i in servers:
    connections.append(ConnectionServer(i['server'],i['channels']))
for i in connections:
    i.start()                

