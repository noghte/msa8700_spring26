#pip install rouge-score
from rouge_score import rouge_scorer

# Stemming example: running -> run
scorer = rouge_scorer.RougeScorer(['rouge1','rouge2'], use_stemmer=True)

reference = "The cat sat on the mat"
candidate = "The cat on the mat"

scores = scorer.score(reference, candidate)
print(scores)
