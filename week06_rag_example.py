from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct

import os
import pandas as pd
import uuid
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()


model = OpenAIEmbeddings(model="text-embedding-3-small")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
print(QDRANT_URL)
