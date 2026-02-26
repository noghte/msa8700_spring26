from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct

import os
import pandas as pd
import uuid
# from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv
load_dotenv()

df = pd.read_csv("kinases.csv")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def get_points(query_text, limit=3):
    query_vector = embedding_model.embed_query(query_text)
    response = client.query_points(
        collection_name="kinase",
        query=query_vector,
        limit=limit,
        with_payload=True
    )
    return response.points

def answer_with_llm(query_text, points):
    context = ""
    for p in points:
        uniprot = p.payload["uniprot"]
        nm = df[df["uniprot"] == uniprot]["name"].values[0]
        fn = df[df["uniprot"] == uniprot]["functions"].values[0]
        context += "Name: " + nm + " Functions: " + fn + "\n\n"
    print(context)

    system_message = "Answer using ONLY the provided context. \
                    If the context is insufficient, or irrelevant, say 'Bad Context!' \
                    Your answer should be short, up to the point, and not more than 1 sentence."
    human_message = f"User Question: {query_text} \n Context:\n{context}"
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=human_message)
    ]
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    
    resp = llm.invoke(messages)
    return resp.content

if __name__ == "__main__":
    # Example
    query_text = "What is the function of protein AKT3?"
    points = get_points(query_text)
    answer = answer_with_llm(query_text, points)
    print(answer)