# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

#import oauth2
import json
import urllib
import urllib2

def search(keyword, cll):
    consumer_key = 'InepiTUxl4_CN8hRCxV4gA'
    consumer_secret = 'ZzuBLqtEreWlm1FqBltPEImuZ2Q'
    token = '7uAeNaimqgTsYqCzboSZylZUukFJ1-I-'
    token_secret = '22FbVEI8cfO63ROlQDV_bePx3XU'
    consumer= oauth2.Consumer(consumer_key,consumer_secret)
    url= 'http://api.yelp.com/v2/search?location=New+York&term=%s&limit=%d&format=json'%(urllib.quote(keyword), 5)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': token,
                      'oauth_consumer_key': consumer_key})
    token = oauth2.Token(token, token_secret)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    url = oauth_request.to_url()
    conn = urllib2.urlopen(url)
    results =json.load(conn)
    str = results["businesses"][0]["name"]
    return str

if __name__ == "__main__":
    search("pizza","40.9,-74")



            
            
            
