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
  
triggers = {'^stat':stat}
