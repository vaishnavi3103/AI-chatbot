from pymongo import MongoClient
import os

# MongoDB client
MONGODB_URI = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI") or "mongodb://localhost:27017"
# Default DB name to 'chatbot' if not provided
DB_NAME = os.getenv("DB_NAME", "chatbot")
client = MongoClient(MONGODB_URI)

# Database
db = client[DB_NAME]

# HR department collection
hr_collection = db.get_collection("hr")

# Project department collection
project_collection = db.get_collection("projects")

# Chat history for session-based memory
chat_history = db.get_collection("chat_history")
