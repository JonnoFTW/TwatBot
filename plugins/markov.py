import os
import re
import glob
import time
import markovgenpy
import random
import cPickle as pickle
help = "Will generate a markov chain from my irc logs, may take a while to generate the database on the first run"

def scrape(conn):
    start = time.time()
    f = open('text.log','w')
    path =  '/home/jonno/logs/'
    p = re.compile(r'^(\,|\03|\d|\.)+$')
    for i in glob.glob(os.path.join(path,'*/#*.log')):
        g = open(i,'r')
        for line in g:
            if line[6] == '<':
                if line.find('http://') == -1:
                    f.write(p.sub('',line[line.find('>')+1:])+' \n')
        g.close()
    f.close()
    finish = time.time()
    conn.sendMsg('Built log in %5g s' % (finish-start),conn.dataN['chan'])
    

def firstrun(conn):
    try:
        if conn.conn.markov == None:
            return
    except:
        pass
    conn.conn.markov = None
    conn.sendMsg('Generating database')
#    scrape(conn)
    f = open('text.log','r')
    start = time.time()
#    conn.log.seek(0,0)
#    trainer = open('/home/jonno/lambdabot/trainer.log','r')
    conn.conn.setMarkov(markovgenpy.Markov(f))
    f.close()
    #conn.setMarkov(pickle.load(open('markov.pickle')))
    finish = time.time()
    conn.sendMsg('Built markov object in %5g s' %(finish-start),conn.dataN['chan'])

def markov(conn):
    try:
        conn.sendMsg(conn.conn.markov.generate_markov_text(random.randint(5,20)),conn.dataN['chan'])
    except Exception, e:
        firstrun(conn)

def rem(conn):
    conn.sendMsg('Freeing memory, removing markov object')
    del conn.conn.markov
triggers = { '^markov':markov,'^markovgen':firstrun,'^freemarkov':rem}
