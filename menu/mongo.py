from pymongo import MongoClient

client = MongoClient("mongodb+srv://nopan_db:lilo123@cluster0.unbki7s.mongodb.net/?appName=Cluster0")
db = client["quickbite_db"]
menu_collection = db["menus"]