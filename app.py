# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

from flask import Flask, render_template, request, redirect, session, url_for, flash
import urllib2, json, urllib

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/oauth2callback')
def oauth2callback():
	return

if __name__ == '__main__':
	app.secret_key = "don't store this on github"
	app.debug = True
	app.run(host='0.0.0.0')