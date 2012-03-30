triggers = {}
def setName(conn,field):   
    try:
        db = conn.getDB()
        id = db.escape_string(conn.dataN['words'][1])
        nick = db.escape_string(conn.dataN['fool'])
        c = db.cursor()
        vals = [nick,id]
        vals = str(tuple(vals))
        c.execute("""INSERT INTO `steamId` (`nick`,`%s`) VALUES %s 
                     ON DUPLICATE KEY UPDATE `%s` = '%s';""" % (field,vals,field,id))
        conn.sendMsg("Set "+field+" for nick "+nick+"")
    except IndexError:
        conn.sendMsg("Please supply a %s to associate your nick with" % (field))
def getName(conn,field):
    try:
        id = conn.dataN['words'][1]
    except IndexError:
        id = conn.dataN['fool']
    db = conn.getDB()
    id = db.escape_string(id)
    c = db.cursor()
    query = "SELECT `"+field+"` FROM steamId WHERE `nick` = '"+id+"'"
   # print field,id, query
    c.execute(query)
  #  print c._last_executed
    x = c.fetchone()
    if x == None or x[0] == None:
        print "Using name: "+ conn.dataN['fool']
        return conn.dataN['fool']
    else:
        print "Using name: "+x[0]
        return x[0]
