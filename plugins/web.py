from BeautifulSoup import BeautifulSoup
import urllib2
import json
help = "^google <string> does a google search, ^urban <word> gets first urbandictionary def, ^weather <State> <Location> gets the weather from the BOM. Australia only!"

def convert(s):
  s = s.replace("<b>",'\2')
  s = s.replace("</b>",'\2')
  return s
def search(conn):
    try:
      page = json.load(urllib2.urlopen("https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+('%20'.join(conn.dataN['words'][1:]))))
      for i in page["responseData"]["results"]:
        conn.sendMsg(convert(i["title"])+": "+i["url"])
    except IndexError, e:
      conn.sendMsg("Usage is: ^google <search string>")

def urban(conn):
  try:
    d = json.load(urllib2.urlopen("http://www.urbandictionary.com/iphone/search/define?term="+('%20'.join(conn.dataN['words'][1:]))))
    if 'pages' not in d:
      conn.sendMsg("Word is not defined")
    else:
      conn.sendMsg(d['list'][0]['definition']+'--- '+d['list'][0]['example'])
  except Exception, e:
    print e
    conn.sendMsg("Usage is: ^ud <word>")
ids = {}
def init_weather():
    states = ["nsw","vic","wa","qld","wa","sa","tas","act","nt"]
    for i in states:
        ids[i] = {}
        if i == "act":
            url = "http://www.bom.gov.au/"+i+"/observations/canberra.shtml"
        else:
            url = "http://www.bom.gov.au/"+i+"/observations/"+i+"all.shtml"
        soup = BeautifulSoup(urllib2.urlopen(url))
        for j in soup.findAll("tr", {"class":"rowleftcolumn"}):
            tag = j.find("th")
            ids[i][tag.text.lower()] = tag.a["href"].split("/")[-1][:-6]
                                                    
        
def weather(conn):
    if len(ids) == 0:
        conn.sendMsg("Consuming memory")
        init_weather()
    try:
        state = conn.dataN['words'][1].lower()
        loc = ' '.join(conn.dataN['words'][2:]).lower()
        s = ids[state][loc]
        url = "http://www.bom.gov.au/fwo/"+(s.split(".")[0])+"/"+s+".json"
        q = json.load(urllib2.urlopen(url))    
        out = ""
        for i in ['City','Temp','Wind','Rain','Humidity','Wind_Dir']:
           out += '%s ' % (i.rjust(9))
        conn.sendMsg(out)
        out = ""
        for i in ['name','air_temp',"wind_spd_kmh","rain_trace","rel_hum","wind_dir"]:
           out += "%s " % (str(q['observations']['data'][0][i]).rjust(9))
        conn.sendMsg(out)
    except IndexError, e:
        conn.sendMsg("Usage is ^weather <State> <Location>")
    except KeyError, e:
        conn.sendMsg("No information for this location")
        
def refreshFML(conn):
  conn.sendMsg("Refreshing page")
  conn.page = BeautifulSoup(urllib2.urlopen("http://fmylife.com/random")).findAll('div',{"class":"post article"})
def fml(conn):
  try:
      if len(conn.page) == 0:
        refreshFML(conn)
  except AttributeError, e:
      refreshFML(conn)
  conn.sendMsg(conn.page.pop().p.text)


def levenshtein(w1,w2):
  x = len(w1)
  y = len(w2)
#  table = [][]
  for i in range(0,x+1):
      pass
  
triggers = {'^ud':urban,'^g':search, '^google':search,"^weather":weather,'^fmyl':fml}
