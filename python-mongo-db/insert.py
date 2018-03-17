
import pymongo
from pymongo import MongoClient
myClinet = MongoClient()
db = myClinet["my_database"] # db name
users = db["users"]  # collections
user1 = {'username':"nick","password":"password","favorite_num":"32","hobbies":["python","games","pizza"]}
user_id = users.insert_one(user1).inserted_id
print(user_id)
# insert multiUser

multiuser = [{'username':"user01","password":"000","favorite_num":"1"},
    {'username':"user02","password":"123","favorite_num":"2"},
    {'username':"user03","password":"456","favorite_num":"3"},
    {'username':"user04","password":"789","favorite_num":"4"},
    {'username':"user05","password":"1112","favorite_num":"5"},
    {'username':"user06","password":"1314","favorite_num":"6"}]
user_id = users.insert_many(multiuser).inserted_ids