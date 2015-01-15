import urllib2
import json
def return_cor(x):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + x + "&key=AIzaSyDbtcCT9g5ulN1-ISPD_XyHxp8w_wadh3U"
    request = urllib2.urlopen(url)
    result = request.read()
    d = json.loads(result)
    return d['results']['geometry']['location']['lat'] + ' , ' + d['results']['geometry']['location']['long']

print return_cor("345+chambers+st+NY")
