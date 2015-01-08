# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

from flask import Flask, render_template, request, redirect, session, url_for, flash
import urllib2, json, urllib

app = Flask(__name__)

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

@app.route('/account')
def account():
    return render_template("account.html")

@app.route('/create')
#@login_required
def create():
	return render_template("create.html")

if __name__ == '__main__':
	app.secret_key = "don't store this on github"
	app.debug = True
	app.run(host='0.0.0.0')