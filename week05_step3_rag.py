from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct

import pandas as pd
import uuid
import os
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

ollama_url = "http://10.230.100.240:17020"
# model = OllamaEmbeddings(
#     model="nomic-embed-text:latest",
#     base_url=ollama_url
# )
model = OpenAIEmbeddings(model="text-embedding-3-small")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

query_text = "What is the function of protein AKT3?"
query_vector = model.embed_query(query_text)

# Goal: to find vectors that are similar to the query vector
response = client.query_points(
    collection_name="kinase",
    query=query_vector,
    limit=5,
    with_payload=True
)

print(response.points)