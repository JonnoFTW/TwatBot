import resource
help = "^stat shows memory/cpu usage"

def stat(conn):
  r = resource.getrusage(resource.RUSAGE_SELF)
  out = ''
  if r.ru_maxrss < 1024:
    out = str(r.ru_maxrss/8) + " kB"
  else:
    out = str(r.ru_maxrss/1024) + " MB"
  conn.sendMsg(out)
  
def debug(conn):
    try:
        if conn.dataN['fool'] in conn.conn.admins:
            if conn.dataN['words'][1] == "on":
                conn.conn.printAll = True
                conn.sendMsg("Debugging on")
            elif conn.dataN['words'][1] == "off":
                conn.conn.printAll = False
                conn.sendMsg("Debugging off")
            else:
                conn.sendMsg("Usage is ^debug on|off")
    except IndexError:
        conn.sendMsg("Debugging is %s" %(str(conn.conn.printAll)))
triggers = {'^stat':stat,'^debug':debug}
