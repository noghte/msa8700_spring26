from transformers import BertTokenizer, BertModel
import torch
import numpy as np

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def cosine_sim(a, b):
    return torch.nn.functional.cosine_similarity(a, b).item()

career = ["executive", "manager", "physician", "athlete"]

# Two groups we want to compare against
male = ["Scott", "John", "Steve"]
female = ["Amy", "Mary", "Susan"]

# Get embeddings
career_vecs = [get_embedding(w) for w in career]
male_vecs = [get_embedding(w) for w in male]
female_vecs = [get_embedding(w) for w in female]

# Compute the bias score

scores = []
for career_vec in career_vecs:
    male_sim = np.mean([cosine_sim(career_vec, m) for m in male_vecs])
    female_sim = np.mean([cosine_sim(career_vec, f) for f in female_vecs])

    # Bias score
    # Positive -> Closer to male names
    # Negative -> Closer to female names
    score = male_sim - female_sim
    scores.append(score)

print(scores)
print("=====\n")
print("Average association:", np.mean(scores))