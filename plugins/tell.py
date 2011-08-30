import _mysql
help = "^tell will private message the given person whenever and whereever it sees them again"
def addtell(conn):
    try:
      conn = _mysql.connect (host="max-damage",user="TwatBot",passwd="dicks",db="tell")
      conn.query("INSERT INTO tell ('dicks',NOW(),fool)")
      conn.sendMsg("consider it noted")
    except Exception, e:
      conn.sendMsg(str(e))

triggers = {'^tell':addtell}
