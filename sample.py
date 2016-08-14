'''
Copyright 2016 @danyal

Stream listener on public tweets based on parameters.
Listener will then store tweets into a database for
further parsing and storage.
'''

import json

'''
Using birdy library for python-twitter interface
'''
from birdy.twitter import StreamClient
from pymongo import MongoClient

'''
Open prefs file with stored parameters and load file
'''
prefs_file = open('prefs')
prefs = json.load(prefs_file)
prefs_file.close()

'''
Initialize streaming client with prefs
'''
tokens = prefs['tokens']
client = StreamClient(str(tokens['consumer_key']),
    str(tokens['consumer_secret']),
    str(tokens['access_token']),
    str(tokens['access_secret']))

'''
Connecting to mongodb and setting up a client interface
'''
mclient = MongoClient()
db_name = str(prefs['mongo']['db_name'])
db = mclient[db_name]

'''
Begin tracking using tracking expression provided in prefs
'''
track_exp = str(prefs['track_exp'])
response = client.stream.statuses.filter.post(track=track_exp)

'''
Iterates over the data returned in the response stream
and stores the data into a mongodb database for parsing
'''
for data in response.stream():
    db.posts.insert_one(data)
