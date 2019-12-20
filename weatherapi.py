import datetime
import json
import urllib3

def calltemp(stationid):
    dend=str(datetime.date.today())
    dbegin=str(datetime.date.today() - datetime.timedelta(days=365))
    http=urllib3.PoolManager()
    webdata=http.request('GET','https://api.meteostat.net/v1/history/daily?station='+str(stationid)+'&start='+dbegin+'&end='+dend+'&key=Z2J6clWF')
    jdata=json.loads(webdata.data.decode('UTF-8'))
    tempdata=[]
    for i in range(len(jdata['data'])):
        tempdata.append(jdata['data'][i]['temperature'])
    ctempdata = [x for x in tempdata if x != None]
    ctempdata=ctempdata+ctempdata+ctempdata
    return ctempdata




#salt lake city = 72572
#bangkok, thailand = 48454
#los angeles = 72295
#casablanca, morocco = 60155
#london, england = 03772