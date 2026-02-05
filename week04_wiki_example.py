import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

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
    if not os.path.exists("countries.csv"):
        print("Creating countries.csv")
        countries = get_countries_from_wikipedia()
        df = pd.DataFrame(countries, columns=["Country"])
        df.to_csv("countries.csv", index=None)
    else:
        df_countries = pd.read_csv("countries.csv")
        df_sorted = df_countries.sort_values(by="Country")
        countries = df_sorted["Country"].to_list()
        print(countries)