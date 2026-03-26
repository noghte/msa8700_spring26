from langgraph.store.memory import InMemoryStore
import uuid
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

store = InMemoryStore()


@tool
def save_city_to_memory(username: str, city_name: str) -> str:
    """
    Save the city that user is interested in to memory for future recall.
    Always call this tool when user mentions a city name.

    Args:
        username (str): The user of interest.
        city_name (str): The city the user is interested in

    Returns:
        str: The status of memory
    """
    namespace = ("user", "city")
    memory_id = str(uuid.uuid4())
    store.put(namespace, memory_id, {"city": city_name})
    return "Favorite city of the user saved to memory."


@tool
def recall_city(username):
    """
    Check if we have already favorite city of this user.
    Always call this FIRST before answering to user questions.

    Args:
        username (str): The user to lookup in memory.

    Returns:
        _type_: _description_
    """
    namespace = ("user", "city")
    results = store.search(namespace, filter={"user": username.lower()})
    if results:
        return results[-1]
    else:
        return "No city found!"


if __name__ == "__main__":
    system_prompt = (
        "You are the user's assistant.\n"
        "Instructions:\n"
        "- Call recall_city FIRST if a city is mentioned."
        "- Then, if user mentions a city, store it to memory by calling save_city_to_memory tool\n"
        "Provide a short answer to user."
    )
    chat_model = ChatOllama(
        base_url="http://10.230.100.240:17020", model="gpt-oss:20b", temperature=0
    )

    # a ReAct agent
    graph = create_agent(
        model=chat_model,
        tools=[save_city_to_memory, recall_city],
        system_prompt=system_prompt,
    )

    # Example query
    # query = "What's the opinion of Aaron about Samsung Galaxy S3?"

    # Change the code to answer this query
    query = "How is the weather in Atlanta in summer?"

    messages = {
        "messages": [
            SystemMessage(content="Follow instructions strictly."),
            HumanMessage(content=query),
        ]
    }

    # Run the agent
    state = graph.invoke(messages)

    response = state["messages"][-1].content
    print(response)
