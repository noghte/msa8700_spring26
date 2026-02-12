import requests

url = "https://rest.uniprot.org/uniprotkb/P00533.json"
r = requests.get(url)

def extract_protein_function(data):
    for c in data.get("comments", []):
        if c.get("commentType") == "FUNCTION":
            return "\n".join(t["value"] for t in c.get("texts", []))

    return "N/A"


if r.status_code == 200: # if the request was successful
    data = r.json()
    print(extract_protein_function(data))
    #data['comments'][0]['texts'][0]['value']
