#Replace <password> with the password for the root_user user. Replace myFirstDatabase with the name of the database that connections will use by default.
uri = "mongodb+srv://root_user:root_user@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"

#from pymongo import MongoClient
import pymongo

client = pymongo.MongoClient(uri)

db = client.movies

print(db)