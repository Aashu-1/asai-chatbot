import chromadb
import os

HF_SPACE_ID = os.getenv("HF_SPACE_ID")
PERSIST_DIR = "/tmp/chroma_db" if HF_SPACE_ID else "./chroma_db"
os.makedirs(PERSIST_DIR, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)
collection = chroma_client.get_or_create_collection(name="resume")

def store_in_chroma(chunks, embeddings):
    if collection.count() > 0:
        print("✅ Chroma already has data, skipping indexing")
        print("hello")
        return

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"chunk_{i}_{hash(chunk)}"],
            documents=[chunk],
            embeddings=[emb if isinstance(emb, list) else emb.tolist()]
        )

    print("✅ Stored in ChromaDB")


def retrieve_context(message, embed_fn):
    query_embedding = embed_fn(message)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents"]
    )

    return "\n".join(results["documents"][0])