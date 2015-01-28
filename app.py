# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import database
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_oauth import OAuth
from functools import wraps
import urllib2, json, urllib
import yelp
#in the virtual env: $pip install facebook-sdk
import facebook

##FACEBOOK GRAPH API: use these if running on serve
FACEBOOK_APP_ID = "935483263159079"
FACEBOOK_APP_SECRET = "ce39cb172d25891be741905badf002e9"

##FACEBOOK GRAPH API: use these if running on localhost
# FACEBOOK_APP_ID = '188477911223606'
# FACEBOOK_APP_SECRET = '621413ddea2bcc5b2e83d42fc40495de'

app = Flask(__name__)
app.secret_key = "don't store this on github"
app.debug = True
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if session["name"]==None:
            flash("You must login to access this protected page!")
            session['nextpage'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner

@app.route('/')
@app.route('/index')
def index():
    if "id" not in session or session['id']==None:
        session["name"] = None
        session['id'] = None
        return render_template("about.html")
    else:
        inviteDict = database.get_invites_for_user(session['id'])
        pending = inviteDict['pending']
        needsapproval = inviteDict['needsapproval']
        ready = inviteDict['ready']
        return render_template("index.html", pending=pending, ready=ready, needsapproval=needsapproval)

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
    next=request.args.get('next') or request.referrer or None,
    _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    session['token'] = resp['access_token']
    me = facebook.get('/me')
    session['name'] = me.data['name']
    session['id'] = me.data['id']
    if not database.user_exists(session['id']):
        database.add_user(session['name'],session['id'])
        flash("Since you are a new user, please update your food preferences.")
        return redirect(url_for('account'))
    return redirect(url_for('index'))

    
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('id', None)
    return redirect(url_for('index'))

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    if request.method=='GET':
        foods = open('foods.txt').read()
        foodlist = foods.split('\n')
        food = ",".join(database.get_user_food_preferences(session['id']))
        return render_template("account.html",name=session['name'], foodlist=foodlist, preferences=food)
    else:
        preferences = request.form["what"]
        preflist = [str(x) for x in preferences[:-2].split(',')]
        database.update_user_food_preferences(session['id'],preflist)
        flash("Your food preferences have been updated.")
        return redirect(url_for('index'))

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
    fburl = "https://graph.facebook.com/v2.2/me/friends?access_token=" + urllib.quote_plus(str((session["token"])))
    req = urllib2.urlopen(fburl)
    result = req.read()
    d = json.loads(result)
    # a = open('sample.json').read()
    # d = json.loads(a)
    friendslist = d['data']
    if friendslist == []:
        friends = ["Justin Strauss","Lev Akabas","Dennis Nenov"]
        friendids = ["100001767295555","100001958141644","100000550963490"]
    else:
        friends = [str(x["name"]) for x in friendslist]
        friendids = [str(x["id"]) for x in friendslist]
    frienddict = []
    for x in range(0,len(friends)):
        frienddict.append((friends[x],friendids[x]))
    frienddict = dict(frienddict)
    # print frienddict['Dennis Nenov']
    if request.method=='GET':
        foods = open('foods.txt').read()
        foodlist = foods.split('\n')
        # print foodlist

        # print friendids
        food = database.get_user_food_preferences(session['id'])
        foodstr = ""
        for x in food:
            foodstr += x+","
        return render_template("create.html", friends=friends, foodlist=foodlist, food=foodstr)
    else:
        title = request.form['title']
        who = request.form['who']
        friendlist= [str(x) for x in who[:-2].split(',')]
        what = request.form['what']
        preflist = [str(x) for x in what[:-2].split(',')]
        where = request.form['where']
        if where[-7:].isdigit():
            where = urllib.unquote(reverse_geo(where)).decode('utf8').replace("+"," ")
        # print where
        date = request.form['date']
        thetime = request.form['thetime']
        friendlist = [frienddict[x.strip()] for x in friendlist]
        database.add_invite(title, session['id'], friendlist, preflist, where, thetime, date) 
        return redirect(url_for('index'))

@app.route('/respond/<chillid>', methods=['GET','POST'])
@login_required
def respond(chillid):
    ## prefs = db.gethostprefs(chillid)
    ## for example, it would return [["Breakfast & Brunch"],"40.720997499999996,-73.8477874","1/27/2015","11:30am"]
    ## host = db.gethost(chillid)
    ## host will return Justin Strauss
    ## title = db.gettitle(chillid)
    prefs = [["Breakfast & Brunch"],"69-50 Austin Street, Flushing, NY 11366, USA","1/27/2015","11:30am"]
    # if prefs[1][:1].isdigit():
    #     prefs[1] = urllib.unquote(reverse_geo(prefs[1])).decode('utf8').replace("+"," ")
    host = "Justin Strauss"
    title = "Brunch"
    if request.method=='GET':
        foods = open('foods.txt').read()
        foodlist = foods.split('\n')
        return render_template('respond.html',host=host, prefs=prefs, title=title, foodlist=foodlist)
    else:
        what = request.form['what']
        if what == "":
            what = prefs[0]
        where = request.form['where']
        if where == "":
            where = prefs[1]
        date = request.form['date']
        if date == "":
            date = prefs[2]
        thetime = request.form['thetime']
        if thetime == "":
            thetime = prefs[3]
        ## db.addresponse(chillid,session['id'],what,where,date,time)
        ## status = db.getstatus(chillid)
        ## get status returns true if none of the values in the dictionary are "pending", returns false otherwise
        #if status:
            ## whats = db.getwhats(chillid) -> a list of lists of food preferences ex. [['Brunch','Mexican'],['Brunch']]
            whats = [['Brunch','Mexican'],['Brunch']]
            ## wheres = db.getwheres(chillid) -> a list of the requested locations
            wheres = ["245 W 107th St New York, NY 10025","345 Chambers St, New York, NY 10282"]
            for x in range(0,len(wheres)):
                if not wheres[x][-7:].isdigit():
                    wheres[x] = geo_loc(wheres[x])
            #print wheres
            ## people = db.getpeople(chillid) -> gets the host and invitees
            restaurant_list = yelp.search(whats,wheres)
            # print restaurant_list
            # needsapproval = [db.gettitle(chillid), people, restaurant_list, datelist, timelist]
            ## db.setneedsapproval(chillid, needsapproval)
        return redirect(url_for('index'))

@app.route('/approve/<chillid>', methods=['GET','POST'])
@login_required
def approve(chillid):
    ## needsapproval = db.getneedsapproval(chillid)
    needsapproval = ['Party', ['Justin Strauss','Derek Tsui'], [{'website': u'http://www.yelp.com/biz/al-horno-lean-mexican-kitchen-new-york', 'name': u'Al Horno Lean Mexican Kitchen', 'rating_image': u'http://s3-media4.fl.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png', 'address': [u'417 W 47th St']}, {'website': u'http://www.yelp.com/biz/hells-kitchen-new-york-2', 'name': u"Hell's Kitchen", 'rating_image': u'http://s3-media4.fl.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png', 'address': [u'679 9th Ave']}, {'website': u'http://www.yelp.com/biz/taqueria-tehuitzingo-new-york', 'name': u'Taqueria Tehuitzingo', 'rating_image': u'http://s3-media4.fl.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png', 'address': [u'578 9th Ave']}, {'website': u'http://www.yelp.com/biz/ponche-taqueria-and-cantina-new-york', 'name': u'Ponche Taqueria & Cantina', 'rating_image': u'http://s3-media4.fl.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png', 'address': [u'420 W 49th St']}, {'website': u'http://www.yelp.com/biz/toloache-new-york-2', 'name': u'Toloache', 'rating_image': u'http://s3-media4.fl.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png', 'address': [u'251 W 50th St']}], ["1/27/2015","1/27/2015"], ['1:30pm','2:00pm']]
    # addresses = []
    # for x in range(0,4):
    #     addresses.append(str(needsapproval[2][x]['address'][0]))
    # print addresses
    if request.method=='GET':
        return render_template('approve.html', needsapproval=needsapproval, numtimes=len(needsapproval[3]))
    else:
        rest = request.form['restRadios']
        time = request.form['timeRadios']
        restaurantname = needsapproval[2][int(rest[-1:])]['name']
        restaurantaddress = needsapproval[2][int(rest[-1:])]['address'][0]
        finaldate = needsapproval[3][int(time[-1:])]
        finaltime = needsapproval[4][int(time[-1:])]
        # print restaurantname
        # print restaurantaddress
        # print finaldate
        # print finaltime
        # finalplan = [needsapproval[0], needsapproval[1], restaurantname, restaurantaddress, finaldate, finaltime]
        ## db.setfinalplan(chillid, finalplan)
        return redirect(url_for('index'))


def reverse_geo(latlong):
        googleurl = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s" % (latlong.split(",")[0], latlong.split(",")[1], 'AIzaSyBun2m9jaQTFGb0qtR7Shh7inqFhzKbLL4')
        request = urllib2.urlopen(googleurl)
        result = request.read()
        d = json.loads(result)
        rdic = d['results'][0]
        address = rdic['formatted_address']
        address = urllib.quote_plus(address)
        return address

def geo_loc(location):
#finds the longitude and latitude of a given location parameter using Google's Geocode API
#return format is a dictionary with longitude and latitude as keys
    loc = urllib.quote_plus(location)
    googleurl = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (loc,"AIzaSyBun2m9jaQTFGb0qtR7Shh7inqFhzKbLL4")
    request = urllib2.urlopen(googleurl)
    results = request.read()
    gd = json.loads(results) #dictionary
    result_dic = gd['results'][0] #dictionary which is the first element in the results list
    geometry = result_dic['geometry'] #geometry is another dictionary
    loc = geometry['location'] #yet another dictionary
    retstr = str(loc["lat"])+","+str(loc["lng"])
    return retstr

@app.route('/summary/<chillid>', methods=['GET','POST'])
@login_required
def summary(chillid):
    ## finalplan = db.getfinalplan(chillid)
    ## returns the final element of the chill list
    finalplan = ["Regents Week Lunch",["Justin Strauss","Dennis Nenov", "Lev Akabas"], "American Flatbread New York, NY", "205 Hudson Street, New York, NY 10013", "1/30/2015","3:00pm"]
    # print finalplan[3]
    imgurl = "https://www.google.com/maps/embed/v1/place?q="+finalplan[3]+"&key=AIzaSyBun2m9jaQTFGb0qtR7Shh7inqFhzKbLL4"
    if request.method=='GET':
        return render_template('summary.html', finalplan=finalplan, imgurl=imgurl, origin=None)
    else:
        origin = request.form['origin']
        return render_template('summary.html', finalplan=finalplan, imgurl=imgurl, origin=origin)

if __name__ == '__main__':
    app.run()
