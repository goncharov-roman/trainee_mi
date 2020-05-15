from pymongo import MongoClient


client = MongoClient('mongodb://Roman:1@db:27017/mydb') # localhost->db
db = client["mydb"]
db.coll.create_index("expire_at", expireAfterSeconds=0)
