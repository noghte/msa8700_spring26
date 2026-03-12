## PIP LIBRARIES:

# pip install -U langchain
# pip install langgraph
# pip install tavily-python
# pip install langchain-ollama

import pandas as pd
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()

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
        max_reviews (int, optional): Maximum number of reviews. Use the default value 5.
    """
    df = load_reviews()
    name = person_name.strip().lower()
    reviews = df[df["reviewerName"].str.lower() == name]["reviewText"].tolist()
    if len(reviews) == 0:
        return f"No reviews found for {person_name}"
    
    return "\n\n".join(reviews[:max_reviews])

@tool 
def extract_reviews_by_product(product_name, max_reviews=10):
    """
    Get reviews mentioning a specific product from amazon_reviews.csv

    Args:
        product_name (str): The product name to search for in review text.
        max_reviews (int, optional): Maximum number of reviews. Defaults to 10.

    Returns:
        str: Reviews related the the product, concatenated.
    """
    df = load_reviews()
    keyword = product_name.strip().lower()
    mask = df["reviewText"].str.lower().str.contains(keyword, na=False)
    reviews = df[mask]["reviewText"].tolist()
    if len(reviews) == 0:
        return f"No reviews found mentioning '{product_name}'"
    return "\n\n".join(reviews[:max_reviews])

@tool
def web_search_product(product_query, max_results=10):
    """
    Search the web for the product (prefer Amazon links) using Tavily.

    Args:
        product_query (string): The product name user is searching for.
        max_results (int, optional): Defaults to 10.
    """
    travily_client = TavilyClient() # api_key="tvly-YOUR_API_KEY"
    # If you're not using a .env file
    # travily_client = TavilyClient(api_key=".....")
    response = travily_client.search(query=product_query, search_depth="basic",max_results=max_results)
    for result in response["results"]:
        if "amazon.com" in result["url"]:
            return result["url"]
    return "Not Found"

if __name__ == "__main__":
    # revs = extract_reviews_by_person("Aaron")
    # print(revs) # Samsung Galaxy S3, Nikon DSLR
    
    system_prompt = (
        "You are a concise analyst.\n"
        "Rules:\n"
        "1) If asked about a reviewer's opinion, call extract_reviews_by_person,\n"
        "2) If asked about a product in general, call extract_reviews_by_product,\n"
        "3) Find the Amazon link of the product using web_search_product tool.\n"
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
        temperature=0
    )

    graph = create_react_agent(
        model=chat_model,
        tools=[extract_reviews_by_person, extract_reviews_by_product, web_search_product],
        prompt=system_prompt
    )

    # Example query
    # query = "What's the opinion of Aaron about Samsung Galaxy S3?"
    
    # Change the code to answer this query
    query = "What's the sentiment of reviewers about Sandisk 16GB?"

    messages = {
        "messages":
            [SystemMessage(content="Follow rules strictly."),
            HumanMessage(content=query)]
        }

    # Run the agent
    state = graph.invoke(messages)

    # Print the final answer
    print(state["messages"][-1].content)