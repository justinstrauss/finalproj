# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import db
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
db.setup()
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
    if "id" not in session:
        session["name"] = None
        session['id'] = None
        session['email'] = None
        return render_template("about.html")
    else:
        ## pending = db.findpending(session['id'])
        ## returns a dictionary of pending chills for that user, keys are titles, values are chill id's
        ## ready = db.findready(session['id'])
        ## returns a dictionary of ready chills for that user, keys are titles, values are chill id's
        pending = {"Brunch":"2"}
        ready = {"Regents Week Lunch":"1"}
        # print pending['Brunch']
        # print ready
        return render_template("index.html", pending=pending, ready=ready)

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
    print me.data
    session['name'] = me.data['name']
    session['id'] = me.data['id']
    # session['email'] = me.data['email']
    return redirect(url_for('index'))
    
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    if request.method=='GET':
        foods = open('foods.txt').read()
        foodlist = foods.split('\n')
        food = db.getfood(session['id'])
        return render_template("account.html",name=session['name'], email=session["email"], foodlist=foodlist, preferences=food)
    else:
        preferences = request.form["what"]
        preflist = [str(x) for x in preferences[:-2].split(',')]
        # print preflist
        db.updatefood(session['id'],preflist)
        flash("Your food preferences have been updated.")
        return redirect(url_for('index'))

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method=='GET':
        foods = open('foods.txt').read()
        foodlist = foods.split('\n')
        # print foodlist

        fburl = "https://graph.facebook.com/v2.2/me/friends?access_token=" + urllib.quote_plus(str((session["token"])))
        print fburl
        req = urllib2.urlopen(fburl)
        result = req.read()
        d = json.loads(result)
        # a = open('sample.json').read()
        # d = json.loads(a)
        friendslist = d['data']
        friends = [str(x["name"]) for x in friendslist]
        # print friends
        return render_template("create.html", friends=friends, foodlist=foodlist)
    else:
        title = request.form['title']
        who = request.form['who']
        what = request.form['what']
        if what == "":
            what = db.getfood(session['id'])
        where = request.form['where']
        if where[:1].isdigit():
            where = urllib.unquote(reverse_geo(where)).decode('utf8').replace("+"," ")
        date = request.form['date']
        thetime = request.form['thetime']
        # Brunch
        # Lev Akabas, Dennis Nenov, 
        # Breakfast & Brunch, 
        # 40.720997499999996,-73.8477874
        # 01/27/2015
        # 11:30am
        ##db.addchill(session['id'], title, who, what, where, date, time)
        ##chills.append(["Brunch","2",{"100001767295555":[["Breakfast & Brunch"],"40.720997499999996,-73.8477874","1/27/2015","11:30am"],"100001958141644":"pending", "100000550963490":"pending"}, []])
        ##adds chill to the chill database table, 2nd element id is chill.length+1
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
        return render_template('respond.html',host=host, prefs=prefs, title=title)
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
            ## wheres = db.getwheres(chillid) -> a list of the requested locations
            ## people = db.getpeople(chillid) -> gets the host and invitees
            ## restaurant_list = yelp.search(whats,wheres)

            ## Something here taking the list of suggestions and picking one
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

@app.route('/summary/<chillid>', methods=['GET','POST'])
@login_required
def summary(chillid):
    ## finalplan = db.getfinalplan(chillid)
    ## returns the final element of the chill list
    finalplan = ["Regents Week Lunch",["Justin Strauss","Dennis Nenov", "Lev Akabas"], "American Flatbread New York, NY", "205 Hudson Street, New York, NY 10013", "1/30/2015","3:00pm"]
    imgurl = "https://www.google.com/maps/embed/v1/place?q="+finalplan[3]+"&key=AIzaSyBun2m9jaQTFGb0qtR7Shh7inqFhzKbLL4"
    if request.method=='GET':
        return render_template('summary.html', finalplan=finalplan, imgurl=imgurl, origin=None)
    else:
        origin = request.form['origin']
        return render_template('summary.html', finalplan=finalplan, imgurl=imgurl, origin=origin)

# @app.route('/create', methods=['GET','POST'])
# #@login_required
# def create():
#     if request.method=='GET':
#         return render_template("create.html")
#     search = request.form['activityEntry']
#     cll = request.form['locationEntry']
#     print cll
#     session['search'] = search
#     session['cll'] = cll
#     if (cll == None or search == None):
#         return render_template("index.html")
#     else:
#         return redirect(url_for('results'))

# @app.route('/results')
# def results():
#     return yelp.search(session.pop('search',None),session.pop('cll',None))

if __name__ == '__main__':
    app.run()
