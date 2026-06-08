# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Complete

---

## Purpose

This function takes a user question and searches the vector store for the best rule chunks. It returns the chunks in order, from closest match to weakest match.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user question |
| `n_results` | `int` | The max number of chunks to return |

**Output:** `list[dict]`

Each dict has these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name |
| `"distance"` | `float` | Cosine distance. Lower is better |

If the collection is empty, return `[]`.

---

## Design Decisions

### Query approach

I use `_collection.query()` with one query string. I pass `query_texts=[query]`, `n_results=n_results`, and `include=["documents", "metadatas", "distances"]`. This gives the text, game metadata, and score for each result.

### Return structure

One returned item looks like this:

```python
{
    "text": "When a 7 is rolled...",
    "game": "Catan",
    "distance": 0.466,
}
```

The text comes from `results["documents"][0]`. The game comes from `results["metadatas"][0]`. The score comes from `results["distances"][0]`.

### Handling the nested result structure

Chroma returns one inner list for each query. We only send one query, so the real results are at index `[0]`. For example, `results["documents"][0]` is the list of chunks for this one question.

### Relevance threshold

`retrieve()` returns all top results. I do not filter here because it is useful to see weak results while testing. The generation step filters weak chunks before sending context to the LLM.

### Edge cases

If the collection is empty, the function returns `[]`. If the query does not match well, it still returns the closest chunks, but the distances will be high. If the query matches many games, it can return chunks from many games.

---

## Implementation Notes

**Test query and top result returned:**

```text
Query: What happens when you run out of disease cubes in Pandemic?
Top result game: Pandemic
Distance score: 0.373
Does it make sense? Yes. The chunk says players lose if a disease cube color runs out.
```

**One thing about the query results that surprised you:**

The query "What happens when you roll a 7?" returned Catan first, but it also returned some Risk chunks after that. This happened because Risk also has dice rules. The distance scores helped show that Catan was the best match.
