#MongoDB storage
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
from logger import logger

load_dotenv()

client = MongoClient(
       os.getenv("MONGO_URI"),
       tls=True,
       tlsCAFile=certifi.where()
)

logger.info("Connected to MongoDB")

db = client["customer_reviews"]

reviews_collection = db["reviews"]
