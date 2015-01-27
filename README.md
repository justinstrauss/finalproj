Convenio: Convene with Convenience
=========
Software Development Fall Term Final Project
Visit our website: [http://convenio.chill.in/](http://convenio.chill.in/)
Watch our demo video: [https://www.youtube.com/user/justinianstrauss](https://www.youtube.com/user/justinianstrauss)

## About

Have you ever tried to meet up with your friends only to realize that it is just too much of a headache to decide on a mutual restaurant and time to meet up? With Convenio, you and your friends can now convene with convenience.

To get started, login into our website with your Facebook credentials. This allows us to connect you to your friends that also use the app. Don't worry, if none of your friends have joined us yet, you'll automatically be able to invite some of the app's creators, Justin, Lev, or Dennis. After logging in for the first time, remember to update your food preferences under the "My Account" tab.

The first step is to select "Create New Chill", which will allow you fill out some basic information about the event you want to host. You'll answer some of the classic who, what, where, when, and why questions, except it is implied that the answer to why is because you want to have fun with friends. WHO do you want to invite? WHAT type of food do you prefer? WHERE do you want to meet? WHEN do you want to meet? Don't worry, we've got your back, all of the fields except for the title of the chill itslef will autocomplete for convenience.

After creating the chill, the friends you invited will receive a notification on their dashboard.

## How to Run Locally

1. open up a terminal and type `$git clone git@github.com:justinstrauss/finalproj.git`
2. create a virtual environment (optional) and type `$pip install flask Flask-OAuth`
3. type `$python app.py` to run the app
4. go to [localhost:5000](localhost:5000) in your browser (Chrome is recommended)

## Tools Utilized

- [Python](https://www.python.org/) and [Flask](http://flask.pocoo.org/) for basic app backbone  
- [Flask-OAuth](https://pythonhosted.org/Flask-OAuth/) for easy Facebook login within the microframework  
- [Login Required Decorator](http://flask.pocoo.org/docs/0.10/patterns/viewdecorators/) for easy authentication
- [Pure CSS](http://purecss.io/) for CSS styling  
- [List Comprehensions](https://docs.python.org/2/tutorial/datastructures.html) for code simplicity  
- [Digital Ocean](https://www.digitalocean.com/) for droplet deployment  
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api) for connecting with friends  
- [Yelp API](http://www.yelp.com/developers/documentation) for restaurant searches  
- [Google Maps API](https://developers.google.com/maps/) for directions and geolocation  
- [JQuery](http://jquery.com/) for interactive form widgets  
- [SQLite](http://www.sqlite.org/) for database storage  
- [Google Places](https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete) for location autocompletion  

## Contributors
[Lev Akabas](https://github.com/levakabas): Analytics, Back End  
[Dennis Nenov](https://github.com/DennisNenov): Code Reviewer, Workflow  
[Justin Strauss](https://github.com/justinstrauss): Project Manager, Back End  
[Derek Tsui](https://github.com/d-tsui): Front End, Styling  

## Timeline
- [X] 12/19: finalize project idea (all)
- [X] 12/24 - 1/4: finish college apps (Justin and Dennis) and work on project during free time (Lev and Derek) during winter break  
- [X] 1/5: get login with Facebook working (Derek)
- [X] 1/7: deploy Digital Ocean droplet (Justin)
- [X] 1/9: move Facebook login from separate page to menu bar (Justin)
- [ ] 1/11: integrate Yelp API (Lev)
- [X] 1/13: geolocation added (Justin)
- [X] 1/15: finish basic front end UI (Derek)
- [X] 1/17: layout "create new chill" form (Dennis)
- [ ] 1/19: integrate directions - Google Maps walking transit biking drive, Citibike, Uber (Justin, Derek)
- [ ] 1/25: complete front page integration
- [ ] 1/27: fin  
