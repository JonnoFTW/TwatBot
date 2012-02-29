import json
from urllib2 import urlopen
import MySQLdb
import MySQLdb.cursors

help = "^steam <steamid> will get userinfo for the user" 

def steam(conn):
    key = conn.conn.steamKey
    db = conn.conn.getDB() 
    c = db.cursor()
    try:
        #An id was provided
        id = conn.dataN['words'][1]
        #Check if the is in the db
        print repr(db.escape_string(id)) 
        c.execute("SELECT steamId from steamId WHERE `nick` = '"+(db.escape_string(id))+"'")
        x = c.fetchone()
        if x:
            id = x[0]
    except IndexError:
        #No id, perhaps they are stored
        print "Using nick as steam name"

        c.execute("SELECT steamId FROM steamId WHERE `nick` = '"+ db.escape_string(conn.dataN['fool'])+"';")
        print c._last_executed
        x = c.fetchone()
        if x:
            id = str(x[0])
        else:
            conn.sendMsg("No steamId associated with this nick. Use ^setsteam <steamId> to associate your nick with a given steamId")
            return
    except:
        conn.sendMsg("Please provide a steamId, or use ^setsteam <steamId> to associate your nick with a given steamId")
        return
    k = json.load(urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+key+"&steamids="+id))
    if len(k['response']['players']) == 0:
        conn.sendMsg("No such user exists! Please specify a valid steamId ")
        return
    p = k["response"]["players"][0]
    if "primaryclanid" in p:
        #Get their clan name
        clan = "http://steamcommunity.com/gid/"+p["primaryclanid"]
    else: 
        clan = "None"
    if "gameextrainfo" in p:
        game = p["gameextrainfo"]
    else:
        game = "None"
    if "realname" in p:
        name = p["realname"]
    else:
        name = "None"
    if not "loccountrycode" in p:
        p["loccountrycode"] = "None"
    friends = []
    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key="+key+"&steamid="+p["steamid"]+"&relationship=friend"
    for i in json.load(urlopen(url))["friendslist"]["friends"]:
        friends.append(i['steamid'])
    f = json.load(urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+key+"&steamids="+(','.join(friends))))
    friends = []
    for i in f["response"]["players"]:
        friends.append(i["personaname"])
    conn.sendMsg("User: %s, Realname: %s, Country: %s, Playing: %s, Clan: %s, Friends: [%s]"%
                 (p["personaname"],name,p["loccountrycode"],game,clan,'; '.join(friends[:10])))

def setsteam(conn):
    #Associate a nick with a steam id for later use
    try:
        db = conn.conn.getDB()
        steamId = db.escape_string(conn.dataN['words'][1])
        nick = db.escape_string(conn.dataN['fool'])
        c = db.cursor()
        vals = [nick,steamId]
        vals = str(tuple(vals))
        c.execute("""INSERT INTO `steamId` (`nick`,`steamId`) VALUES %s 
                     ON DUPLICATE KEY UPDATE `steamId` = %s;""" % (vals,steamId))
        conn.sendMsg("Set steam for nick "+nick+", use ^steam to view your stats")
    except IndexError, e:
        conn.sendMsg('^setSteam <steamId>. Associates a steamId with your nick to get your details from')
triggers = {"^steam":steam,'^setsteam':setsteam}
