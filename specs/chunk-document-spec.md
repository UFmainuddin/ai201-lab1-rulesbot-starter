# Spec: `chunk_document()`

**File:** `ingest.py`
**Status:** Complete

---

## Purpose

This function splits one rule book into smaller chunks. The chunks are used for embeddings and search.

Each chunk should have enough text to make sense by itself.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | The full rule book text |
| `game_name` | `str` | The game name |

**Output:** `list[dict]`

Each dict has these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name |
| `"chunk_id"` | `str` | A unique chunk id |

---

## Design Decisions

### Splitting approach

The code uses a character sliding window. It takes 300 characters, then moves forward by 250 characters. This makes a 50 character overlap.

### Chunk size

The chunk size is 300 characters. This is a good size for rule books because many rules are short.

### Overlap

The overlap is 50 characters. This helps when a rule is split between two chunks.

### Minimum chunk length

The minimum chunk length is 50 characters. Very small chunks are skipped because they usually do not have enough meaning.

### Rationale

Rule book text is dense. A small but complete chunk helps the search find the correct rule. Big chunks can mix too many rules together.

### Known limitations

The splitter can cut in the middle of a sentence. It does not understand paragraphs. A sentence-aware splitter could be better, but this version is simple and works for the lab.

---

## Implementation Notes

**Actual chunk count produced across all 8 rule books:**

```text
149 chunks
```

**One thing that surprised you or did not match your expectations:**

Some chunks start in the middle of a sentence. The overlap helps, but the chunks are not always clean to read.
