# app/models.py
import os
from pymongo import MongoClient

# Get Mongo URI from environment variable
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable is not set")

# Initialize MongoDB client
mongo_client = MongoClient(mongo_uri)
