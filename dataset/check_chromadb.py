from chromadb import PersistentClient
client = PersistentClient(path="C:/Users/sohaib/Downloads/medical-chatbot-main/medical-chatbot-main/dataset/chromadb")
collections = client.list_collections()
print("Available collections:", [c.name for c in collections])