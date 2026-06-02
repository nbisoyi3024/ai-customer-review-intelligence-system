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

category_counts = df["category"].value_counts()

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

st.subheader("Category Distribution")
st.bar_chart(df["category"].value_counts())

st.subheader("Sample Data")
st.dataframe(df.head())