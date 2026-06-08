# RulesBot Planning

This file explains my choices for the lab. I use simple words so it is easy to read later.

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why this strategy fits rule book text:**

Rule books have many small rules. A 300 character chunk is usually big enough for one rule. It is also small enough so the search result is not too broad. The 50 character overlap helps when one rule is split between two chunks.

**Actual chunk count:** 149 chunks from 8 rule books

**One thing I noticed:**

Some chunks start in the middle of a sentence. This is not perfect, but the overlap helps keep the meaning.

---

## Retrieval Observations

| Query | Top result game | Does it make sense? |
|-------|-----------------|---------------------|
| "How do you win?" | Many games can match | Yes, because many games have win rules |
| "What happens when you roll a 7?" | Catan | Yes, this is about the robber rule |
| "Can two players share a route?" | Ticket To Ride | Yes, this is about double routes |

**Anything surprising?**

For "roll a 7", the first result was Catan, but some lower results were Risk because Risk also talks about dice. This shows why the generation step should ignore weak chunks.

---

## Response Quality

| Query | Answer accurate? | Properly grounded? | Cited the right game? |
|-------|------------------|--------------------|-----------------------|
| "What happens when you run out of disease cubes in Pandemic?" | Yes | Yes | Yes, Pandemic |
| "How do you get out of Jail in Monopoly?" | Yes | Yes | Yes, Monopoly |
| "How does the queen move in chess?" | Yes | Yes | It said the answer was not in the loaded rules |

**What would I change about the prompt to improve grounding?**

The prompt is direct now. It says to use only the provided rule text and not guess. If I wanted to improve it more, I would ask the model to quote a short phrase from the rule text for each answer.
