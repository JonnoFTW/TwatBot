import MySQLdb
import MySQLdb.cursors
import cPickle
import re
import socket
import uuid 
import subprocess
import random 
from datetime import datetime
import time
help = "Copies the functionality of amigo"
def suptime(conn):
   conn.sendMsg(subprocess.check_output(["uptime"]))
def uid(conn):
   conn.sendMsg(str(uuid.uuid1()).upper())
def fortune(conn):
    for i in subprocess.check_output(["fortune","-s"],shell=True).splitlines():
        conn.sendMsg(i.replace("\x03",""))
def uname(conn):
    conn.sendMsg(subprocess.check_output(["uname","-a"]))
def w(conn):
  running = subprocess.check_output(["w","-hsf"]).splitlines()
  users = dict()
  for i in running:
    j = i.split()
    u = j[0]
    proc = (' '.join(j[3:]))
    if u in users:
      users[u] = users[u]+', '+proc
    else:
      users[u] = proc
  for i in users.items():
    conn.sendMsg(i[0]+': '+i[1])
                                          
def ti(conn):
    conn.sendMsg(time.strftime("%a %b %d %H:%M:%S %Z %Y",time.localtime()))
    
def sdate(conn):
    then = datetime(1993,8,31,0,0,0)
    now = datetime.now()
    conn.sendMsg(time.strftime('%a Sep '+str((now-then).days)+' %H:%M:%S %Z 1993',time.localtime()))
def roulette(conn):
    conn.sendMsg('\001ACTION Loads a single round into the revolver and places it to '+conn.dataN['fool']+'\'s head\001')
    if random.randint(1,6) == 6:
      conn.sendMsg('\001ACTION *BANG*\001')
      conn.sendMsg('.kb '+conn.dataN['fool'])
    else:
      conn.sendMsg('\001ACTION *click*\001')
