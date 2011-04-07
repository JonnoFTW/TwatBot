import urllib
import re
help = "4chan dubs getter AIO. use ^check <board> for current post no. of a bord . 9MB Bale pack at http://www.mediafire.com/?j3idvabga74e8sy"
def getPostCount(board):
   url = 'http://boards.4chan.org/'+board
   f = urllib.urlopen(url)
   page = f.read()
   #Filter out the post numbers
   no = max(map(lambda x: re.sub("[^0-9]","",x),filter(lambda x: (x[:6] == 'id=\"no'),page.split())))
   return no
boards = ['a','b','c','d','e','f','g','gif','h','hr','k','m','o','p','r','s','t','u','v','w','wg','i','ic','cm','y','3','adv','an','cgl','ck','co','fa','fit','int','jp','lit','mu','n','po','sci','soc','sp','tg','toy','trv','tv','vp','x']
def getNo(conn):
    if len(conn.dataN['words']) > 1:
        chan = conn.dataN['words'][1].lower()
        if chan not in boards:
            conn.sendMsg('Please select an actual channel',conn.dataN['chan'])
        else:
            conn.sendMsg('Current post for '+chan+' is:'+getPostCount(chan),conn.dataN['chan'])    
    else:
        conn.sendMsg('How about you give me a board?',conn.dataN['chan'])
 

triggers = {'^check':getNo,'^checkem':getNo}
