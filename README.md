# AI Customer Review Intelligence System

## Repository Name

`ai-customer-review-intelligence-system`

---

# README.md

# AI Customer Review Intelligence System

A production-style Generative AI application for customer review analysis using OpenAI LLMs, semantic search, vector embeddings, and Retrieval-Augmented Generation (RAG).

This system analyzes customer reviews to generate:

* Sentiment analysis
* Review summarization
* Issue extraction
* AI-generated recommendations
* Semantic similarity search

Built using Python, OpenAI APIs, ChromaDB, FastAPI, MongoDB, and Streamlit.

---

# Features

* AI-powered customer review analysis using OpenAI LLMs
* Semantic search using embeddings + ChromaDB
* Context-aware retrieval system
* FastAPI backend services
* Streamlit interactive frontend
* MongoDB integration for review storage
* Modular AI pipeline architecture
* Duplicate review handling and data cleaning
* Real-time conversational analysis workflow

---

# Tech Stack

## Backend

* Python
* FastAPI
* OpenAI API
* MongoDB

## Generative AI

* OpenAI GPT models
* Embeddings
* Retrieval-Augmented Generation (RAG)
* Prompt Engineering

## Vector Database

* ChromaDB

## Frontend

* Streamlit

## Data Processing

* Pandas
* NumPy

---

# System Architecture

User Reviews → Data Cleaning → Embedding Generation → ChromaDB Vector Storage → Semantic Retrieval → OpenAI LLM Analysis → Streamlit UI

---

# Project Structure

```bash
ai-customer-review-intelligence-system/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env.example
│
├── data/
│   └── sample_reviews.csv
│
├── backend/
│   ├── api.py
│   ├── llm_service.py
│   ├── vector_store.py
│   └── database.py
│
├── frontend/
│   └── streamlit_ui.py
│
├── utils/
│   ├── preprocessing.py
│   └── prompts.py
│
└── chroma_db/
```

---

# Screenshots

Add screenshots here:

* Streamlit dashboard
* Semantic search results
* Review summarization output
* Architecture diagram

Example:

```markdown
![Dashboard](images/dashboard.png)
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ai-customer-review-intelligence-system.git
cd ai-customer-review-intelligence-system
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=your_mongodb_connection_string
```

---

# Run Application

## Start FastAPI Backend

```bash
uvicorn backend.api:app --reload
```

## Run Streamlit Frontend

```bash
streamlit run frontend/streamlit_ui.py
```

---

# Sample Use Cases

* Analyze customer sentiment trends
* Detect recurring customer issues
* Generate automated business insights
* Search similar customer complaints
* Summarize large review datasets

---

# Future Improvements

* Multi-agent workflow integration
* Advanced analytics dashboard
* Cloud deployment (GCP/AWS)
* Real-time streaming reviews
* LLM evaluation metrics
* User authentication

---

# Resume Project Description

Built an end-to-end GenAI system for customer review analysis including sentiment detection, summarization, and issue extraction using OpenAI LLMs. Implemented semantic search using embeddings and ChromaDB to enable context-aware retrieval of similar reviews. Designed modular FastAPI backend with Streamlit UI and MongoDB storage for scalable deployment.

---

# LinkedIn Featured Description

Built a production-style GenAI system for sentiment analysis, review summarization, issue extraction, and semantic search using OpenAI embeddings and ChromaDB. Designed modular FastAPI backend services with Streamlit UI and MongoDB integration for scalable AI workflows.

---

# Files You Should Upload to GitHub

## MUST Upload

* Source code
* requirements.txt
* README.md
* sample dataset
* screenshots
* architecture diagram

## DO NOT Upload

* .env
* API keys
* large datasets
* venv folder
* chroma cache files

---

# .gitignore Example

```gitignore
venv/
.env
__pycache__/
*.pyc
chroma_db/
.DS_Store
```

---

# Recommended GitHub Topics

Add these topics to your repository:

* generative-ai
* llm
* rag
* chromadb
* openai
* fastapi
* streamlit
* semantic-search
* vector-database
* python
* ai-project

---

# Suggested Commit Message

```bash
Initial commit - AI Customer Review Intelligence System with RAG, semantic search, and FastAPI backend
```

---

# LinkedIn Featured Title

AI Customer Review Intelligence System | GenAI + Semantic Search
