from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure MongoDB using environment variables
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/")
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "resume_challenge")



client = MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DATABASE_NAME]
collection = db["views"]

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "This is a dummy response"})

@app.route('/GetResumeCounter', methods=['GET'])
def get_and_increment_views():
    # Retrieve the current view count
    view_item = collection.find_one({"id": "0"})
    
    if view_item:
        views = view_item['views']
    else:
        views = 0
        collection.insert_one({"id": "0", "views": views})

    # Increment the view count
    views += 1
    collection.update_one({"id": "0"}, {"$set": {"views": views}})
    
    return jsonify({"count": views})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
