import socket
import uuid 
from subprocess import check_output
import random 
import time
help = "Copies the functionality of amigo"

def uid(conn):
   conn.sendMsg(str(uuid.uuid1()).upper())
def fortune(conn):
    for i in check_output(["fortune","-s"]).split('\n'):
        conn.sendMsg(i)
def uname(conn):
    conn.sendMsg(check_output(["uname","-a"]))
def w(conn):
  running = check_output(["w","-hsf"]).split('\n')
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
    conn.sendMsg('eternal summers time',time.localtime())
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
       ip = ""
     ass = check_output(["dig",ip,conn.dataN['words'][1],"+short"]).split('\n')
     conn.sendMsg(', '.join(ass)[:-2])
   except IndexError,e :
     conn.sendMsg("Please provide a domain to search for")
triggers = { '^fortune':fortune,
             '^uname':uname,
             '^time':ti,
             '^w':w,
             '^uuid':uid,
             '^sdate':sdate,
             '^roulette':roulette,
             '^dig':dig }
    
