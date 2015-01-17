# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import random, re, datetime
from pymongo import Connection

def setup():
	conn = Connection()
	db = conn['convenio']
	db.convenio.drop()

	#default to test
	users = []
	#[name,email,password]
	users.append(["justin","justin@example.com","test"])
	users.append(["derek","derek@example.com","test"])
	users.append(["lev","lev@example.com","test"])
	users.append(["dennis","dennis@example.com","test"])

	dlist = []
	for i in range(len(users)):
		d = {'name':users[i][0],'email':users[i][1],'pw':users[i][2]}
		dlist.append(d)

	db.convenio.insert(dlist)


	# db = conn['convenio_blog']
	# db.convenio_blog.drop()

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

def authenticate(username,password):
	conn = Connection()
	db = conn['convenio']
	return 1 == (db.convenio.find({'name':username,'pw':password})).count()

def userexists(username):
	conn = Connection()
	db = conn['convenio']
	return 1 == (db.convenio.find({'name':username})).count()

def emailexists(email):
	conn = Connection()
	db = conn['convenio']
	return 1 == (db.convenio.find({'email':email})).count()

def getcontacts(username):
	conn = Connection()
	db = conn['convenio']
	res = db.convenio.find({'name':{'$not':re.compile(username)}},{"_id":False})
	info = [x for x in res]
	return info

def getblog(username):
	conn = Connection()
	db = conn['convenio_blog']
	res = db.convenio_blog.find({'name':{'$not':re.compile(username)}},{"_id":False})
	info = [x for x in res]
	return reversed(info)

def getblogcontent(title):
	conn = Connection()
	db = conn['convenio_blog']
	res = db.convenio_blog.find({'title':title},{"_id":False})
	return res

def getprofile(username):
	conn = Connection()
	db = conn['convenio']
	res = db.convenio.find({'name':username},{"_id":False})
	info = [x for x in res]
	return info

def getposts(username):
	conn = Connection()
	db = conn['convenio_blog']
	res = db.convenio_blog.find({'author':username},{"_id":False})
	info = [x for x in res]
	return reversed(info)

def updatepw(username,newpw):
	conn = Connection()
	db = conn['convenio']
	db.convenio.update({'name':username},{'$set':{'pw':newpw}})

def adduser(username,email,password):
	conn = Connection()
	db = conn['convenio']
	db.convenio.insert([{'name':username,'email':email,'pw':password}])

def invalidpost(title, content):
	conn = Connection()
	db = conn['convenio_blog']
	valid = (0 == (db.convenio_blog.find({'title':title})).count())
	valid = valid and len(content) > 0 and len(title)>0

	return not(valid)

def invalidcomment(comment):
	return len(comment)==0

def addpost(title, username,content):
	conn = Connection()
	db = conn['convenio_blog']
	now = datetime.datetime.now()
	db.convenio_blog.insert([{'title':title,'author':username,'content':content, 'comments':[], 'time':[now.month,now.day,now.year,now.hour,now.minute]}])

def addcomment(title, username,comment):
	conn = Connection()
	db = conn['convenio_blog']
	now = datetime.datetime.now()
	newcomment = [comment,username,[now.month,now.day,now.year,now.hour,now.minute]]
	print newcomment
	print title
	db.convenio_blog.update({'title':title},{'$push':{'comments':newcomment}})

def votepost(title,points):
	conn = Connection()
	db = conn['convenio_blog']
	db.convenio_blog.update({'title':title},{'$inc':{'points':points}})


# if __name__ == '__main__':
# 	setup()