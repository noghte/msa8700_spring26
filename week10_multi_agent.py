import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from week_10_manage_email_agent import manage_email
from week_10_schedule_event_agent import schedule_event

from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY=os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-5-mini", stream_usage=False)

SUPERVISOR_PROMPT = (
    "You are a helpful personal assistant. "
    "You can schedule calendar events and send emails. "
    "Break down user requests into appropriate tool calls and coordinate the results. "
    "When a request involves multiple actions, use multiple tools in sequence."
)

supervisor_agent = create_agent(
    model,
    tools=[schedule_event, manage_email],
    system_prompt=SUPERVISOR_PROMPT,
)

query = "Schedule a team standup for tomorrow at 9am at New York office"
ai_msg = supervisor_agent.invoke({"messages": [{"role": "user", "content": query}]})
for msg in ai_msg["messages"]:
    print("----START----\n")
    print(msg.content)
    print("\n---END-----\n")

final_response = ai_msg["messages"][-1].content
print("Final Response:")
print(final_response)