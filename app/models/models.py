from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://mlinami:fLPbruwOJD2tvR0h@basigo.fkhuf.mongodb.net/?retryWrites=true&w=majority&appName=BasiGo"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Ping the MongoDB server to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. Successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Export the client
mongo_client = client
