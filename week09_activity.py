import pandas as pd
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()

@tool
def fetch_trivia_question():
    """
    Fetch a trivia question.
    """
    url = "https://opentdb.com/api.php?amount=3&category=28&difficulty=medium&type=boolean"
    # TODO: call the api and return the question + answer choice
    # Hint: response.json()["results"][0]
    pass

# Todo: similar to week07_agent_example.py create an agent

# if user asks for question, print the question 