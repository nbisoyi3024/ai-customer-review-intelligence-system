#LLM analysis
import os
import time
import json
from dotenv import load_dotenv
from openai import OpenAI
from logger import logger


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_review(review):

    prompt = f"""
        Analyze this customer review:

        Review:
       {review}

       Return ONLY valid JSON. 
       
       {{ 
       "sentiment": "", 
       "summary": "", "issues": [], 
       "category": "", 
       "recommendation": "" 
       }} 
     """
    #------Input validation------
    if not review:
          raise ValueError("Review cannot be empty")
    
    logger.info("Starting review analysis")

    logger.info(f"Review received: {len(review)} characters")
    
    # Track how long the API call takes
    start_time = time.time()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[ {"role": "user", "content": prompt} ]
    )

    content= response.choices[0].message.content.strip()
    
    if not content:
           raise ValueError("Empty response from model")

    if "```" in content:
           content = content.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(content)

        logger.info(
        f"Review analyzed successfully in {time.time()-start_time:.2f}s"
    )
        return result
    
    except json.JSONDecodeError:
             logger.error(f"Invalid JSON returned: {content}")
             raise