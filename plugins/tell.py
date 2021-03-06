# coding=utf-8
import MySQLdb
import MySQLdb.cursors
help = "^tell will private message the given person whenever and whereever it sees them again. use ^read to read any message you may have"


def addTell(conn):
    """
    Usage: ^tell <to> <msg>
    Add a tell to the database for a specific username.
    Database has:
        - Table tell- (PK)msgId,to(nick),message,time,sender(nick)
    """
    try:
      db = conn.conn.getDB()
      cursor = db.cursor()
      cursor.execute("""INSERT INTO tell (`to`,message,time,sender)
                     VALUES (%s,%s,NOW(),%s)""",
                     (conn.dataN['words'][1],
                      ' '.join(conn.dataN['words'][2:]),
                      conn.dataN['fool']))
      conn.sendMsg("Consider it noted")
      conn.tells.add(conn.dataN['words'][1])
      print conn.tells
    except Exception, e:
      print e
      conn.sendMsg("Usage: ^tell <to> <message>")
    finally:
      cursor.close()
      db.close() 
def getTell(conn):
    try:
      db = conn.conn.getDB()
      cursor = db.cursor()
      cursor.execute("""SELECT tell.sender, tell.message, tell.time
                        FROM tell WHERE `to` = %s
                     """,(conn.dataN['fool']))
      msgs = cursor.fetchall()
      if len(msgs) == 0:
          conn.sendNot("You have no messages")
      else:
          conn.sendNot("You have the following messages: ")
          for i in msgs:
              try:
                  conn.sendNot(u"From: {0} on {1} -----> {2}".format(i[0],i[2],i[1]).decode('utf-8'))
              except:
                  pass
          cursor.execute("DELETE FROM tell WHERE `to` = %s",(conn.dataN['fool']))
          cursor.close()
          try:
            conn.tells.remove(conn.dataN['fool'])
          except:
            print "Could not remove user from send to list"
    except Exception, e:
        print e
        conn.sendNot("Something went wrong telling the message! %s" % (str(e)))
    finally:
        cursor.close()
        db.close()

triggers = {'^tell':addTell,'^read':getTell}
