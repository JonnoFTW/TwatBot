import urllib2
import json
help = "^google <search string> performs the google search and returns links!"

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
triggers = {'^g':search, '^google':search}
