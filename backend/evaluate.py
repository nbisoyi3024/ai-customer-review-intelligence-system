#backend/evaluate.py
# we will see how well our LLM is performing using RAGAS
# block RAGAS from trying to load Vertex AI
import os
from dotenv import load_dotenv

load_dotenv()

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset
from backend.llm_analyzer import analyze_review
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


# sample reviews to test
test_reviews = [
    "The product quality was amazing but delivery took 3 weeks!",
    "Terrible customer service, no one responded to my emails.",
    "Great battery life and the screen is beautiful.",
    "Package arrived completely broken. Very disappointed.",
    "Price is too high for what you get. Not worth it."
]

# we willrun each review through pipeline
questions   = []
answers     = []
contexts    = []

for review in test_reviews:

    # get the result from your actual analyzer
    result = analyze_review(review)

    # question = the review itself (what we're analyzing)
    questions.append(f"Analyze this review: {review}")

    # answer = the summary your LLM generated
    answers.append(result.get("summary", ""))

    # context = the review text (the source of truth)
    # RAGAS checks if the answer is faithful to this
    contexts.append([review])

    print(f"Review:   {review[:50]}...")
    print(f"Summary:  {result.get('summary', '')}")
    print(f"Sentiment:{result.get('sentiment', '')}")
    print()

# build dataset for RAGAS
dataset = Dataset.from_dict({
    "question": questions,
    "answer":   answers,
    "contexts": contexts
})

# create OpenAI LLM and embeddings for RAGAS to use
ragas_llm = LangchainLLMWrapper(ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
    ))
ragas_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY")
))

# run evaluation
print("Running RAGAS evaluation...")
results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=ragas_llm,
    embeddings=ragas_embeddings
)

# show scores
print()
print("=" * 40)
print("RAGAS EVALUATION RESULTS")
print("=" * 40)
faithfulness_score = sum(float(x) for x in results['faithfulness']) / len(results['faithfulness'])
relevancy_score = sum(float(x) for x in results['answer_relevancy']) / len(results['answer_relevancy'])

print(f"Faithfulness:     {faithfulness_score:.2f}")
print(f"Answer Relevancy: {relevancy_score:.2f}")
print()

# interpret scores
if faithfulness_score > 0.8:
    print("Low hallucination — summaries grounded in review text")
else:
    print("High hallucination — summaries adding info not in review")

if relevancy_score > 0.8:
    print("Summaries are relevant to the review content")
else:
    print("Summaries going off-topic — improve prompt")