# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import random, re, datetime, pymongo

connection = pymongo.Connection()

def setup():
	#default to test
	users = []
	#[name,id,email,food preferences[]]
	users.append(["Justin Strauss","100001767295555","justinianstrauss@gmail.com", ["American"], ["1"]])
	users.append(["Lev Akabas","100001958141644","lakabas15@gmail.com", ["Italian"], ["1"]])
	users.append(["Dennis Nenov","100000550963490", "nycdennen@gmail.com", ["Mexican"], []])

	dlist = []
	for i in range(len(users)):
		d = {'name':users[i][0],'id':users[i][1], 'email':users[i][2], 'food':users[i][3], 'chills':users[i][4]}
		dlist.append(d)
	db = connection['convenio']
	db.convenio.insert(dlist)


	db = connection['chills']
	db.chills.drop()

	chills = []
	# [name, id, chillersdict[], final plan]
	# chillers is a dictionary: keys are the id's of the users that are invited, value is "pending" if they haven't filled out the response form or if they have, it's a list of their preferences
	# preferences list [what, where, date, time]
	# first person in chillers dict is the host
	chills.append(["Regents Week Lunch","1",{"100001767295555":[["American","Mexican"],"Tribeca, New York, NY, United States","1/30/2015","3:00pm"],"100001958141644":"pending"}, []])

	dlist = []
	for i in range(len(chills)):
		d = {'name':chills[i][0],'id':chills[i][1], 'chillers':chills[i][2], 'finalplan':chills[i][3]}
		dlist.append(d)

	db.convenio.insert(dlist)


	# dlist = []
	# dlist.append({'title':'First post weee!', 'author':'derek', 'content':'I have just made my first post.','comments':[['First comment!','justin',[11,2,2014,23,20]]],'time':[11,2,2014,23,13], 'points':2})
	# dlist.append({'title':'Anybody know how to use MongoDB...', 'author':'justin', 'content':'I\'m having a little trouble with setting up MongoDB on my Mac.  Can anyone help','comments':[['I can!','derek',[11,2,2014,23,18]]],'time':[11,2,2014,23,14], 'points':2})
	# dlist.append({'title':'I like donuts.', 'author':'robbie', 'content':'...but I missed out on free donuts day.  Robbie sad.','comments':[['I like doughnuts too!','zamansky',[11,2,2014,23,21]]],'time':[11,2,2014,23,16], 'points':5})
	# dlist.append({'title':'Evil!!', 'author':'zamansky', 'content':'The pit of ultimate darkness. https://www.youtube.com/watch?v=LjoUUvEUFbY','comments':[['HECUBUS','robbie',[11,2,2014,23,21]]],'time':[11,2,2014,23,17], 'points':9})

	# db.convenio_blog.insert(dlist)


	# print "COLLECTION"
	# print(db.collection_names())
	# print "FIND"
	# res = db.convenio.find({},{"_id":False})
	# info = [x for x in res]
	# print info

# def authenticate(username,password):
# 	conn = Connection()
# 	db = conn['convenio']
# 	return 1 == (db.convenio.find({'name':username,'pw':password})).count()

def userexists(fbid):
	db = connection['convenio']
	return 1 == (db.convenio.find({'id':fbid})).count()

# def emailexists(email):
# 	conn = Connection()
# 	db = conn['convenio']
# 	return 1 == (db.convenio.find({'email':email})).count()

# def getcontacts(username):
# 	conn = Connection()
# 	db = conn['convenio']
# 	res = db.convenio.find({'name':{'$not':re.compile(username)}},{"_id":False})
# 	info = [x for x in res]
# 	return info

# def getblog(username):
# 	conn = Connection()
# 	db = conn['convenio_blog']
# 	res = db.convenio_blog.find({'name':{'$not':re.compile(username)}},{"_id":False})
# 	info = [x for x in res]
# 	return reversed(info)

# def getblogcontent(title):
# 	conn = Connection()
# 	db = conn['convenio_blog']
# 	res = db.convenio_blog.find({'title':title},{"_id":False})
# 	return res

def getprofile(fbid):
	db = connection['convenio']
	res = db.convenio.find({'id':fbid},{"_id":False})
	info = [x for x in res]
	return info

# def getposts(username):
# 	conn = Connection()
# 	db = conn['convenio_blog']
# 	res = db.convenio_blog.find({'author':username},{"_id":False})
# 	info = [x for x in res]
# 	return reversed(info)

# def updatepw(username,newpw):
# 	conn = Connection()
# 	db = conn['convenio']
# 	db.convenio.update({'name':username},{'$set':{'pw':newpw}})

def adduser(username,fbid,email):
	db = connection['convenio']
	db.convenio.insert([{'name':username,'id':fbid, 'email':email, 'food':[], "chills":[]}])

def getfood(fbid):
	return getprofile(fbid)[0]['food']

def updatefood(fbid, preflist):
	db = connection['convenio']
	db.convenio.update({'id':fbid},{'$set':{'food':preflist}})

def getchills(fbid):
	return getprofile(fbid)[0]['chills']


# def invalidpost(title, content):
# 	conn = Connection()
# 	db = conn['convenio_blog']
# 	valid = (0 == (db.convenio_blog.find({'title':title})).count())
# 	valid = valid and len(content) > 0 and len(title)>0

# 	return not(valid)

# def invalidcomment(comment):
# 	return len(comment)==0

# def addpost(title, username,content):
# 	conn = Connection()
# 	db = conn['convenio_blog']
# 	now = datetime.datetime.now()
# 	db.convenio_blog.insert([{'title':title,'author':username,'content':content, 'comments':[], 'time':[now.month,now.day,now.year,now.hour,now.minute]}])

# def addcomment(title, username,comment):
# 	conn = Connection()
# 	db = conn['convenio_blog']
# 	now = datetime.datetime.now()
# 	newcomment = [comment,username,[now.month,now.day,now.year,now.hour,now.minute]]
# 	print newcomment
# 	print title
# 	db.convenio_blog.update({'title':title},{'$push':{'comments':newcomment}})

# def votepost(title,points):
# 	conn = Connection()
# 	db = conn['convenio_blog']
# 	db.convenio_blog.update({'title':title},{'$inc':{'points':points}})


# if __name__ == '__main__':
# 	setup()
