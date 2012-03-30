import json
import re
from urllib2 import urlopen
from urllib  import quote


help = "^steam <steamid> will get userinfo for the user" 

def steam(conn):
    key = conn.conn.steamKey
    db = conn.conn.getDB() 
    c = db.cursor()
    try:
        #An id or nick was provided
        id = conn.dataN['words'][1]
        #Check if the is in the db
        x = conn.getName('steamId')
        if x:
            id = x
        else:
            #Perhaps they are providing a user name?
            s = re.compile('var\sajaxFriendUrl\s\=\s\"http\:\/\/steamcommunity\.com\/actions\/AddFriendAjax\/(\d+)\"\;')
            try:
                f = urlopen("http://steamcommunity.com/id/"+quote(id)).read()
                id = s.findall(f)[0]
            except HTTPError:
                conn.sendMsg("No such user by that name")
                return
                
    except IndexError:
        #No id, perhaps they are stored
        id = conn.getName('steamId')
        if not id:
            conn.sendMsg("No steamId associated with this nick. Use ^setsteam <steamId> to associate your nick with a given steamId")
            return
    except:
        conn.sendMsg("Please provide a steamId, or use ^setsteam <steamId> to associate your nick with a given steamId")
        return
    k = json.load(urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+key+"&steamids="+id))
    if len(k['response']['players']) == 0:
        conn.sendMsg("No such user exists! Please specify a valid steamId ")
        print k
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
        friends.append(i["steamid"])
    conn.sendMsg("User: %s, Realname: %s, Country: %s, Playing: %s, Clan: %s, Friends: [%s]"%
                 (p["personaname"],name,p["loccountrycode"],game,clan,'; '.join(friends[:10])))

def setsteam(conn):
    #Associate a nick with a steam id for later use
    try:
        conn.setName('steamId')
    except IndexError:
        conn.sendMsg('Please provide a steamId to associate your nick with')
        
triggers = {"^steam":steam,'^setsteam':setsteam}
