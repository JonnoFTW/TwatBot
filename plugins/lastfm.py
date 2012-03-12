# coding=utf-8

from urllib2 import urlopen
from urllib  import quote, quote_plus
import json

help = "Various functions for last.fm. Use ^np <user> to get a users last played track." 


    
        
def np(conn):
    #get now playing info for a user
    key = conn.conn.keys['lastfm_api_key']
    name = conn.getName('lastfm')
    #Get the users now playing shit
    u = json.load(urlopen("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+quote(name.encode("utf-8"))+"&format=json&api_key="+key))
    try:
        if u['recenttracks']['total'] == '0':
            conn.sendMsg("This user has nothing played")
            print u
            return
    except KeyError: 
        pass
    try:
        track = u['recenttracks']['track'][0]
    except KeyError:
        conn.sendMsg("No user by that name")
        return
    try:
        url = "http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&autocorrect=1&format=json&track="+quote_plus(track['name'].encode("utf-8"))+"&artist="+quote_plus(track['artist']['#text'].encode("utf-8"))+"&album="+quote_plus(track['album']['#text'].encode("utf-8"))+"&api_key="+key
    except KeyError:
        conn.sendMsg("Can't decode runes")
        return
   # print url
    try:
        t = json.load(urlopen(url))
    except:
        conn.sendMsg("An error occured getting the tags")
    try:
  #      print t
        tags = ', '.join(map(lambda x:x['name'],t['toptags']['tag'][:5]))
    except TypeError:
        tags = t['toptags']['tag']['name']
    except KeyError:
        url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&autocorrect=1&format=json&artist="+quote_plus(track['artist']['#text'].encode("utf-8"))+"&api_key="+key
        t = json.load(urlopen(url))
     #   print t
        try:
            tags = ', '.join(map(lambda x:x['name'],t['toptags']['tag'][:5]))
        except KeyError:
            tags = 'No tags available' 
    conn.sendMsg("\0030,4Last.fm\003 User '%s' is now pegging to '%s' by '%s' from '%s', (%s)" % (name,track['name'],track['artist']['#text'],track['album']['#text'],tags)) 

def setlastfm(conn):
    #Associate your nick with a username
    conn.setName('lastfm')
def lastfm(conn):
    #Get info about an artists or something
    conn.sendMsg("Not yet implemented")
triggers = {'^np':np,'^setlastfm':setlastfm, '^lastfm':lastfm}