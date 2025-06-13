import json
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

json_file = r"C:\Users\sohaib\Downloads\medical-chatbot-main\medical-chatbot-main\dataset\chromadb\medquad_cleaned.json"
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)
    print(f"Loaded {len(data)} items from JSON file")

client = chromadb.PersistentClient(path="C:/Users/sohaib/Downloads/medical-chatbot-main/medical-chatbot-main/dataset/chromadb")
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="medquad", embedding_function=embedding_function)
print("Collection created, starting indexing...")

for idx, item in enumerate(data):
    if idx % 100 == 0:  # Print progress every 100 items
        print(f"Indexed {idx} items...")
    try:
        collection.add(
            ids=[str(idx)],
            documents=[item["question"]],
            metadatas=[{"answer": item["answer"], "topic": item["topic"], "source": item["source"]}]
        )
    except Exception as e:
        print(f"Error at item {idx}: {e}")

print("✅ Data indexed into ChromaDB successfully!")