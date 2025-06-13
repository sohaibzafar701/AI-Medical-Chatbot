from chromadb import PersistentClient
client = PersistentClient(path="C:/Users/sohaib/Downloads/medical-chatbot-main/medical-chatbot-main/dataset/chromadb")
collection = client.get_collection(name="medquad")
print(f"Number of items in medquad: {collection.count()}")
sample = collection.get(limit=1)
print(f"Sample data: {sample}")