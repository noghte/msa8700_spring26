import requests

#url = "http://10.230.100.240:17020/api/generate"
url = "http://localhost:11434/api/generate"
data = {
    "model" : "llama3.2:1b",
    "prompt": "How's the weather in Atlanta?",
    "stream": False
}
response = requests.post(url, json=data)
print(response.json()["response"])