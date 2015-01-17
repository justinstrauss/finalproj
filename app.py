# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import db
from flask import Flask, render_template, request, redirect, session, url_for, flash
import urllib2, json, urllib

app = Flask(__name__)

secrets = json.load(open("secrets.json"))

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
    return render_template("index.html")

@app.route('/login')
def login():
    url="https://www.facebook.com/dialog/oauth"
    data = urllib.urlencode(secrets['request_redirect'])
    req = urllib2.Request(url+"?"+data)
    response = urllib2.urlopen(req)
    result = response.read()
    return result

@app.route("/oauth2callback")
def oauth2callback():
    if request.args.has_key('error'):
        return "ERROR"

    url = "https://www.facebook.com/connect/login_success.html"
    code = request.args.get('code')
    values = secrets['request_token']
    values['code'] = code

    data = urllib.urlencode(values)
    req = urllib2.Request(url,data)
    response = urllib2.urlopen(req)
    rawresult = response.read()
    d = json.loads(rawresult)
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo?id_token=%s"%(d['id_token'])
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    rawresult = response.read()
    d = json.loads(rawresult)
    session['user']=d['email']
    return redirect("/")

@app.route('/account')
def account():
    return render_template("account.html")

@app.route('/create')
#@login_required
def create():
	return render_template("create.html")

if __name__ == '__main__':
        db.setup()
	app.secret_key = "don't store this on github"
	app.debug = True
	app.run(host='0.0.0.0')
