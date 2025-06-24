# Guarded Agent Chatbot – RAG-Powered Query System

This project implements a Retrieval-Augmented Generation (RAG) pipeline to create a guarded chatbot that answers user questions based on internal documentation. It features two smart agents:
- A Guard Agent to filter irrelevant or inappropriate queries.
- A Details Agent that fetches relevant information from a vector database and generates responses using LLMs.

## Project Architecture and Flow

The project revolves around two main agents: `GaurdAgent` and `DetailsAgent`, orchestrated by a Streamlit app: `development_code.py`.

### 1. Preprocessing (`cleaning_data.ipynb`)
- Extracts raw text from the `initial_data/AI Training Document.pdf`.
- Cleans text by removing repetitive headers, footers, and extra whitespace.
- Splits the cleaned text into sentence-aware chunks.
- Saves results to `chunks.json`.

### 2. Embedding & Vector DB (`build_vector_database.ipynb`)
- Generates embeddings for each chunk using the `text-embedding-004` model.
- Initializes a Pinecone index (768-dimensional, cosine metric).
- Uploads embeddings and metadata to Pinecone under the `ns1` namespace.

### 3. Chatbot Interface (`development_code.py`)
- Users interact via a Streamlit interface.
- Guard Agent filters queries:
  - Rejects inappropriate content (e.g., competitors, staff info, pricing).
  - Allows relevant queries (e.g., about eBay policies).
- Details Agent:
  - Converts query to an embedding.
  - Retrieves top relevant chunks from Pinecone.
  - Uses those chunks as context for Gemini LLM to generate a grounded response.
- Users can toggle source knowledge visibility and reset chat.

## Model and Embedding Choices

- LLM: `gemini-1.5-flash`
  Used by both agents for natural language generation due to speed and cost-effectiveness.

- Embedding: `text-embedding-004`
  Produces 768-dimensional embeddings ideal for semantic search with Pinecone.

## Setup and Usage

### Prerequisites
Install dependencies:
```bash
pip install -r requirements.txt
```

> Ensure your `requirements.txt` includes:
> `streamlit`, `python-dotenv`, `google-generativeai`, `pinecone-client`, `pandas`, `requests`, `PyMuPDF`, `spacy`, `json`

Install spaCy English model:
```bash
python -m spacy download en_core_web_sm
```

### Environment Variables
Create a `.env` file in your root directory:
```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
```

## Step-by-Step Execution

### 1. Preprocess the Document
Run `cleaning_data.ipynb` to:
- Load and clean the PDF.
- Chunk it into sentence-aware text blocks.
- Save to `chunks.json`.

### 2. Build Embedding & Vector DB
Run `build_vector_database.ipynb` to:
- Load the chunks.
- Generate embeddings.
- Initialize Pinecone and upload them.

### 3. Start the Chatbot
```bash
streamlit run development_code.py
```

The chatbot UI will open in your browser. Ask questions, and the agents will handle them accordingly.

## Features

- Guarded input filtering using LLM
- Semantic search over documentation
- Source knowledge toggle in UI
- Streamlit interface with real-time feel
- Pinecone-powered RAG backend

## Project Structure

```
.
├── initial_data/
│   └── AI Training Document.pdf
├── chunks.json
├── .env
├── development_code.py
├── gaurd_agent.py
├── details_agent.py
├── cleaning_data.ipynb
├── build_vector_database.ipynb
└── requirements.txt
```

## Links

- GitHub Repo: https://github.com/Nik-56/amlgo_chatbot  
- Demo Video: https://drive.google.com/file/d/1Il6oFvpcWA4x-8LGV9-3hCxpLFMI_WeW/view?usp=sharing
