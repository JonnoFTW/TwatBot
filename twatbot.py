#!/usr/bin/python2.7
# coding=utf-8
import socket
import os,signal
import sys, traceback
import gc
from Queue import Queue
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
    
import MySQLdb
import MySQLdb.cursors
import random
import twitter
import time
import plugins.markov
import plugins.tell
from collections import deque
import parser
import datetime
import SocketServer
from threading import Thread,Lock,Timer
import thread

def getFile(x):
    with open(x) as f:
        result = f.readlines()
        result = map(lambda x: x.rstrip('\n'),result)
        return result
keys = dict()

with open('keys') as f:
    for i in f.read().splitlines():
        j = i.split()
        keys[j[0]] = j[1]
        


#print (api.VerifyCredentials())

servers = [
 {'server': 'irc.rizon.net',
  'channels':["#perwl",'#futaba','#touhouradio'],
  'admins':["Garfunk",'Jonno_FTW','Garfunkel','Dionysus'],
  'nick': 'TwatBot',
  'messages':[]
  }
 ]



class GitHandler(SocketServer.BaseRequestHandler):
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
        

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
listener =  ThreadedTCPServer(("localhost",6666),GitHandler)
server_thread = Thread(target=listener.serve_forever)
server_thread.daemon = True
server_thread.start()
log = open('text.log','a+')
logLock = Lock()

api = twitter.Api(
    keys['consumer_key'],
    keys['consumer_secret'],
    keys['access_token_key'],
    keys['access_token_secret']
    )

def WhoThread(conn):
    print "Requesting users from channels on "+conn.server
    for i in conn.chans:
        conn.users[i].clear()
        conn.ircCom('WHO',i)
        time.sleep(30)
                
class DoublesThread():
    def __init__(self):
        self.count = 0
    def inc(self):
        self.count += random.randint(1,10)
        if self.count >= 10000:
            self.count = 0
dubObj = DoublesThread()            
dubs = Timer(1,dubObj.inc)
dubs.start()


