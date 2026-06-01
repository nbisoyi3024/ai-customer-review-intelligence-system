#UI
import streamlit as st
from llm_analyzer import analyze_review
from mongo_db import reviews_collection
from vector_db import store_single_review,store_dataset_reviews,search_reviews
from pipeline import process_review


st.set_page_config(page_title="AI Customer Review Analyzer")

st.title("AI Customer Review Analyzer")

review = st.text_area(
    "Write a Customer Review",
    height=250
)

if st.button("Analyze Review"):

    if review.strip() == "":
        st.warning("Please enter a review.")

    else:
        with st.spinner("Analyzing review..."):

            result = process_review(review)

            # Save original review
            result["review"] = review

            st.write("SAVING TO MONGO")
            # Save to MongoDB
            reviews_collection.insert_one(result)
            # Store in ChromaDB
            st.write("CALLING CHROMADB")
            store_single_review(review)
            
            st.write("CHROMADB FINISHED")

        st.success("Analysis Complete ✅")

        st.subheader("Sentiment")
        st.write(result["sentiment"])

        st.subheader("Summary")
        st.write(result["summary"])

        # if there is no issue, show None
        st.subheader("Issues")

        if result["issues"]:
            for issue in result["issues"]:
                st.markdown(f"- {issue}")
        else:
            st.write("No issues found")

        st.subheader("Category")
        st.write(result["category"])

        st.subheader("Recommendation")
        st.write(result["recommendation"])

st.markdown("### Semantic Search")

user_query = st.text_input("Search similar reviews")

if st.button("Search"):
    if user_query.strip() == "":
        st.warning("Please enter a search query.")
    else:
        results = search_reviews(user_query)
        st.json(results)

        st.subheader("Top Matching Reviews")

        if results:
            for r in results:
                st.info(r)
        else:
            st.warning("No similar reviews found") 