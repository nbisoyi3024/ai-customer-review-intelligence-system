#LLM analysis
import os
import time
import json
from dotenv import load_dotenv
from backend.logger import logger
from langchain_openai import AzureChatOpenAI, ChatOpenAI

load_dotenv()  

#while the default provider is OpenAI, you can switch to Azure by setting the LLM_PROVIDER environment variable to "azure".
provider = os.getenv("LLM_PROVIDER", "openai").lower()

if provider == "azure":
    client = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

elif provider == "openai":
    client = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )

else:
    raise ValueError(f"Unsupported LLM provider: {provider}")

def analyze_review(review):

    prompt = f"""
        Analyze this customer review:
        
        Allowed categories:
      - Delivery
      - Product Quality
      - Customer Support
      - Pricing
      - Packaging
      - Returns & Refunds
      - Other 
       
        Review:
       {review}

       Return ONLY valid JSON. 
       
       {{ 
       "sentiment": "", "summary":"", 
       "issues": [], "category": "", 
         "recommendation": "" 
       }} 
       "Write the summary using words directly from the review. 
       Do not infer emotions not explicitly stated."
     """
    #------Input validation------
    if not review:
          raise ValueError("Review cannot be empty")
    
    logger.info("Starting review analysis")

    logger.info(f"Review received: {len(review)} characters")
    
    # Track how long the API call takes
    start_time = time.time()

    response = client.invoke(prompt)
    content= response.content
    
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