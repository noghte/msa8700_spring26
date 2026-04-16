import requests

url = "http://10.230.100.240:17020/api/generate"

data = {
    "model" : "gpt-oss:20b",
    "prompt": "Fill in the blank (just one word). Scott works in a hospital, he is a [BLANK].",
    "stream": False
}

for i in range(5):
    response = requests.post(url, json=data)
    print(i, response.json()["response"])