def dig(conn):
   try:
     try:
       socket.inet_aton(conn.dataN['words'][1])
       ip = "-x"
     except socket.error:
       if not re.match(r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*',conn.dataN['words'][1]):
           conn.sendMsg('Please enter a valid domain name')
           return
       ip = " "
     ass = subprocess.check_output(["dig",ip,conn.dataN['words'][1],"+short"]).split('\n')
     conn.sendMsg(', '.join(ass)[:-2])
   except IndexError,e :
     conn.sendMsg("Please provide a domain to search for")
def trendy(conn):
    # Be sure to have a trendy file ready
    trends = []
    for line in open('plugins/trendy'):
       trends.append(line[:-1])
    l = len(trends)-1
    conn.sendMsg(' '.join([trends[random.randint(0,l)],trends[random.randint(0,l)],trends[random.randint(0,l)]]))
def uptime(conn):
    conn.sendMsg(str(datetime.now()-conn.uptime))

def hipster(conn):
   hip = []
   for line in open('plugins/hipster'):
      hip.append(line[:-1])
   l = len(hip)-1
   out = []
   while(len( (' '.join(out).split())) < 5):
      out.append(hip[random.randint(0,l)])
   conn.sendMsg(' '.join(out))
   
def asl(conn):
#   conn.sendMsg('new behaviour!')
   places = ['sa','hawaii','israel','nigeria','aus','cali','nyc','nsw','fl','uk','france','russia','germany','japan','china','nz']
   conn.sendMsg('/'.join([str(random.randint(8,30)),random.choice(['m','f']),random.choice(places)]))

def flip(conn):
   if random.randint(0,1): 
      msg = 'Heads'
   else:
      msg = 'Tails'
   conn.sendMsg('A coin is flipped, '+msg)
def roll(conn):
   conn.sendMsg('A dice is rolled '+str(random.randint(1,6)))

def joke(conn):
   jokes = []
   buf = []
   for line in open('plugins/jokes.txt'):
      if line.split() == []:
         if buf != []:
            jokes.append(buf)
            buf = []
      else:
         buf.append(line.strip())
   for i in random.choice(jokes):
      conn.sendMsg(i)

def doubles(conn):
   db = conn.conn.getDB()
   cursor = db.cursor()
   try:
     if conn.dataN['words'][1]:
       if conn.dataN['words'][1] == "top":
           #print the top 3 users
           cursor.execute("SELECT *  FROM doubles order by quads desc, trips desc, dubs desc, misses desc limit 0,3")
           conn.sendMsg("Top doubles users are: ")
           for i in cursor.fetchall():
            conn.sendMsg(i[0]+': Dubs:'+str(i[1])+ ' Trips:'+str(i[2])+' Quads:'+str(i[3])+ ' Misses:'+str(i[4]))
       elif conn.dataN['words'][1] == "losers":
           cursor.execute("SELECT *  FROM doubles order by misses desc limit 0,3")
           conn.sendMsg("Top losers users are: ")
           for i in cursor.fetchall():
            conn.sendMsg(i[0]+': Dubs:'+str(i[1])+ ' Trips:'+str(i[2])+' Quads:'+str(i[3])+ ' Misses:'+str(i[4]))
       else:
           print "Getting user"
           # Get the user specified
           cursor.execute("SELECT * FROM doubles WHERE `nick` = '%s'" % (db.escape_string(conn.dataN['words'][1])))
           x= cursor.fetchone()
           if x:
             print cursor._last_executed
             print x
             conn.sendMsg(conn.dataN['words'][1]+ ': Dubs:'+str(x[1])+ ' Trips:'+str(x[2])+' Quads:'+str(x[3])+ ' Misses:'+str(x[4]))
           else:
             conn.sendMsg('No results for user')
   except IndexError:
    n = str(conn.conn.dubs.count).zfill(4)
    count = 0
    for i in n[::-1]:
       if i == n[-1]:
          count += 1
       else:
          break
    out = {1:" ",2:", DOUBLES",3:", TRIPS",4:", QUADS"}[count]
    c = {1:'misses',2:'dubs',3:'trips',4:'quads'}[count]
    nick = db.escape_string(conn.dataN['fool'])
    # if "noxialis" in conn.dataN['fool'].lower():
        # if random.randint(0,2) == 0:
            # conn.sendMsg("Critical error, scores reset")
            # cursor.execute("DELETE FROM `doubles` WHERE `nick` = '"+nick+"';")
    vals = [nick,0,0,0,0]
    vals[count] = 1
    vals = str(tuple(vals))
    cursor.execute("""INSERT INTO `doubles` (`nick`,`misses`,`dubs`,`trips`,`quads`) 
                        VALUES %s 
                        ON DUPLICATE KEY UPDATE `%s` = `%s` +1 ;""" % (vals,c,c))
    print cursor._last_executed
    print count
    if count > 1:
        conn.sendMsg("You rolled "+n+out)
    else:
        conn.sendNot("You rolled "+n+out)
        
def lines(conn):
    db = MySQLdb.connect (host="max-damage",user="Twatbot",passwd="dicks",db="tell")
    cursor = db.cursor()
    try:
        nick = conn.dataN['words'][1]
    except IndexError:
        nick = conn.dataN['fool']
    cursor.execute("SELECT COUNT(`nick`) FROM `logs` WHERE `nick` = '%s'" % (db.escape_string(nick)))
    conn.sendMsg("Lines from "+nick+": "+str(cursor.fetchone()[0]))
   
def latin(conn):
    try:
      if conn.conn.latin:
        #Print a random latin phrase
        key = random.choice(conn.conn.latin.keys())
        print key
        conn.sendMsg(key +' ----> '+conn.conn.latin[key])
    except AttributeError, e:
      conn.conn.latin = None
      pkl = open('plugins/latin.pkl','rb') 
      conn.conn.latin = cPickle.load(pkl)
      conn.sendMsg("Loaded phrases")
      pkl.close()
      latin(conn)
def genre(conn):
    prefixes = ['','post','indie','avant-garde','nautical','break','wub','chip','vintage','classic','virtuosic','death','instrumental','british','industrial','thrash','japanese','J','K','acoustic','progressive','power','glam','melodic','new wave','german','gothic','symphonic','grind','synth','minimal','psychedelic','brutal','sexy','easy listening','christian','anime','stoner','comedy','sad','christmas','neo','russian','finnish','summer','underground','dream','pagan','minimal','ambient','nu','speed','contemporary','alt','acid','english','kvlt','cult','mu','raw','norwegian','viking','porn']
    suffixes = ['core','','step','groove','noise']
    gens = ['folk','ambient','electronica','funk','hip-hop','dance','pop','trance','indie','soul','hard','lounge','blues','classical','grunge','/mu/core','emo','rap','rock','punk','alternative','nautical','electro','swing','screamo','jazz','reggae','metal','classical','math','nerd','country','western','dub',"drum 'n' bass",'celtic','shoegaze']
    x = random.choice(prefixes)
    if x:
        x +='-'
        if random.randint(0,2) == 1:
            x += random.choice(prefixes)+'-'
    x += random.choice(gens)
    if random.randint(0,3) == 1:
        x += random.choice(suffixes)
    
    conn.sendMsg(x)
triggers = { '^fortune':fortune,
             '^uname':uname,
             '^lines':lines,
             '^time':ti,
             '^w':w,
             '^uuid':uid,
             '^sdate':sdate,
             '^roulette':roulette,
             '^trendy':trendy,
             '^dig':dig,
             '^uptime':uptime,
             '^hipster':hipster,
             'asl':asl,
             '^suptime':suptime,
             '^roll':roll,
             '^joke':joke,
             '^flip':flip,
             '^doubles':doubles,
             '^latin':latin,
             '^genre':genre
}
    
