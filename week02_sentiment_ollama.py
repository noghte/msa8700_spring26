import requests
import pandas as pd

df = pd.read_csv("amazon_reviews.csv")
df = df[["reviewText"]]

url = "http://10.230.100.240:17020/api/generate"

for text in df["reviewText"].to_list()[:5]:
    data = {
        "model" : "llama3.1",# "gpt-oss:20b", # llama3.1
        "prompt": f"Classify the sentiment of the following review as positive, neutral, or negative:\n\n{text}\n\nNOTE: Answer only with one word [Positive, Neutral, or Negative]. Do not explain. Do not return anything else.",
        "stream": False
    }
    response = requests.post(url, json=data)
    print("Text:", text[:300], "Sentiment:", response.json()["response"])
    print("\n=========\n")