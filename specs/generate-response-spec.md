# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Complete

---

## Purpose

This function takes the user question and the retrieved rule chunks. It asks the LLM to answer using only those chunks.

The answer should name the game. If the answer is not in the chunks, the bot should say that clearly.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user question |
| `retrieved_chunks` | `list[dict]` | Chunks from `retrieve()` |

**Output:** `str`

The output is the answer shown to the user.

---

## Design Decisions

### Context formatting

Each chunk is labeled as a source. I include the source number, game name, distance score, and rule text. I separate sources with `---` so the model can see where one chunk ends and the next starts.

### System prompt grounding instruction

```text
Answer using only the rule text provided by the user. If the answer is not in the provided rule text, say that clearly. Do not guess, do not use outside knowledge, and do not fill in missing details. Always name the game or games that support the answer.
```

### System prompt citation instruction

```text
Always name the game or games that support the answer.
```

### Fallback behavior

If no chunks are retrieved:

```text
I could not find anything relevant in the loaded rule books. Try rephrasing your question or check that ingestion is working.
```

If all chunks are weak:

```text
I could not find this answer in the loaded rule books. Please ask about one of the loaded games or try a more specific question.
```

### Handling low-relevance chunks

I filter out chunks with distance above `0.55` before calling the LLM. This keeps weak matches from confusing the answer. The tradeoff is that a hard question might lose useful context, but it is safer than giving the model bad context.

### Message structure

The system message has the grounding rules. The user message has the retrieved context and the question. This keeps the instructions separate from the data.

---

## Implementation Notes

**Test query and response:**

```text
Query: What happens when you run out of disease cubes in Pandemic?
Response: In Pandemic, if any color of disease cubes runs out when a cube must be placed, the game ends immediately and players lose.
Correctly grounded? Yes
Cited the right game? Yes
```

**One thing changed after testing:**

I changed the weak chunk cutoff from `0.65` to `0.55`. The higher cutoff let in weak dice chunks from Risk for a Catan question about rolling a 7.
