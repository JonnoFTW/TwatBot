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
  running = subprocess.check_output(["w","-hsf"]).split('\n')
  users = dict()
  for i in running[:-2]:
    j = i.split()
    proc = (' '.join(j[3:]))
    if proc.count('bash') != 0:
      continue
    if j[0] in users:
      users[j[0]] = users[j[0]]+', '+proc
    else:
      users[j[0]] = proc
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
   places = ['nigeria','aus','cali','nyc','nsw','fl','uk','france','russia','germany','japan','china','nz']
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

def ff(conn):
   conn.sendMsg("\002[SM] Friendly fire is disabled.\002")
   
def thetime(conn):
   conn.sendMsg(time.strftime("%H:%M:%S",time.localtime()))

def rank(conn):
   u = len(conn.conn.users[conn.dataN['chan']])
   conn.sendMsg("Your rank is: "+str(random.randint(1,u))+"/"+str(u))

def statsme(conn):
   stats = ["p90 pub hero","deagle hero","awp whore","team flasher",
           "meat shield","gary","knif crab","DUAL AKIMBO","\002100% MAVERICK\002",
            "cv-47 clutch champion","GLOCKenspiel","happy camper",
            "grrgrgrgrgrgrgr","(gary)","long A rusher","afk","naked",
            "clarion burst fire headshot","bhopping scout master race","MP5 navy SEAL",
            "l33t kr3w","pot plant"]
   conn.sendMsg(conn.dataN['fool']+ " status: "+random.choice(stats))
   
triggers = { '^fortune':fortune,
             '^uname':uname,
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

             'ff':ff,
             'thetime':thetime,
             'rank':rank,
             'statsme':statsme
             }
    
