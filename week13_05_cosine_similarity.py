#  pip install transformers
from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def cosine_sim(a, b):
    return torch.nn.functional.cosine_similarity(a, b).item()

candidate = "The quick brown fox jumps over the lazy dog"
reference = "A red fox quickly jumps over a fast dog"
candidate_emb = get_embedding(candidate)
reference_emb = get_embedding(reference)

similarity = cosine_sim(candidate_emb, reference_emb)
print(f"Similarity: {similarity:.4f}")