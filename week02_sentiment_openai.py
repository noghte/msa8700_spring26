from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

import os

df = pd.read_csv("amazon_reviews.csv")
df = df[["reviewText"]]

OPENAI_KEY=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

for text in df["reviewText"].to_list()[:5]:
    prompt=f"Classify the sentiment of the following review as positive, neutral, or negative:\n\n{text}\n\nINSTRUCTIONS: Answer only with one word [Positive, Neutral, or Negative]. Do not explain. Do not return anything else."

    resp = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role":"system", "content":"You are helpful assistant expert in finding sentiments of reviews."},
            {"role": "user", "content": prompt }
        ],
        temperature=1 #The less the temperature is, the more the model is faithful to the prompt. Higher temperature = more creativity
    )
    print("Text:", text[:300], "Sentiment:", resp.choices[0].message.content)
    print("\n=========\n")