import requests
import json
from langchain.agents import create_agent
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
    # url = "https://opentdb.com/api.php?amount=3&category=28&difficulty=medium&type=boolean"
    # Docs: https://the-trivia-api.com/docs/
    url = "https://the-trivia-api.com/v2/questions?limit=1"
    data = requests.get(url).json()
    return {"question": data[0]["question"]["text"], "correct_answer": data[0]['correctAnswer']}  
 

if __name__ == "__main__":

    system_prompt = (
        "You are a trivia expert.\n"
        "Instructions:\n"
        "- If user asks about a question, call fetch_trivia_question tool\n"
        "Output Format: JSON\n"
        "{{ 'question': 'question_text', 'correct_answer': 'correct_answer_text' }}"
        "\n\nExample:\n"
        "{{ 'question': 'The sky is blue because of water reflection.', 'correct_answer': 'False' }}"
    )
    chat_model = ChatOllama(
        base_url = "http://10.230.100.240:17020",
        model="gpt-oss:20b",
        temperature=0
    )

    # a ReAct agent
    graph = create_agent(
        model=chat_model,
        tools=[fetch_trivia_question],
        system_prompt=system_prompt
    )

    # Example query
    # query = "What's the opinion of Aaron about Samsung Galaxy S3?"
    
    # Change the code to answer this query
    query = "Give me a trivia question"

    messages = {
        "messages":
            [SystemMessage(content="Follow instructions strictly."),
            HumanMessage(content=query)]
        }

    # Run the agent
    state = graph.invoke(messages)

    # Print the final answer
    # print(state["messages"][-1].content)
    response = json.loads(state["messages"][-1].content)
    print("Question:",response["question"])
    
    user_answer = input("\nEnter your answer: ").strip().lower()
    correct_answer = response["correct_answer"].strip().lower()

    if user_answer == correct_answer:
        print("✅ Correct!")
    else:
        print("❌ Wrong!")
        print("The correct answer is", correct_answer)

