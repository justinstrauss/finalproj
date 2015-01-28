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

##FACEBOOK GRAPH API
FACEBOOK_APP_ID = "935483263159079"
FACEBOOK_APP_SECRET = "ce39cb172d25891be741905badf002e9"

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
    request_token_params={'scope': 'user_friends'}
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
    fburl = "https://graph.facebook.com/v2.2/me?access_token=" + urllib.quote_plus(str((session["token"])))
    req = urllib2.urlopen(fburl)
    result = req.read()
    d = json.loads(result)
    # a = open('sample.json').read()
    # d = json.loads(a)
    session['id'] = d['id']
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
    session.pop('token', None)
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
        friends = []
        friendids = []
    else:
        friends = [str(x["name"]) for x in friendslist]
        friendids = [str(x["id"]) for x in friendslist]
    frienddict = []
    for x in range(0,len(friends)):
        frienddict.append((friends[x],friendids[x]))
    frienddict = dict(frienddict)
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
        what = request.form['what']
        preflist = [str(x) for x in what[:-2].split(',')]
        where = request.form['where']
        if where[-7:].isdigit():
            where = urllib.unquote(reverse_geo(where)).decode('utf8').replace("+"," ")
        # print where
        date = request.form['date']
        thetime = request.form['thetime']
        friendlist = [frienddict[x.strip()] for x in friends]
        database.add_invite(title, session['id'], friendlist, preflist, where, thetime, date) 
        return redirect(url_for('index'))

@app.route('/respond/<chillid>', methods=['GET','POST'])
@login_required
def respond(chillid):
    prefDict = database.get_host_preferences(chillid)
    prefs = [prefDict['food'],prefDict['location'], prefDict['date'], prefDict['time']]
    # if prefs[1][:1].isdigit():
    #     prefs[1] = urllib.unquote(reverse_geo(prefs[1])).decode('utf8').replace("+"," ")
    host = database.get_host_name(chillid)
    title = database.get_invite_title(chillid)
    if request.method=='GET':
        foods = open('foods.txt').read()
        foodlist = foods.split('\n')
        return render_template('respond.html',host=host, prefs=prefs, title=title, foodlist=foodlist)
    else:
        what = request.form['what']
        what = [str(x) for x in what[:-2].split(',')]
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
        database.add_user_preferences(chillid,session['id'],where,thetime,date,what)
        return redirect(url_for('index'))

@app.route('/approve/<chillid>', methods=['GET','POST'])
@login_required
def approve(chillid):
    whats = database.get_invite_food_preference(chillid)
    invitePref = database.get_invite_preferences(chillid)
    wheres = invitePref['location']
    for x in range(0,len(wheres)):
        if not wheres[x][-7:].isdigit():
            wheres[x] = geo_loc(wheres[x])
    people = database.get_invitees(chillid)
    restaurant_list = yelp.search(whats,wheres)
    datelist = invitePref['date']
    timelist = invitePref['time']
    needsapproval = [database.get_invite_title(chillid), people, restaurant_list, datelist, timelist]
    if request.method=='GET':
        return render_template('approve.html', needsapproval=needsapproval, numtimes=len(needsapproval[3]))
    else:
        rest = request.form['restRadios']
        time = request.form['timeRadios']
        restaurantname = needsapproval[2][int(rest[-1:])]['name']
        restaurantaddress = needsapproval[2][int(rest[-1:])]['address'][0]
        finaldate = needsapproval[3][int(time[-1:])]
        finaltime = needsapproval[4][int(time[-1:])]
        database.set_final_plan(chillid, restaurantaddress, finaltime, finaldate)
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
    finalplanDict = database.get_invite_dict(chillid)
    inviteeList = database.get_invitees(chillid)
    finalplan = [finalplanDict['title'], inviteeList, finalPlanDict['location'], finalPlanDict['date'], finalPlanDict['time']]
    imgurl = "https://www.google.com/maps/embed/v1/place?q="+finalplan[3]+"&key=AIzaSyBun2m9jaQTFGb0qtR7Shh7inqFhzKbLL4"
    if request.method=='GET':
        return render_template('summary.html', finalplan=finalplan, imgurl=imgurl, origin=None)
    else:
        origin = request.form['origin']
        return render_template('summary.html', finalplan=finalplan, imgurl=imgurl, origin=origin)

if __name__ == '__main__':
    app.run()
