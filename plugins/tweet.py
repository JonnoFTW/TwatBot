import random
help = """^^ sends the previous line to twitter. Can't quote yourself either. ^^ n sends the nth line from the scrollback twitter. View with ^scroll. n is n places from the start of the scroll starting at 0. ^last gets the last tweet from Buttsworth. '^last user' gets the last tweet from user."""
badwords = ["jihad","anal","nigger","fuck","global-jihad", "beatdownbrigade", "404chan", "genericus", "hussyvid", "pthc", "kdv", "r@ygold", "kiddy","#ff"]
tags = ["perwlcon","perwl","perl","python"]
def getTwit(conn,user):
        try:
            result = conn.api.GetUserTimeline(user)[0].text
        except Exception, e:
            result = 'Could not get twitter' + str(e)
        return result

def setTwit(conn,msg):
        try:
            result = conn.api.PostUpdate(msg)
            return result
        except Exception, e:
            self.sendMsg( 'Could not update twitter: '+ str(e) )
            return False

def tweet(conn):
    if conn.dataN['fool'] not in conn.banned and conn.dataN['chan'] not in conn.ignores:
        if ("".join(conn.chans[conn.dataN['chan']][len(conn.chans[conn.dataN['chan']])-1].split())) != "":
            try:
              index = int(conn.dataN['words'][1])
            except:
              index = -1
            if conn.dataN['fool'] == conn.chans[conn.dataN['chan']][index].split(':')[0]:
                conn.sendMsg("Can't quote yourself"+( '!'*(random.randint(0,2))))
                return
            if any(map(lambda x: x.lower() in badwords,conn.dataN['words'])):
                conn.sendMsg('Naughty words not allowed')
                return
            else:
                if len(conn.dataN['words']) > 1:
                   toSend = conn.chans[conn.dataN['chan']][int(conn.dataN['words'][1])]
		else:
                    toSend = (conn.chans[conn.dataN['chan']].pop())[:140]
                print(toSend)
                for i in tags:
                    toSend = toSend.replace(i,"#"+i)
                #toSend = ' '.join(map(lambda x: tag(x),toSend.split()))
                if toSend.find("\001ACTION") != -1:
                    toSend = '*** '+(toSend.replace(': \001ACTION','',1)[:-1])
                r = setTwit(conn,toSend)
                spaces = '!'*(random.randint(0,2))  
                if r!= False: conn.sendMsg('Sending to twitter'+spaces) 

def last(conn):
    if len(conn.dataN['words']) > 1:
        conn.sendMsg(getTwit(conn,conn.dataN['words'][1]))
    else:
        conn.sendMsg(getTwit(conn,'Buttsworth_'))


triggers = {'^twat':tweet,'^^':tweet,'^last':last}
