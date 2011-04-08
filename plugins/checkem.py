import urllib
import re
help = "4chan dubs getter AIO. use ^check <board> for current post no. of a board . 9MB Bale pack at http://www.mediafire.com/?j3idvabga74e8sy"

def readWord(f,s = ''):
    p = f.read(1)
    if p == ' ':
        return s
    else:
        return readWord(f,s+p)
def getNos(f):
    nos = []
    # Read in first 8 tags
    count = 0
    while count != 8:
       word = readWord(f)
       if word[:6] == 'id=\"no':
         count+= 1
         nos.append(re.sub("[^0-9]","",word))
    return max(nos)

def getPostCount(board):
   url = 'http://boards.4chan.org/'+board
   f = urllib.urlopen(url)
   return getNos(f)
boards = ['a','b','c','d','e','f','g','gif','h','hr','k','m','o','p','r','s','t','u','v','w','wg','i','ic','cm','y','3','adv','an','cgl','ck','co','fa','fit','int','jp','lit','mu','n','po','sci','soc','sp','tg','toy','trv','tv','vp','x']
def getNo(conn):
    if len(conn.dataN['words']) > 1:
        chan = conn.dataN['words'][1].lower()
        if chan not in boards:
            conn.sendMsg('Please select an actual channel',conn.dataN['chan'])
        else:
            conn.sendMsg('Current post for '+chan+' is: '+getPostCount(chan),conn.dataN['chan'])    
    else:
        conn.sendMsg('How about you give me a board?',conn.dataN['chan'])
 

triggers = {'^check':getNo,'^checkem':getNo}
