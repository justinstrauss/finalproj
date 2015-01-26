import urllib2
import urllib
import json
def return_cor(x):
    x = urllib.quote_plus(x)
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + x + "&key=AIzaSyDbtcCT9g5ulN1-ISPD_XyHxp8w_wadh3U"
    request = urllib2.urlopen(url)
    result = request.read()
    d = json.loads(result)
    return str(d['results'][0]['geometry']['location']['lat'])+ ' , ' + str(d['results'][0]['geometry']['location']['lng'])
