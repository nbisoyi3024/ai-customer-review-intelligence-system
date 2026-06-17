#FastAPI app for customer review analysis
import time
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from backend.logger import logger

from backend.llm_analyzer import analyze_review
from backend.mongo_db import reviews_collection
from backend.vector_db import store_single_review


app = FastAPI()

# Logging
logger.info("API initialized")

# Request schema/receive review
class ReviewRequest(BaseModel):
    review: str

# Endpoints
@app.get("/")
def home():
    return {"message": "Customer Review Intelligence API"}

@app.get("/health")
def health():
    return {"status": "ok"}

# API endpoint
@app.post("/analyze")
def analyze(req: ReviewRequest):

    try:
         logger.info("Analyzing review")

         # Analyze review using LLM(openAI)
         result = analyze_review(req.review)

        ## Save result to MongoDB
         result["review"] = req.review
         
         reviews_collection.insert_one(result)

         # Store embedding to ChromaDB
         store_single_review(req.review)
         
         logger.info("Review analyzed successfully")
         #return json
         return {
             "sentiment": result.get("sentiment"),
             "summary": result.get("summary"),
             "review": req.review
         }
    #handle errors gracefully
    except Exception as e:

        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Analysis failed")

#top 10 reviews endpoint   
@app.get("/reviews/top10")
def get_top10_reviews():
    reviews = list(reviews_collection.find())
    categories = [r.get("category", "unknown").lower() for r in reviews]
    category_counts = {c: categories.count(c) for c in set(categories)}
    return {"total_reviews": len(reviews), "category_counts": category_counts}