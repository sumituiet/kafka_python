# database.py
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Adjust if your MongoDB runs elsewhere
db = client["FaceDetectionDB"]                     # Database name
collection = db["DetectedFaces"]                   # Collection name

def insert_face_data(data):
    """
    Inserts face detection data into MongoDB.
    :param data: JSON data received from Kafka consumer.
    """
    if data:
        collection.insert_one(data)
        print("✅ Data inserted into MongoDB.")