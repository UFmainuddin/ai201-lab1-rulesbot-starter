# RulesBot

RulesBot is a board game rules assistant. It uses RAG, which means it first finds useful rule text and then asks an LLM to answer from that text.

The bot can answer questions about these games:

- Catan
- Clue
- Codenames
- Monopoly
- Pandemic
- Risk
- Ticket To Ride
- Uno

---

## What Is Implemented

- Loads rule books from `docs/`
- Splits rule books into chunks
- Stores chunks in ChromaDB
- Retrieves the best chunks for a user question
- Sends only the retrieved chunks to Groq
- Uses a grounding prompt so the answer stays inside the rule text
- Gives a fallback when the answer is not in the loaded rules

---

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example env file:

```bash
cp .env.example .env
```

On Windows:

```powershell
Copy-Item .env.example .env
```

Add your Groq API key in `.env`.

---

## Run

```bash
python app.py
```

The first run may take time because the embedding model downloads and loads.

If the browser does not open, use the local URL printed in the terminal. It is usually:

```text
http://127.0.0.1:7860
```

---

## Re-ingest Rules

ChromaDB saves the chunks in `chroma_db/`. If you change the chunking code or rule files, delete `chroma_db/` and run the app again.

On Mac or Linux:

```bash
rm -rf chroma_db/
python app.py
```

On Windows:

```powershell
Remove-Item -Recurse -Force chroma_db
python app.py
```

---

## Main Files

| File | Purpose |
|------|---------|
| `app.py` | Gradio chat app |
| `config.py` | Model and path settings |
| `ingest.py` | Loads and chunks rule books |
| `retriever.py` | Stores chunks and retrieves matches |
| `generator.py` | Builds the prompt and calls Groq |
| `planning.md` | Lab notes and test notes |
| `specs/` | Design notes for each milestone |
