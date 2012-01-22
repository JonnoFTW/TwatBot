import json
from urllib2 import urlopen
help = "^steam <steamid> will get userinfo for the user" 

def steam(conn):
    key = conn.conn.steamKey
    k = json.load(urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+key+"&steamids="+conn.dataN['words'][1]))
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
    
triggers = {"^steam":steam}
