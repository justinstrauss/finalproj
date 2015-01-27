# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import oauth2
import json
import urllib
import urllib2

# Takes a double array of keywords and an array of coordinates                                                                                                                     
def search(keywords, lls):
    cll = locate(lls)
    frequencies = frequency_dict(keywords)

    consumer_key = 'InepiTUxl4_CN8hRCxV4gA'
    consumer_secret = 'ZzuBLqtEreWlm1FqBltPEImuZ2Q'
    token = '7uAeNaimqgTsYqCzboSZylZUukFJ1-I-'
    token_secret = '22FbVEI8cfO63ROlQDV_bePx3XU'
    consumer= oauth2.Consumer(consumer_key,consumer_secret)
    list_of_businesses = []
    for keyword in frequencies.keys():
        url= 'http://api.yelp.com/v2/search?term=%s&ll=%s&limit=%d&format=json'%(urllib.quote(keyword), cll, 10)
        oauth_request = oauth2.Request('GET', url, {})
        oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                              'oauth_timestamp': oauth2.generate_timestamp(),
                              'oauth_token': token,
                              'oauth_consumer_key': consumer_key})
        tok = oauth2.Token(token, token_secret)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, tok)
        url = oauth_request.to_url()
        conn = urllib2.urlopen(url)
        results =json.load(conn)
        for dictionary in results["businesses"]:
            list_of_businesses.append(dictionary)
    d = {}
    count = 0
    for dict in list_of_businesses:
        # Check to eliminate repeats #                                                                                                                                             
        is_unique = True
        for x in range (0, count):
            if list_of_businesses[x]["name"] == dict["name"]:
                d[count] = 0
                is_unique = False
        
        if is_unique:
            points = 0
        # Takes into account the Yelp rating of the location. 16 points for a full rating of five stars #                                                                          
            points += (dict["rating"] - 1) * 4
        # Takes into account the number of people who chose the cuisine offered at the location. 40 points for all cuisine choices being that cuisine #                            
            number = 0
            for category in dict["categories"]:
                if category[0] in frequencies.keys():
                    number += frequencies[category[0]] * 40 / len(keywords)
                    points += number
        # Takes into account distance from the center location. 10 points for being within a half a mile away from the midpoint #                                                  
            points += min(4000 / dict["distance"], 10)

        # If fewer than 1/10 of the people put that cuisine, the location is not considered #                                                                                      
            if number > 4:
                d[count] = points
            else:
                d[count] = 0
        count += 1

    # Sort the locations by points and keep the top five                                                                                                                           
    list = sorted(d, key=lambda i: d[i])
    list = [list[-1], list[-2], list[-3], list[-4], list[-5]]

    final = []
    for x in list:
        dict = list_of_businesses[x]
        dictionary = {}
        dictionary['name'] = dict['name']
        dictionary['address'] = dict['location']['address']
        dictionary['website'] = dict['url']
        dictionary['rating_image'] = dict['rating_img_url']
        final.append(dictionary)
    return final


def frequency_dict(keywords):
    d = {}
    for list in keywords:
        for keyword in list:
            value = float(1) / len(list)
            if keyword in d.keys():
                d[keyword] += value
            else:
                d[keyword] = value
    return d

def median(list):
    half = len(list) / 2
    list.sort()
    if len(list) % 2 == 0:
        return (list[half-1] + list[half]) / 2.0
    else:
        return list[half]


def locate(lls):
    lattitudes = []
    longitudes = []
    for ll in lls:
        new = ll.split(",")
        lattitudes.append(float(new[0]))
        longitudes.append(float(new[1]))
    ideal_lat = median(lattitudes)
    ideal_lon = median(longitudes)
    return str(ideal_lat) + "," + str(ideal_lon)


if __name__ == "__main__":
    print search([['Pizza','Italian'],['Pizza','Italian'],['Italian','Mexican','Chinese'],['Pizza','Italian','Chinese']],["40.808,-73.962","40.76,-73.986","40.9,-73.0"])


            
            
            
