import pandas as pd
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
# import requests

def load_reviews():
    df = pd.read_csv("amazon_reviews.csv")
    df["reviewerName"] = df["reviewerName"].fillna("").astype(str)
    df["reviewText"] = df["reviewText"].fillna("").astype(str)
    return df

@tool
def extract_reviews_by_person(person_name, max_reviews=5):
    """
    Get reviews written by a specific person from amazon_reviews.csv

    Args:
        person_name (str): The username of the person who write the review
        max_reviews (int): Maximum number of reviews. Use the default value 5.
    """
    df = load_reviews()
    name = person_name.strip().lower()
    reviews = df[df["reviewerName"].str.lower() == name]["reviewText"].tolist()
    if len(reviews) == 0:
        return f"No reviews found for {person_name}"
    
    return "\n\n".join(reviews[:max_reviews])

if __name__ == "__main__":
    # revs = extract_reviews_by_person("Aaron")
    # print(revs) # Samsung Galaxy S3, Nikon DSLR
    
    system_prompt = (
        "You are a concise analyst.\n"
        "Rules:\n"
        "1) If asked about a reviewer's opinion, call extract_reviews_by_person\n"
        "Important: After calling tools, response in this format:\n"
        "Sentiment: Positive | Negative | Mixed | Neutral\n"
        "Evidence:\n"
        "   - bullet point\n"
        "   - bullet point\n"
        "Amazon Link: <url> or Not Found\n"
        "Do not invent links or reviews."
    )
    chat_model = ChatOllama(
        base_url = "http://10.230.100.240:17020",
        model="gpt-oss:20b",
        temprature=0
    )

    graph = create_react_agent(
        model=chat_model,
        tools=[extract_reviews_by_person],
        prompt=system_prompt
    )

    # Example query
    query = "What's the opinion of Aaron about Samsung Galaxy S3?"
    messages = {
        "messages":
            [SystemMessage(content="Follow rules strictly."),
            HumanMessage(content=query)]
        }

    # Run the agent
    state = graph.invoke(messages)

    # Print the final answer
    print(state["messages"][-1].content)