# Justin Strauss, Lev Akabas, Derek Tsui, Dennis Nenov
# Software Development Period 7
# Final Project

import sqlite3, hashlib

def create_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("create table users (name text, facebook_id text)")
    c.execute("create table userprefmatch(preference text, facebook_id text)")
    c.execute("create table inviteprefmatch(invite_id text, facebook_id text, food_pref text)")
    c.execute("create table userinvitematch(invite_id text, facebook_id text, location_pref text, time_pref text, date_pref text)")
    c.execute("create table invites(invite_id text, real_id integer, title text, creator_id text, final_location text, final_time text, final_date text)")    
    conn.commit()
    conn.close()


def invite_friends(invite_id, listOfFriends):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    for friend in listOfFriends:
        command = "INSERT INTO userinvitematch(invite_id, facebook_id, location_pref, time_pref, date_pref) VALUES('" + invite_id + "','" + str(friend) + "','None','None','None')"
        c.execute(command)
    conn.commit()
    conn.close()

def add_food_preferences(invite_id, user_id, list_of_preferences):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    for foodPref in list_of_preferences:
        command = "INSERT INTO inviteprefmatch(invite_id, facebook_id, food_pref) VALUES('" + invite_id + "','" + str(user_id) + "','" + foodPref  + "')"
        c.execute(command)
    conn.commit()
    conn.close()

def add_setting_preferences(invite_id, user_id, location, time, date):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    command = "update userinvitematch set location_pref='"+ location + "', time_pref='" + time + "', date_pref='" + date + "' where invite_id=='" + invite_id +"' and facebook_id=='" + user_id + "'"
    c.execute(command)
    conn.commit()
    conn.close()
    
def add_invite(title, creator_id, list_of_friends, list_of_preferences, location, time, date):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    currentMax = c.execute("select max(real_id) from invites").fetchone()
    if currentMax[0] == None:
        newid = 1
    else:
       newid = int(currentMax[0]) + 1
    newInviteID = hashlib.sha512(str(newid)).hexdigest()
    command = "INSERT INTO invites(invite_id, real_id, creator_id, title, final_location, final_time, final_date) VALUES('" + str(newInviteID) + "','" + str(newid) + "','" + str(creator_id) + "','" + str(title) + "','None','None','None')"
    c.execute(command)
    conn.commit()
    conn.close()
    list_of_friends.append(creator_id)
    invite_friends(str(newInviteID),list_of_friends)
    add_food_preferences(str(newInviteID),creator_id, list_of_preferences)
    add_setting_preferences(str(newInviteID),creator_id, location, time, date)

def test():
    #create_db()
    #add_invite("Test Chill", "Dennis", ["Lev", "Justin"],["Tacos", "Pizza"], "NYC", "11:00am", "12/13/15")    
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM invites")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM userinvitematch")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM inviteprefmatch")
    print(cursor.fetchall())

test()

##def add_post(title, content, author, database_id):
##    conn = sqlite3.connect("database.db")
##    c = conn.cursor()
##    currentMax = c.execute("select max(post_id) from post").fetchone()
##    if currentMax[0] == None:
##        newid = 1
##    else:
##       newid = int(currentMax[0]) + 1
##    command = "INSERT INTO post(title, content, author, database_id, post_id) VALUES('" + title + "','" + content + "','" + author + "','" + str(database_id) + "','" + str(newid) +  "')"
##    c.execute(command)
##    conn.commit()
##    conn.close()
##    
##def database_list():
##    conn = sqlite3.connect("database.db")
##    c = conn.cursor()
##    databases = []
##    for row in c.execute("select name, database_id from database"):
##        databases.append([row[0],row[1]])
##    return databases
##
##def post_list(databaseid):
##    conn = sqlite3.connect("database.db")
##    c = conn.cursor()
##    posts = []
##    for row in c.execute("select title,  author, post_id from post where database_id==" + str(databaseid)):
##        posts.append([row[0],row[1],row[2]])
##    return posts
##
##def get_post(postid, databaseid):
##    conn = sqlite3.connect("database.db")
##    c = conn.cursor()
##    post_dict = {}
##    command = """
##    SELECT title, content, author
##    FROM post
##    WHERE database_id==""" + str(databaseid) + """ and post_id==""" + str(postid)
##    for post in c.execute(command):
##        post_dict['title'] = post[0]
##        post_dict['author'] = post[2]
##        post_dict['content'] = post[1]
##    return post_dict

