import os
from groq import Groq
from dotenv import load_dotenv
import numpy as np
import faiss

load_dotenv(dotenv_path=".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

embedding_model = None  # lazy load


def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return embedding_model


def split_into_chunks(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def build_faiss_index(chunks, model):
    embeddings = model.encode(chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index, embeddings


def retrieve_relevant_chunks(query, chunks, index, model, k=6):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    return [chunks[i] for i in indices[0]]


def simplify_legal_text(text, language):

    model = get_embedding_model()

    chunks = split_into_chunks(text)
    index, _ = build_faiss_index(chunks, model)

    query = """
Extract structured information about:
- Eligibility
- Benefits
- Obligations
- Penalties
- Deadlines
"""

    retrieved_chunks = retrieve_relevant_chunks(query, chunks, index, model)
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a legal simplification assistant.

Use ONLY the context provided below.
Do NOT hallucinate or invent information.

Keep headers EXACTLY as:

Eligibility:
Benefits:
Obligations:
Penalties:
Deadlines:

Generate content in {language}.
Be concise and avoid repetition.

Context:
{context}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content
