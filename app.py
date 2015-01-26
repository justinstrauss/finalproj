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
FACEBOOK_APP_ID = '188477911223606'
FACEBOOK_APP_SECRET = '621413ddea2bcc5b2e83d42fc40495de'

client_id = "935483263159079"
client_secret = "ce39cb172d25891be741905badf002e9"
# access_token  = "935483263159079|7EyHz4GRI92YiJxik2E-91MuW1o"

app = Flask(__name__)
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
        return render_template("index.html", name=session['name'], id=session['id'], email=session['email'])

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
    session['email'] = me.data['email']
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
        request = urllib2.urlopen(fburl)
        result = request.read()
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
        where = request.form['where']
        when = request.form['when']
        date = request.form['date']
        thetime = request.form['thetime']
        print title
        print who
        print what
        print where
        print when
        print date
        print thetime

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
    db.setup()
    app.secret_key = "don't store this on github"
    app.debug = True
    app.run()
