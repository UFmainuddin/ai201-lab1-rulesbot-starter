from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)

MAX_CONTEXT_DISTANCE = 0.55


def _format_context(chunks):
    context_parts = []
    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"Source {index}\n"
            f"Game: {chunk['game']}\n"
            f"Distance: {chunk['distance']:.3f}\n"
            f"Rule text:\n{chunk['text']}"
        )
    return "\n\n---\n\n".join(context_parts)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    The answer must use only the retrieved rule text. If retrieval gives no
    useful context, return a clear fallback instead of asking the model to
    guess.
    """
    if not retrieved_chunks:
        return (
            "I could not find anything relevant in the loaded rule books. "
            "Try rephrasing your question or check that ingestion is working."
        )

    relevant_chunks = [
        chunk for chunk in retrieved_chunks
        if chunk["distance"] <= MAX_CONTEXT_DISTANCE
    ]

    if not relevant_chunks:
        return (
            "I could not find this answer in the loaded rule books. "
            "Please ask about one of the loaded games or try a more specific question."
        )

    system_prompt = (
        "Answer using only the rule text provided by the user. "
        "If the answer is not in the provided rule text, say that clearly. "
        "Do not guess, do not use outside knowledge, and do not fill in missing details. "
        "Always name the game or games that support the answer."
    )

    user_prompt = (
        "Retrieved rule text:\n"
        f"{_format_context(relevant_chunks)}\n\n"
        "Question:\n"
        f"{query}\n\n"
        "Write a short answer. Include the game name in the answer."
    )

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()
