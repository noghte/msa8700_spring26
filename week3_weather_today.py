import requests

ollama_url = "http://10.230.100.240:17020/api/generate"

def get_weather(city):
    r = requests.get(f"https://wttr.in/{city}?format=j1")
    data = r.json()
    return data

city_name = input("Enter a city name:")
data = get_weather(city_name)
feels_like = data["current_condition"][0]["FeelsLikeF"]
localObsDateTime = data["current_condition"][0]["localObsDateTime"]
humidity = data["current_condition"][0]["humidity"]

weather = f"""On {localObsDateTime}, 
        the weather of {city_name} feels like: {feels_like} F 
        and humidity is {humidity}"""

prompt = f"Do I need a jacket in {city_name} tonight? More info: {weather}"

data = {
    "model": "gpt-oss:20b",
    "prompt": prompt,
    "stream": False
}

res = requests.post(ollama_url, json=data)
llm_response = res.json()["response"]

print(llm_response)