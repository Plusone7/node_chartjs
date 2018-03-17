
import datetime
import pymongo
from pymongo import MongoClient
myClinet = MongoClient()
db = myClinet["my_database"] # db name
users = db["users"]  # collections

# date time
current_date = datetime.datetime.now()
old_date= datetime.datetime(2016,7,14)

# insert date time
users.insert({"username":"user","password":"2314","date":current_date})
