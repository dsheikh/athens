'''
Copyright 2016 @danyal

Parser to clean data and create a list of places
'''
import json
import pymongo
import operator
from pymongo import MongoClient

'''
Open prefs file with stored parameters and load file
'''
prefs_file = open('prefs')
prefs = json.load(prefs_file)
prefs_file.close()

mclient = MongoClient()
db_name = str(prefs['mongodb']['db_name'])
db = mclient[db_name]
