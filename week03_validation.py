# Rewrite the review analysis code (with Ollama)
# with error validation with pydantic library. 

import requests
import pandas as pd
from pydantic import BaseModel, Field, ValidationError
from enum import Enum
import json

# sentiment enum (a type)
class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

# schema for pydantic
class ReviewAnalysis(BaseModel):
    review:str = Field(description="the review text")
    sentiment:Sentiment = Field("must be positive, neutral, or negative")
    confidence:float = Field("confidence between 0 to 1", ge=0, le=1)

df = pd.read_csv("amazon_reviews.csv")
df = df[["reviewText"]]

url = "http://10.230.100.240:17020/api/generate"

for text in df["reviewText"].to_list()[:5]:
    prompt = f"""Classify the sentiment of the following review as positive, neutral, or negative:
    \n\n{text}\n\n
    INSTRUCTIONS: 
    Return ONLY a valid JSON object with these exact fields:
    - "review: a summary of the review in one or two sentences"
    - "sentiment: must be exactly one of: "positive", "neutral", or "negative"
    - "confidence: a number between 1 to 100 representing your confidence"
    Do not explain. 
    Do not return anything else.
    Example output:
    {{ "review: "Great product!", "sentiment": "positive", "confidence": 0.95 }}
    """
    data = {
        "model" : "llama3.1",# "gpt-oss:20b", # llama3.1
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    llm_response = response.json()["response"]

    try:
        parsed_json = json.loads(llm_response)
        result = ReviewAnalysis(**parsed_json)
        # we assume everything is ok
        print("Summary:", result.review)
        print("Sentiment:", result.sentiment.value)
        print("Confidence: ", result.confidence)
        print("Status: 😁 Valid!")
    except json.JSONDecodeError: # a JSON error
        print("Error: Response is not JSON")
    except ValidationError as e:
        print("😔 Error!")
        print("Review:", text)
        print("Error Description:", e.errors()[0]["msg"])
        print("Invalid Input:", e.errors()[0]["input"])

    print("\n=========\n")