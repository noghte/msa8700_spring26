import requests
import pandas as pd

def extract_protein_function(data):
    for c in data.get("comments", []):
        if c.get("commentType") == "FUNCTION":
            return "\n".join(t["value"] for t in c.get("texts", []))

    return "N/A"

df = pd.read_csv("kinase_classification.csv")
uniprot_ids = df["uniprot"].dropna().unique()[:100]

functions = []
names = []
index = 0
for uniprot_id in uniprot_ids:
    index +=1
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    r = requests.get(url)
    data = r.json()
    if data["entryType"] == "Inactive":
        protein_name = "N/A"
        protein_function = "N/A"
    else:
        protein_name = data['proteinDescription']['recommendedName']['fullName']['value']
        protein_function = extract_protein_function(data)
    
    names.append(protein_name)
    functions.append(protein_function)
    print(f"Index: {index}, Uniprot: {uniprot_id}")

df_output = pd.DataFrame({"uniprot": uniprot_ids, "name": names, "functions": functions})
df_output.to_csv("kinases.csv", index=False)