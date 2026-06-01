#Data ingestion
import pandas as pd
from vector_db import store_dataset_reviews

df = pd.read_csv(
    "data/train.csv",
    header=None,
    names=["id", "title", "review"]
)
# Combine title + review text
df["full_text"] = df["title"] + " " + df["review"]

# Drop null values
df = df[["full_text"]].dropna()

# Test with small sample first
df = df.sample(250, random_state=42)

store_dataset_reviews(df)

#create a smaller sample for testing
sample_df = df.sample(250, random_state=42)

sample_df.to_csv("/Users/niharikabisoyi/Desktop/GenAI/CustomerAnalysis/data/sample_reviews.csv", index=False)