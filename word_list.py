from collections import defaultdict

import spacy
import wordfreq as wf
from beartype import beartype as typed
from tqdm import tqdm  # type: ignore

nlp = spacy.load("de_core_news_md")

result_freq: dict[str, float] = defaultdict(float)
result_lemmas = defaultdict(list)

for word in tqdm(wf.top_n_list("de", 10**6, wordlist="large")):
    if len(word) < 2 or any(c.isdigit() for c in word):
        continue
    doc = nlp(word)
    if len(doc) != 1:
        continue
    lemma = doc[0].lemma_
    result_freq[word] += wf.word_frequency(word, "de", wordlist="large")
    result_lemmas[lemma].append(word)

with open("words_de.txt", "w", encoding="utf-8") as f:
    for word, freq in sorted(result_freq.items(), key=lambda x: x[1], reverse=True):
        f.write(f"{word}\t{freq}\n")

for lemma, words in result_lemmas.items():
    matches = any(lemma.lower() == w.lower() for w in words)
    if not matches:
        print(lemma, words)
