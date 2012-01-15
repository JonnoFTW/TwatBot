# coding=utf-8
from BeautifulSoup import BeautifulSoup
import urllib2
import json
import xml.dom.minidom
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
    if conn.dataN['words'][-1].isdigit():
      i = conn.dataN['words'].pop()
    else:
      i = 0
    d = json.load(urllib2.urlopen("http://www.urbandictionary.com/iphone/search/define?term="+('%20'.join(conn.dataN['words'][1:]))))
    if 'pages' not in d:
      suggestions = map(lambda x: x['term'],(filter(lambda x: x['type'] == 'link',d['list'])))[:4]
      conn.sendMsg("Word is not defined. Perhaps you meant: "+(', '.join(suggestions)))  
    else:
      conn.sendMsg(d['list'][int(i)]['definition']+'--- '+d['list'][int(i)]['example'])
  except IndexError, e:
    print e
    conn.sendMsg("Usage is: ^ud <word>")
       
def weather(conn):
    chan = str(conn.dataN['chan'])
    try:
        state = conn.dataN['words'][1].lower()
        loc = ' '.join(conn.dataN['words'][2:]).lower()
        with open("plugins/bom.dat") as f:
          for i in f:
            j = i.split()
            if j[0] == state:
              if ' '.join(j[2:]) == loc:
                s= j[1]
                break
            elif j[0] > state:
              break
        url = "http://www.bom.gov.au/fwo/"+(s.split(".")[0])+"/"+s+".json"
        q = json.load(urllib2.urlopen(url))    
        out = ""
        for i in ['City',u'Temp(°C)','Wind(m/s)','Rain(mm)','Humidity(%)','Wind_Dir','Wind_spd(km/h)','Visibility(km)','Updated']:
           out += '%s ' % (i.rjust(10))
        conn.sendMsg(out,chan)
        out = ""
        for i in ['name','air_temp',"wind_spd_kmh","rain_trace","rel_hum","wind_dir","wind_spd_kmh","vis_km","local_date_time"]:
           out += "%s " % (str(q['observations']['data'][0][i]).rjust(10))
        conn.sendMsg(out,chan)
    except IndexError, e:
        conn.sendMsg("Usage is ^weather <State> <Location>",chan)
    except NameError, e:
        # Using google weather now
        p = urllib2.urlopen("http://www.google.com/ig/api?weather="+('+'.join(conn.dataN['words'][1:]))).read()
        dom = xml.dom.minidom.parseString(p)
        info = dict()
        info["city"] = dom.getElementsByTagName("city")[0].getAttribute("data")
        for i in dom.getElementsByTagName("current_conditions")[0].childNodes:
            info[i.tagName] = i.getAttribute("data")
        conn.sendMsg(' '.join(["City:",     info["city"],
                                u"Temp (°C):",  info["temp_c"],
                                info["humidity"],
                                info["wind_condition"],
                                "Condition:", info["condition"]
                                ])
                    )
        #conn.sendMsg("No information for this location",chan)
        
def refreshFML(conn):
  conn.sendMsg("Refreshing page")
  conn.conn.page = BeautifulSoup(urllib2.urlopen("http://fmylife.com/random")).findAll('div',{"class":"post article"})
def fml(conn):
  try:
      if len(conn.conn.page) == 0:
        refreshFML(conn)
  except AttributeError, e:
      refreshFML(conn)
  conn.sendMsg(conn.conn.page.pop().p.text)

def etymology(conn):
  try:
    page = BeautifulSoup(urllib2.urlopen("http://www.etymonline.com/index.php?search="+conn.dataN['words'][1]))
    conn.sendMsg(page.find('dd').text[:400])
  except IndexError,e :
    conn.sendMsg('usage is ^etym <word>')
  except AttributeError:
    conn.sendMsg('No word history available')
  
def levenshtein(w1,w2):
  x = len(w1)
  y = len(w2)
#  table = [][]
  for i in range(0,x+1):
      pass
def openBook(conn):
  try:
    j =json.load(urllib2.urlopen("http://graph.facebook.com/search?q="+('%20'.join(conn.dataN['words'][1:]))+"&type=post"))
    for i in j["data"]:
      try:
        conn.sendMsg((i["from"]["name"]+": "+i["message"])[:750])
        break
      except:
        pass
    del j
  except (IndexError, urllib2.HTTPError), e:
    conn.sendMsg("Usage is ^fb <search string>")
  
triggers = {'^ud':urban,
            '^g':search,
            '^google':search,
            "^weather":weather,
            '^fmyl':fml,
            '^fb':openBook,
            '^etym':etymology
            }
