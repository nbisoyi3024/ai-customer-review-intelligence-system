#Business logic

from llm_analyzer import analyze_review
from vector_db import store_single_review
from logger import logger

def process_review(review):

    logger.info("Pipeline started")
    
    result = analyze_review(review)

    store_single_review(review)

    logger.info("Pipeline completed")
    return result