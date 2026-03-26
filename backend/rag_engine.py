from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model (lightweight + free)
model = SentenceTransformer("all-MiniLM-L6-v2")


def split_into_chunks(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def build_faiss_index(chunks):
    embeddings = model.encode(chunks)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index, embeddings


def retrieve_relevant_chunks(query, chunks, index, k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    retrieved = [chunks[i] for i in indices[0]]
    return retrieved
