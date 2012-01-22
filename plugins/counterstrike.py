import time
import random
help = "Command line Counter Strike: Source"

def ff(conn):
   conn.sendMsg("\002[SM] Friendly fire is disabled.\002")
   
def thetime(conn):
   conn.sendMsg(time.strftime("%H:%M:%S",time.localtime()))

def timeleft(conn):
    conn.sendMsg(time.strftime("[SM] Time remaining for map: %M:%S",(time.gmtime((20*60)-(time.time() % (20*60))))))

def rank(conn):
   u = len(conn.conn.users[conn.dataN['chan']])
   conn.sendMsg("Your rank is: "+str(random.randint(1,u))+"/"+str(u))

def statsme(conn):
   stats = ["p90 pub hero","deagle hero","awp whore","team flasher",
           "meat shield","gary","knif crab","DUAL AKIMBO","\002100% MAVERICK\002",
            "cv-47 clutch champion","GLOCKenspiel","happy camper",
            "grrgrgrgrgrgrgr","(gary)","long A rusher","afk","naked",
            "clarion burst fire headshot","bhopping scout master race","MP5 navy SEAL",
            "l33t kr3w","pot plant"]
   conn.sendMsg(conn.dataN['fool']+ " status: "+random.choice(stats))
   
def nextmap(conn):
    updateMap(conn)
    if len(conn.conn.maps) == 1:
        conn.sendMsg("This is the last round")
        return
    if len(conn.conn.maps) == 0:
        resetmaps(conn)
    
    conn.sendMsg("[SM] Next map: "+conn.conn.maps[1])

def currentmap(conn):
    updateMap(conn)
    conn.sendMsg("[SM] Current map is: "+conn.conn.maps[0])

def updateMap(conn):
    try:
        print "Rounds since last checked: " + str( int( (time.time() - conn.conn.nextMap) / (20*60))-1)
        print "Map list is: "+ (', '.join(conn.conn.maps))
        for i in xrange(int((time.time() - conn.conn.nextMap)/(20*60))-1):
            if len(conn.conn.maps) == 0:
                resetmaps(conn)
            conn.conn.maps.pop(0)
    except AttributeError:
        resetmaps(conn)
def resetmaps(conn):
    try:
        if time.time() > conn.conn.nextMap:
            conn.conn.nextMap = time.time() + (time.time() % (20*60))
    except AttributeError:
        conn.conn.nextMap = time.time() + (time.time() % (20*60))
    conn.conn.lastChecked = time.time()
    maps = ["cs_office","cs_assault","de_dust2","de_aztec","de_inferno","cs_italy","de_train","de_nuke","fy_iceworld","de_dust"]
    random.shuffle(maps)
    conn.conn.maps = maps
    
triggers ={  'ff':ff,
             'thetime':thetime,
             'rank':rank,
             'statsme':statsme,
             'timeleft':timeleft,
             'nextmap':nextmap,
             'currentmap':currentmap}