class Connection:
    """A class to hold the connection to the server
    and related information"""
    def __init__(self,server,channels,port = 6667,nick='TwatBot',admins = [],messages = []):
        self.db = self.getDB()
        self.connections = connections
        self.msgQueue = Queue()
        self.disp = Thread(target=self.dispatcher)
        self.disp.start()
        self.dubs = dubObj
        self.quitting = False
        self.FATAL_ERROR = False
        self.printAll = False
        self.debug = False
        self.server = server.lower()
        self.port = port
        self.nick = nick
        self.api = api
        self.steamKey = keys['steam_api_key']
        cu = self.db.cursor()
        cu.execute("SELECT `to` FROM tell")
        s = cu.fetchall()
        self.tells = set()
        for i in s:
            self.tells.add(i[0])
        print self.tells
        self.admins = admins
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
        self.whoInit()
        self.keys = keys
        for i in messages:
            self.sendMsg(i['msg'],i['to'])
    
    def whoInit(self):
        self.who = Thread(target=WhoThread,args=(self,),name="WHO:"+self.server)
        self.who.start()
        
    def dispatcher(self):
        while True:
            try:
                item = self.msgQueue.get()
                result = self.irc.send(item)
                time.sleep(1)
                if result == 0:
                    raise RuntimeError("Failed to send")
                else:
                    print 'Sending on '+self.server+':',item.strip()
            except :
                if item[:4] == 'QUIT':
                    return
                #  print str(e)
                # Should kill the connection thread here
                self.FATAL_ERROR = True
                print "FATAL ERROR IN SENDING RESTARTING CONNECTION"
                self.decon()
                return
                #  time.sleep(10)
                #  self.connect()
            finally:
                self.msgQueue.task_done()
        
    def ircCom(self,command,msg):
        tosend = (unicode(' '.join(msg.splitlines())) + '\r\n').encode('utf-8','replace')
        chunks = []
        if command[-1] != ":":
            command = command+' '
        tosend = tosend.lstrip()
        while tosend:
            chunks.append(command+(tosend[:510-len(command)]))
            tosend = tosend[510-len(command):]
        for i in chunks:
            self.msgQueue.put(i)
            
    def sendNotice(self,msg,fool):
        self.ircCom('NOTICE '+fool+':',"\001"+msg+"\001")
        
    def sendMsg(self,msg,chan = None):
        if chan == None: chan = self.dataN['chan']
        self.ircCom('PRIVMSG '+chan+' :',msg)
        
    def sendNot(self,msg):
        self.ircCom('NOTICE '+self.dataN['fool']+ ' :',msg.rstrip('\r\n'))
 
    def connect(self): 
      try:
        print "Connecting to %s:%d" % (self.server,self.port)
        self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.irc.settimeout(300)
        self.irc.connect ((self.server,self.port))
        self.ircCom ('NICK',self.nick)
        self.ircCom ('USER',self.nick + ' x * :Segwinton Buttsworthy')
        self.sendMsg('identify '+keys['nickpass'],'nickserv')
        time.sleep(5)
        for i in self.chans.keys():
            self.joinChan(i)
        return self.irc
      except socket.error, e:
        self.irc.close() 
        print "-------------socket error---------"
        print str(e)
        return False
      except Exception, e:
        self.irc.close()
        print "general exception found"
        print str(e)
        return False

    def decon(self):
      try:
        self.irc.close()
        self.disp.cancel()
      except Exception, e:
        print str(e)
    def close(self): 
        try:
            self.ircCom("QUIT",":I don't quit, I wait")
            self.quitting = True
            time.sleep(2)
            self.decon() 
            print 'Removing pid file'
            os.unlink(pidfile)
            print "Stopping listener"
            listener.shutdown()
            print "Listener stopped"
            dubs.cancel()
            print "Killed dubs thread"
            print "Killing process"
            os.kill(os.getpid(), signal.SIGINT)
        except Exception, e:
            print 'An exception occured:',e
        
    def joinChan(self,chan):
        self.ircCom('JOIN',chan)
        self.chans[chan] = deque([],10)
        self.users[chan] = set()
      #  self.ircCom('WHO',chan)

    def setMarkov(self,obj):
        self.markov = obj

    def getDB(self):
        return MySQLdb.connect (host="max-damage",user="fsa",passwd=keys['mysql_pass'],db="tell")

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
  def __init__(self,server,channels,port = 6667,nick = 'TwatBot',admins = [],messages = []):
      Thread.__init__(self)
      self.server = server
      self.channels = channels
      self.port = port
      self.nick = nick
      self.admins = admins
      self.messages = messages
      self.m = 1
      self.setName("Connection thread to: "+server)
      for i in connections:
        if i.conn.server == server:
          self.m = 0
          break
      if self.m != 0:
        self.recon()
  def recon(self):
    self.conn =  Connection(self.server,self.channels,self.port,self.nick,self.admins,self.messages)
  def run(self):
    while True:
        if self.conn.quitting:
            print "Quitting forever"
            #sys.exit(0)
            thread.interrupt_main()
            return
        if self.conn.FATAL_ERROR:
            # Stop thread and restart, don't attempt to reconnect
            self.conn.decon()
            time.sleep(5)
            self.recon()
            continue
        gc.collect()
        try:
            dataN = self.conn.irc.recv(4096)# .decode('utf-8','ignore')
            if self.conn.printAll:
                print dataN
        except (socket.timeout, socket.error), e:
            self.conn.FATAL_ERROR = True
          #  print str(e)
          #  self.conn.decon()
          #  time.sleep(2)
          #  self.conn.irc = False
          #  while not self.conn.irc:
          #    time.sleep(30)
          #    print "Attempting to reconnect to "+self.server
          #    self.conn.irc = self.conn.connect()
        except KeyboardInterrupt:
            self.conn.close()
            print "Keyboard Interrupt detected, exiting"
            return
        for i in dataN.splitlines():
          try:
              if i.split()[0] == 'PING':
                self.conn.ircCom('PONG', i.split(':')[1])
                continue
          except IndexError:
            return
          self.conn.dataN = line(i)
          if not self.conn.dataN: continue
          if self.conn.dataN['cmd'] == 'PRIVMSG' and self.conn.dataN['chan'][0] != '#':
            self.conn.dataN['chan'] = self.conn.dataN['fool']
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
    connections.append(ConnectionServer(i['server'],i['channels'],admins = i['admins'],nick = i['nick'],messages = i['messages']))
for i in connections:
    i.start()  

