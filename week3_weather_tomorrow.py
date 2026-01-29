import requests

ollama_url = "http://10.230.100.240:17020/api/generate"

def get_weather(city):
    r = requests.get(f"https://wttr.in/{city}?format=j1")
    data = r.json()
    return data

city_name = input("Enter a city name:")
data = get_weather(city_name)
temp = data["weather"][1]["avgtempF"]
tomrrow_date = data["weather"][1]["date"]
uv_index = data["weather"][1]["uvIndex"]

weather = f"""On {tomrrow_date}, 
        the weather of {city_name} is predicted to be: {temp} F 
        and the uv index is {uv_index}"""

prompt = f"Do I need a jacket and sunscreen in {city_name} tomorrow? More info: {weather}"

data = {
    "model": "gpt-oss:20b",
    "prompt": prompt,
    "stream": False
}

res = requests.post(ollama_url, json=data)
llm_response = res.json()["response"]

print(llm_response)