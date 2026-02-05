import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from pydantic import BaseModel, Field
import requests
import json

url = "http://10.230.100.240:17020/api/generate"

def ask_llm(country):
    data = {
        "model" : "gpt-oss:20b",
        "prompt": f"For the country `{country}`, provide:"\
            "1. The capital city"\
            "2. The continent it belongs"\
            "Respond ONLY with valid JSON and do not provide explanations. Response format:"\
            "{{'capital':'capital_name', 'continent':'continent_name'}}",
        "stream": False
    }
    response = requests.post(url, json=data)
    return response.json()["response"]

class CountryInfo(BaseModel):
    capital:str = Field("the capital name")
    continent:str = Field("the continent name")

def get_countries_from_wikipedia():
    header = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36"
    }
    url = "https://en.wikipedia.org/wiki/List_of_sovereign_states"
    r = requests.get(url, headers=header)

    # Creating a data structure that can parse HTML 
    soup = BeautifulSoup(r.text, "html.parser")
    countries = []
    for table in soup.select("table.wikitable"):
        for link in table.select("td b a"):
            country = link.get_text().strip()
            countries.append(country)
    countries = list(set(countries)) # to remove the duplicates
    return countries

if __name__ == "__main__":
    df = None
    if not os.path.exists("countries.csv"):
        print("Creating countries.csv")
        countries = get_countries_from_wikipedia()
        df = pd.DataFrame(countries, columns=["Country"])
        df.to_csv("countries.csv", index=None)
    else:
        df = pd.read_csv("countries.csv")

    df = df.sort_values(by="Country")
    df = df[:5]
    for idx, row in df.iterrows():
        # if df[idx]["Capital"] and df[idx]["Capital"] != "Error":
        try:
            info = ask_llm(row["Country"])
            parsed_json = json.loads(info)
            result = CountryInfo(**parsed_json)
            df.at[idx, 'Capital'] = result.capital
            df.at[idx, 'Continent'] = result.continent
        except Exception as e:
            df.at[idx, 'Capital'] = "Error"
            df.at[idx, 'Continent'] = "Error"
    
    df.to_csv("countries_enriched.csv")
# Enrich our dataset to get the capital and the continent of each country