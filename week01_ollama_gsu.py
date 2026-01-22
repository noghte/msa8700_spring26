import requests

url = "http://10.230.100.240:17020/api/generate"

data = {
    "model" : "llama3.1",
    "prompt": "What do you know about Atlanta?",
    "stream": False
}
response = requests.post(url, json=data)
print(response.json()["response"])