import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://gpu-01.insight.gsu.edu:11443/api/generate"
api_key = os.getenv("GSU_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "llama3.1",
    "prompt": "What do you know about Atlanta?",
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
print(response.json()["response"])