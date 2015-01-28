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

def add_user_preferences(invite_id, user_id, location, time, date, list_of_preferences):
    add_food_preferences(invite_id, user_id, list_of_preferences)
    add_setting_preferences(invite_id,user_id, location, time, date)
 
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
    add_user_preferences(str(newInviteID), creator_id, location, time, date, list_of_preferences)

def get_invite_food_preferences_dict(invite_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    masterdict = {}
    for row in c.execute("select facebook_id, food_pref from inviteprefmatch where invite_id=='"+ invite_id +"'"):
        if row[0] in masterdict:
            masterdict[row[0]].append(row[1])
        else:
            masterdict[row[0]] = [row[1]]
    conn.commit()
    conn.close()
    return masterdict

def get_invite_food_preferences(invite_id):
    masterdict = get_invite_food_preferences_dict(invite_id)
    masterlist = []
    for key in masterdict.keys():
        masterlist.append(masterdict[key])
    return masterlist

def get_invite_preferences(invite_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    masterdict = {}
    masterdict['location'] = []
    masterdict['time'] = []
    masterdict['date'] = []
    for row in c.execute("select location_pref, date_pref, time_pref from userinvitematch where invite_id=='"+ invite_id +"'"):
        masterdict['location'].append(row[0])
        masterdict['time'].append(row[2])
        masterdict['date'].append(row[1])
    conn.commit()
    conn.close()
    return masterdict

def get_invitees(invite_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    masterlist = []
    for row in c.execute("select facebook_id from userinvitematch where invite_id=='"+ invite_id +"'"):
        masterlist.append(row[0])
    conn.commit()
    conn.close()
    return masterlist

#returns true if everyone responded
def see_if_everyone_responded(invite_id):
    listToScan = get_invite_preferences(invite_id)['location']
    for item in listToScan:
        if item == "None":
            return False
    return True

#returns true if the invite is finalized--i.e. the owner picked a location
def see_if_finalized(invite_id):
    dictToScan = get_invite_dict(invite_id)
    for key in dictToScan.keys():
        if dictToScan[key] == "None":
            return False
    return True

def get_invite_dict(invite_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    masterdict = {}
    for row in c.execute("select title, creator_id, final_location, final_time, final_date from invites where invite_id=='"+ invite_id +"'"):
        masterdict['title'] = row[0]
        masterdict['creator_id'] = row[1]
        masterdict['location'] = row[2]
        masterdict['time'] = row[3]
        masterdict['date'] = row[4]
    conn.commit()
    conn.close()
    return masterdict

def get_invite_title(invite_id):
    return get_invite_dict(invite_id)['title']
                            
def set_final_plan(invite_id, location, time, date):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    command = "update invites set final_location='"+ location + "', final_time='" + time + "', final_date='" + date + "' where invite_id=='" + invite_id +"'"
    c.execute(command)
    conn.commit()
    conn.close()

def get_user_name(facebook_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    for row in c.execute("select name from users where facebook_id=='"+ facebook_id +"'"):
        return row[0]

def get_host_id(invite_id):
    return get_invite_dict(invite_id)['creator_id']

def get_host_name(invite_id):
    return get_user_name(get_host_id(invite_id))

def get_host_food_preferences(invite_id):
    return get_invite_food_preferences_dict(invite_id)[get_host_id(invite_id)]

def get_host_preferences(invite_id):
    host_id = get_host_id(invite_id)
    masterdict = {}
    masterdict['food'] = get_host_food_preferences(invite_id)
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    for row in c.execute("select location_pref, time_pref, date_pref from userinvitematch where invite_id=='" + invite_id +"' and facebook_id=='" + host_id + "'"):
        masterdict['location'] = row[0]
        masterdict['time'] = row[1]
        masterdict['date'] = row[2]
    conn.commit()
    conn.close()
    return masterdict

def get_user_food_preferences(facebook_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    masterlist = []
    for row in c.execute("select preference from userprefmatch where facebook_id=='" + facebook_id + "'"):
        masterlist.append(row[0])
    conn.commit()
    conn.close()
    return masterlist

def update_user_food_preferences(facebook_id, list_of_preferences):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("delete from userprefmatch where facebook_id=='" + facebook_id + "'")    
    for foodPref in list_of_preferences:
        command = "INSERT INTO userprefmatch(facebook_id, preference) VALUES('" + str(facebook_id) + "','" + str(foodPref) + "')"
        c.execute(command)
    conn.commit()
    conn.close()

#returns true if the user exists
def user_exists(facebook_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    command = "SELECT COUNT(*) FROM users where facebook_id=='" + facebook_id + "'"
    for row in c.execute(command):
        count = row[0]
    conn.commit()
    conn.close()
    return count > 0
    

def add_user(name, facebook_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    command = "INSERT INTO users(facebook_id, name) VALUES('" + str(facebook_id) + "','" + str(name) + "')"
    c.execute(command)
    conn.commit()
    conn.close()

def get_invites_for_user(facebook_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    masterdict = {}
    masterdict['pending'] = {}
    masterdict['ready'] = {}
    masterdict['needsapproval'] = {}
    for row in c.execute("select invite_id from userinvitematch where facebook_id=='" + facebook_id + "'"):
        invite_title = get_invite_title(row[0])
        invite_id = row[0]
        package = [invite_id, invite_title]
        if (see_if_finalized(invite_id)):
            masterdict['ready'][invite_title] = invite_id
        elif (see_if_everyone_responded(invite_id)):
            masterdict['needsapproval'][invite_title] = invite_id
        else:
            masterdict['pending'][invite_title] = invite_id
    conn.commit()
    conn.close()
    return masterdict

def test():
    #create_db()
    #add_invite("Test Chill", "100001767295555", ["100000550963490"],["Tacos", "Pizza"], "NYC", "11:00am", "12/13/15")
    #print get_invites_for_user("100000550963490")['pending']['Test Chill']
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM invites")
    print(cursor.fetchall())
    print ""
    print ""
    cursor.execute("SELECT * FROM userinvitematch")
    print(cursor.fetchall())
    print ""
    print ""
    cursor.execute("SELECT * FROM inviteprefmatch")
    print(cursor.fetchall())
    print ""
    print ""
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
    print ""
    print ""

#test()
