# pip install bert-score
from bert_score import score
candidate = ["The quick brown fox jumps over the lazy dog"]
reference = ["A red fox quickly jumps over a fast dog"]
P, R, F1 = score(candidate, reference, lang="en")
print(P, R, F1)
#tensor([0.9471]) tensor([0.9508]) tensor([0.9489])