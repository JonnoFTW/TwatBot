# coding=utf-8

from urllib2 import urlopen
from urllib  import quote, quote_plus, urlencode
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
    urls = [{'method':'track.gettoptags',
             'album':track['album']['#text'].encode("utf-8"),
             'track':track['name'].encode("utf-8")
             },
            {'method':'artist.gettoptags'}]
    for i in urls:
        i['format'] = 'json'
        i['autocorrect'] = 1
        i['artist'] =  track['artist']['#text'].encode("utf-8")
        i['api_key'] = key
    tags = []
    for url in urls:
      try:
          t = json.load(urlopen("http://ws.audioscrobbler.com/2.0/?"+urlencode(url)))
          tags = ', '.join(map(lambda x:x['name'],t['toptags']['tag'][:5]))
          break
      except (TypeError, KeyError):
          tags = 'No tags available' 
          continue
    if track['album']['#text']:
        track['album']['#text'] = " from '"+ track['album']['#text']+"'"
    conn.sendMsg("\0030,4Last.fm\003 User '%s' is now pegging to '%s' by '%s'%s, (%s)" % (name,track['name'],track['artist']['#text'],track['album']['#text'],tags)) 

def setlastfm(conn):
    #Associate your nick with a username
    conn.setName('lastfm')
def lastfm(conn):
    #Get info about an artists or something
    conn.sendMsg("Not yet implemented")
triggers = {'^np':np,'^setlastfm':setlastfm, '^lastfm':lastfm}
