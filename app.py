# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import db
from flask import Flask, render_template, request, redirect, session, url_for, flash
import urllib2, json, urllib
import yelp
#in the virtual env: $pip install facebook-sdk
import facebook

##FACEBOOK GRAPH API
client_id = "935483263159079"
client_secret = "ce39cb172d25891be741905badf002e9"
access_token  = "935483263159079|7EyHz4GRI92YiJxik2E-91MuW1o"

app = Flask(__name__)

def getID(token):
        graph = facebook.GraphAPI(token);
        return graph.get_object("me")["id"]

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
    # graph = facebook.GraphAPI(access_token)
    # profile = graph.get_object("me")
    # friends = graph.get_connections("me", "friends")
    # graph.put_object("me", "feed", message="I am writing on my wall!")
    if 'user' not in session:
        cookie = facebook.get_user_from_cookie(request.cookies, client_id, client_secret)
        print cookie
        if cookie != None:
            session["token"]= cookie["access_token"]
            session["user"]= getID(session["token"]);
            redirect("/");
        return render_template("index.html")
    return render_template("index.html")

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
