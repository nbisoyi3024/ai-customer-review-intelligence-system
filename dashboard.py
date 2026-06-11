from pymongo import MongoClient
import pandas as pd
from backend.mongo_db import reviews_collection
import os 
import streamlit as st
import matplotlib.pyplot as plt
from backend.logger import logger

client = MongoClient(os.getenv("MONGO_URI"))
db = client["customer_reviews"]
reviews_collection = db["reviews"]

data = list(reviews_collection.find())

df = pd.DataFrame(data)

# ---------------- SENTIMENT CHART ----------------
st.subheader("📈 Sentiment Distribution")

sentiment_counts = df["sentiment"].value_counts()

fig, ax = plt.subplots()

ax.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%"
)

st.pyplot(fig)

# ---------------- CATEGORY CHART ----------------

st.subheader("📊 Review Categories")

category_counts = df["category"].value_counts().head(10)

fig2, ax2 = plt.subplots()

ax2.bar(
    category_counts.index,
    category_counts.values
)

plt.xticks(rotation=45)

st.pyplot(fig2)

df = df.drop(columns=["_id"])

st.title("📊 Customer Analytics Dashboard")

st.metric("Total Reviews", len(df))

st.subheader("Sentiment Distribution")
st.bar_chart(df["sentiment"].value_counts())

st.subheader("Top 10 Categories")
st.bar_chart(category_counts)

st.subheader("Sample Data")
st.dataframe(df.head())

st.subheader("🔍 Explore Top Reviews")

query = st.text_input("Search reviews (e.g. delivery, pricing, support)")

if query:

    results = reviews_collection.find({
        "$text": {"$search": query}
    }).limit(10)

    top_reviews = list(results)

    if len(top_reviews) == 0:
        st.warning("No matching reviews found.")
    else:
        for i, review in enumerate(top_reviews, 1):

            st.markdown(f"### Review {i}")

            st.write("📝", review.get("review_text", "No text"))

            st.write("📂 Category:", review.get("category"))

            st.write("😊 Sentiment:", review.get("sentiment"))

            st.divider()