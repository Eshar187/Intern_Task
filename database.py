from pymongo import MongoClient
from test import DB_URL

client = MongoClient(DB_URL)

db = client.student
collection = db.registrations