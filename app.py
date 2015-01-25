# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import db
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_oauth import OAuth
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
    if "name" not in session:
        session["name"] = None
    if "id" not in session:
        session['id'] = None
    if "token" not in session:
        session["token"] = None
    return render_template("index.html", name=session['name'], id=session['id'], token=session['token'])

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
    me = facebook.get('/me')
    session['name'] = me.data['name']
    session['id'] = me.data['id']
    session['token'] = (resp['access_token'])
    if not db.userexists(session['id']):
        db.adduser(session['name'],session['id'])
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

@app.route('/account')
def account():
    return render_template("account.html")

@app.route('/create', methods=['GET','POST'])
#@login_required
def create():
    if request.method=='GET':
        return render_template("create.html")
    search = request.form['activityEntry']
    cll = request.form['locationEntry']
    print cll
    session['search'] = search
    session['cll'] = cll
    if (cll == None or search == None):
        return render_template("index.html")
    else:
        return redirect(url_for('results'))

@app.route('/results')
def results():
    return yelp.search(session.pop('search',None),session.pop('cll',None))

if __name__ == '__main__':
        db.setup()
	app.secret_key = "don't store this on github"
	app.debug = True
	app.run(host='0.0.0.0')