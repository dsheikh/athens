'''
Copyright 2016 @danyal

Stream listener on public tweets based on parameters.
Listener will then store tweets into a database for
further parsing and storage.
'''

'''
Using birdy library for python-twitter interface
'''
from birdy.twitter import StreamClient
from pymongo import MongoClient

client = StreamClient('consumer_key',
    'consumer_secret',
    'access_token',
    'access_secret')

'''
Connecting to mongodb and setting up a client interface
'''
mclient = MongoClient()
db = mclient['test_db']

response = client.stream.statuses.filter.post(track='olympics')

'''
Iterates over the data returned in the response stream
and stores it into the mongodb database for parsing
'''
for data in response.stream():
    db.posts.insert_one(data)
