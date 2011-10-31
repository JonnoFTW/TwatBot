import urllib2
import json
help = "Gets the definition of a word from the urbandictionary website"

def urban(conn):
  try:
    d = json.load(urllib2.urlopen("http://www.urbandictionary.com/iphone/search/define?term="+conn.dataN['words'][1]))
    if 'pages' not in d:
      conn.sendMsg("Word is not defined")
    else:
      conn.sendMsg(d['list'][0]['definition'])
  except Exception, e:
    print e
    conn.sendMsg("Usage is: ^ud <word>")

triggers = {'^ud':urban}
