import requests
import pandas as pd

def extract_protein_function(data):
    for c in data.get("comments", []):
        if c.get("commentType") == "FUNCTION":
            return "\n".join(t["value"] for t in c.get("texts", []))

    return "N/A"

df = pd.read_csv("kinase_classification.csv")
uniprot_ids = df["uniprot"].dropna().unique()[:40]
print(uniprot_ids)

functions = []
names = []

for uniprot_id in uniprot_ids:
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    r = requests.get(url)
    data = r.json()
    protein_name = data['proteinDescription']['recommendedName']['fullName']['value']
    names.append(protein_name)
    protein_function = extract_protein_function(data)
    functions.append(protein_function)

df_output = pd.DataFrame({"uniprot": uniprot_ids, "name": names, "functions": functions})
df_output.to_csv("kinases.csv", index=False)