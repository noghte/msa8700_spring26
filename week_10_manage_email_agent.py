from langchain.tools import tool
from langchain.agents import create_agent
import os
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY=os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-5-mini", stream_usage=False)

@tool
def send_email(
    to: list[str],  # email addresses
    subject: str,
    body: str,
    cc: list[str] = []
) -> str:
    """Send an email via email API. Requires properly formatted addresses."""
    # Stub: In practice, this would call SendGrid, Gmail API, etc.
    return f"Email sent to {', '.join(to)} - Subject: {subject}"


# query = "Schedule a team meeting next Tuesday at 2pm for 1 hour"
# ai_msg = calendar_agent.invoke({"messages": [{"role": "user", "content": query}]})
# for msg in ai_msg["messages"]:
#     print("----START----\n")
#     print(msg.content)
#     print("\n---END-----\n")

# final_response = ai_msg["messages"][-1].content
# print("Final Response:")
# print(final_response)

EMAIL_AGENT_PROMPT = (
    "You are an email assistant. "
    "Compose professional emails based on natural language requests. "
    "Extract recipient information and craft appropriate subject lines and body text. "
    "Use send_email to send the message. "
    "Always confirm what was sent in your final response."
)

email_agent = create_agent(
    model,
    tools=[send_email],
    system_prompt=EMAIL_AGENT_PROMPT,
)


@tool
def manage_email(request: str) -> str:
    """Send emails using natural language.

    Use this when the user wants to send notifications, reminders, or any email
    communication. Handles recipient extraction, subject generation, and email
    composition.

    Input: Natural language email request (e.g., 'send them a reminder about
    the meeting')
    """
    result = email_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text

