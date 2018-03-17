import pymongo
from pymongo import MongoClient
myClinet = MongoClient()
db = myClinet["my_database"] # db name
users = db["users"]  # collections

#count()
db.users.find().count()

print(db.users.find().count())
#db.users.find({"username":"user01"}).count()
print(db.users.find({"username":"user01","password":"123"}).count())