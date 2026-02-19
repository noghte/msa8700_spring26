from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct

import os
import pandas as pd
import uuid
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

DIM_SIZE = 1536
# qdrant_client.delete_collection(collection_name="kinase")
qdrant_client.recreate_collection(
    collection_name="kinase", 
    vectors_config=models.VectorParams(
        size=DIM_SIZE, 
        distance=models.Distance.COSINE)
        )

print(qdrant_client.get_collections())

# delete collection
# qdrant_client.delete_collection(collection_name="sentiments")

df = pd.read_csv("kinases.csv")
functions = df["functions"].fillna("").tolist()

ollama_url = "http://10.230.100.240:17020"
# model = OllamaEmbeddings(
#     model="nomic-embed-text:latest",
#     base_url=ollama_url
# )
model = OpenAIEmbeddings(model="text-embedding-3-small")

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