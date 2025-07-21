from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    db = client["campus_club"]
    return db