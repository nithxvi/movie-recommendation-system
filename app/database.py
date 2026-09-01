import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL is not set")

if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME is not set")


client = MongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=5000
)

try:
    client.admin.command("ping")
    print("Successfully connected to MongoDB!")
except Exception as e:
    print("MongoDB connection failed:", e)
    raise


db = client[DATABASE_NAME]

users_collection = db["users"]
interactions_collection = db["interactions"]
recommendations_collection = db["recommendations"]