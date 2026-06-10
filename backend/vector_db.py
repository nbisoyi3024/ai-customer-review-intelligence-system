#Embeddings
import chromadb
import uuid
import os
from openai import OpenAI
from dotenv import load_dotenv
from backend.logger import logger 
from backend.llm_analyzer import analyze_review

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_collection():

    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    collection = chroma_client.get_or_create_collection(
        name="customer_reviews"
    )
    logger.info("Connected to ChromaDB")
    
    return collection


def get_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def store_single_review(review):

    collection = get_collection()

    embedding = get_embedding(review)
    
    analysis = analyze_review(review)

    existing = collection.get()

    if review not in existing["documents"]:
        collection.add(
        ids=[str(uuid.uuid4())],
        documents=[review],
        embeddings=[embedding],
        metadatas=[{
                "category": analysis["category"],
                "sentiment": analysis["sentiment"]
            }]
    )

    print("Stored Successfully")
    print(collection.count())


def search_reviews(query):

    collection = get_collection()

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]

def store_dataset_reviews(df):
    for _, row in df.iterrows():
       
        text = row["full_text"]
       
        collection = get_collection()

        embedding = get_embedding(text)

        analysis = analyze_review(text)

        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "category": analysis["category"],
                "sentiment": analysis["sentiment"]
            }]
        )

    print("Stored dataset in ChromaDB")
    print("Total records:", collection.count())


def get_top_reviews(query, k=10):

    collection = get_collection()

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results