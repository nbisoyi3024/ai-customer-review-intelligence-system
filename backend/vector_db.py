import faiss
import numpy as np
import uuid
import os
import pickle

from openai import OpenAI
from dotenv import load_dotenv

from backend.logger import logger
from backend.llm_analyzer import analyze_review

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FAISS_INDEX_PATH = "./faiss_db/index.faiss"
METADATA_PATH = "./faiss_db/metadata.pkl"


def get_index():
    """
    Load existing FAISS index or create a new one.
    """

    os.makedirs("./faiss_db", exist_ok=True)

    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        logger.info("Loaded existing FAISS index")
    else:
        # text-embedding-3-small produces 1536-dimensional embeddings
        index = faiss.IndexFlatL2(1536)
        logger.info("Created new FAISS index")

    return index


def get_metadata():
    """
    Load metadata associated with FAISS vectors.
    """

    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "rb") as f:
            return pickle.load(f)

    return []


def save_index(index):
    """
    Persist FAISS index to disk.
    """

    faiss.write_index(index, FAISS_INDEX_PATH)


def save_metadata(metadata):
    """
    Persist review metadata to disk.
    """

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def store_single_review(review):

    index = get_index()
    metadata = get_metadata()

    # Avoid duplicate reviews
    for item in metadata:
        if item["review"] == review:
            logger.info("Review already exists")
            return

    embedding = get_embedding(review)

    analysis = analyze_review(review)

    # Convert embedding to FAISS format
    vector = np.array([embedding], dtype="float32")

    # Add vector to FAISS
    index.add(vector)

    # Store metadata using same index position
    metadata.append({
        "id": str(uuid.uuid4()),
        "review": review,
        "category": analysis["category"],
        "sentiment": analysis["sentiment"]
    })

    save_index(index)
    save_metadata(metadata)

    logger.info("Stored review in FAISS")

    print("Stored Successfully")
    print("Total records:", index.ntotal)


def search_reviews(query):

    index = get_index()
    metadata = get_metadata()

    if index.ntotal == 0:
        return []

    query_embedding = get_embedding(query)

    query_vector = np.array(
        [query_embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_vector,
        3
    )

    results = []

    for idx in indices[0]:

        if idx != -1:
            results.append(metadata[idx]["review"])

    return results


def store_dataset_reviews(df):

    index = get_index()
    metadata = get_metadata()
    # Keep track of reviews already stored in FAISS
    existing_reviews = {item["review"] for item in metadata}

    added = 0
    skipped = 0

    for _, row in df.iterrows():

        text = row["full_text"]

        # Skip reviews already in FAISS
        if text in existing_reviews:
            skipped += 1
            continue

        embedding = get_embedding(text)

        analysis = analyze_review(text)

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        index.add(vector)

        metadata.append({
            "id": str(uuid.uuid4()),
            "review": text,
            "category": analysis["category"],
            "sentiment": analysis["sentiment"]
        })
        existing_reviews.add(text)
        added += 1

    save_index(index)
    save_metadata(metadata)

    print("Stored dataset in FAISS")
    print("Added:", added)
    print("Skipped:", skipped)
    print("Total records:", index.ntotal)


def get_top_reviews(query, k=10):

    index = get_index()
    metadata = get_metadata()

    if index.ntotal == 0:
        return {
            "documents": [[]],
            "distances": [[]]
        }

    query_embedding = get_embedding(query)

    query_vector = np.array(
        [query_embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_vector,
        min(k, index.ntotal)
    )

    documents = []

    for idx in indices[0]:

        if idx != -1:
            documents.append(
                metadata[idx]["review"]
            )

    return {
        "documents": [documents],
        "distances": distances.tolist()
    }