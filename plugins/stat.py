import resource
import psutil
help = "^stat shows memory/cpu usage"
import threading
def threads(conn):
  conn.sendMsg(", ".join(map(lambda x: x.getName(),threading.enumerate())))
def stat(conn):
  r = resource.getrusage(resource.RUSAGE_SELF)
  out = ''
  if r.ru_maxrss < 1024:
    out = str(r.ru_maxrss/8) + " kB"
  else:
    out = str(r.ru_maxrss/1024) + " MB"
  conn.sendMsg("Bot mem usage:"+str(out)+"; System CPU:"+str(psutil.cpu_percent(interval=1))+"% ;System mem usage: "+str(psutil.phymem_usage()[3])+"%")
  
  
def ddos(conn):
    try:
        conn.sendMsg("Now DDoSing "+conn.dataN['words'][1])
    except:
        conn.sendMsg("Now DDoSing "+conn.dataN['fool'])
         

def debug(conn):
    try:
        if conn.dataN['fool'] in conn.conn.admins:
            if conn.dataN['words'][1] == "on":
                conn.conn.printAll = True
                conn.sendMsg("PrintAll is on")
            elif conn.dataN['words'][1] == "off":
                conn.conn.printAll = False
                conn.sendMsg("PrintAll off")
            else:
                conn.sendMsg("Usage is ^debug on|off")
    except IndexError:
        conn.sendMsg("prinatAll is %s" %(str(conn.conn.printAll)))
triggers = {'^stat':stat,'^printAll':debug,'^ddos':ddos,'^threads':threads}
