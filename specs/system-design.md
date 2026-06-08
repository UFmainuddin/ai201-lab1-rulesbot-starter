# RulesBot System Design

**Status:** Complete

---

## Problem

Board game rule books can be hard to search during a game. A player may ask one small question, but the answer can be hidden in a long rule book.

RulesBot helps by answering from the loaded rule books. The answer should come from the rule text, not from the model's memory.

---

## Architecture

RulesBot uses a RAG pipeline.

```text
User question
  -> Ingest rule books
  -> Retrieve useful chunks
  -> Generate a grounded answer
  -> Show the answer in the UI
```

---

## Parts

### 1. Ingest

File: `ingest.py`

The app loads text files from `docs/`. Each rule book is split into chunks. Each chunk has text, a game name, and a chunk id.

### 2. Store

File: `retriever.py`

Chunks are stored in ChromaDB. ChromaDB also stores embeddings, so the app can search by meaning.

### 3. Retrieve

File: `retriever.py`

When the user asks a question, ChromaDB returns the closest chunks. Lower distance means a better match.

### 4. Generate

File: `generator.py`

The app sends the retrieved chunks and the user question to Groq. The system prompt tells the model to use only the provided rule text.

### 5. UI

File: `app.py`

The Gradio app shows the chat box and calls the retrieval and generation steps.

---

## Technical Choices

### Embedding model

The app uses `all-MiniLM-L6-v2`. It is small and runs locally. It is good enough for short rule chunks.

### Vector store

The app uses ChromaDB with a local path, `chroma_db/`. This lets the app skip ingestion after the first run.

### LLM

The app uses Groq with `llama-3.3-70b-versatile`. The API key comes from `.env`.

### Distance

The app uses cosine distance. Lower scores are better. Very high scores are weak matches.

---

## File Status

| File | Status | Purpose |
|------|--------|---------|
| `app.py` | Complete | Runs the Gradio app |
| `config.py` | Complete | Stores settings |
| `ingest.py` | Complete | Loads and chunks rule books |
| `retriever.py` | Complete | Stores and retrieves chunks |
| `generator.py` | Complete | Builds grounded answers |
| `planning.md` | Complete | Records lab notes |
