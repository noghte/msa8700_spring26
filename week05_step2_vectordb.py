from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct

import pandas as pd
import uuid
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

QDRANT_URL = "https://fa393320-0177-4942-b5c2-4eb22b132542.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.vjPCYZ8B2RfF6CBPMgilDTK1GKmcM71JVg7ZUd7xyHM"

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# qdrant_client.delete_collection(collection_name="kinase")
qdrant_client.recreate_collection(
    collection_name="kinase", 
    vectors_config=models.VectorParams(
        size=768, 
        distance=models.Distance.COSINE)
        )

print(qdrant_client.get_collections())

# delete collection
# qdrant_client.delete_collection(collection_name="sentiments")

df = pd.read_csv("kinases.csv")
functions = df["functions"].fillna("").tolist()

ollama_url = "http://10.230.100.240:17020"
model = OllamaEmbeddings(
    model="nomic-embed-text:latest",
    base_url=ollama_url
)

# Testing one item
# print(functions[0])
# vector = model.embed_documents(functions[0])
# print(vector)
vectors = model.embed_documents(functions) 
print("embedding done!")

points = []
for i, row in df.iterrows():
    points.append(
        PointStruct(
            id=uuid.uuid4(),
            vector=vectors[i],
            payload={
                "uniprot": row["uniprot"],
                "name": row["name"]
            }
        )
    )
    print(f"Index: {i+1}")

qdrant_client.upsert(collection_name="kinase", points=points)
print("Done!")