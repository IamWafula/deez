import requests 
import  json


def check(site):
    dat =     {
    "client": {
      "clientId":      "yourcompanyname",
      "clientVersion": "1.5.2"
    },
    "threatInfo": {
      "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING"],
      "platformTypes":    ["WINDOWS"],
      "threatEntryTypes": ["URL"],
      "threatEntries": [
        {"url": site},
        
      ]
    }
  }

    datj = json.dumps(dat)

    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=AIzaSyBEO67oFG453JIXCpB38kbMhr6o4UQT2W4"
    res = requests.post(url,datj).text

    if '"threatType": "SOCIAL_ENGINEERING"' in res:
      return False
    else:
      return True


