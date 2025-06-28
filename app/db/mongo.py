from pymongo import MongoClient

def init_mongo(app):
    client = MongoClient("mongodb://localhost:27017/")
    app.mongo_client = client
    app.mongo_db = client["gaming"]

