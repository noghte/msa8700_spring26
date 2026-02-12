sample_data = {
    "colors": ["red", "yellow"],
    "comments": [
        {"commentType": "Description"},
        {
            "commentType": "FUNCTION",
            "texts": [
                {"value": "text 1"}, 
                {"value": "text 2"}],
        },
        {"commentType": "FUNCTION"},
    ],
}


def extract_protein_function(data):
    for c in data.get("comments", []):
        if c.get("commentType") == "FUNCTION":
            return "\n".join(t["value"] for t in c.get("texts", []))

results = extract_protein_function(sample_data)
print(results)