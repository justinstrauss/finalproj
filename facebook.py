import urllib2, json
##FACEBOOK API KEY
client_id = "935483263159079"
client_secret = "ce39cb172d25891be741905badf002e9"
access_token  = "935483263159079|7EyHz4GRI92YiJxik2E-91MuW1o"

def get_uname(user_id):
    url = "https://graph.facebook.com/%s"%(user_id)
    request = urllib2.urlopen(url)
    result = request.read()
    d = json.loads(result) #dictionary of our results
    print d["username"]

def fb_profile():
    url = "http://graph.facebook.com/%s/accounts?key=value&"
    request = urllib2.urlopen(url)
    result = request.read()
    d = json.loads(result) #dictionary of our results
    #print d["username"]
    execTime = d['executionTime'] #gets the time when program was run, keeping here in case we want to use that somewhere!.
    rlist = d['stationBeanList']
    return rlist
#given a specific location, will return the dictionary entry to the nearest citibike station
    
if __name__ == '__main__':
    get_uname(100000550963490)
