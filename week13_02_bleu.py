from nltk.translate.bleu_score import sentence_bleu
from nltk import word_tokenize

reference = "The cat sat on the mat"
candidate = "The cat on the mat"

ref_tokens = word_tokenize(reference)
cand_tokens = word_tokenize(candidate)

#weights: 1-gram, 2-gram, 3-gram, 4-gram
bleu = sentence_bleu([ref_tokens], cand_tokens, weights=(1,1,0,0)) 
print(f"BLEU score: {bleu:.4f}")

