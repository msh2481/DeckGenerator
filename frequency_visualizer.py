import matplotlib.pyplot as plt
import numpy as np

with open("words_de.txt", "r", encoding="utf-8") as f:
    y = []
    total = 0.0
    for line in f:
        word, freq = line.strip().split("\t")
        total += float(freq)
        y.append(total)
arr = np.array(y, dtype=np.float32)
arr = arr / total
arr = 1 - arr

plt.figure(figsize=(10, 10), dpi=100)
plt.plot(arr, "k", lw=1)
plt.xscale("log")
plt.grid(True)
plt.xlabel("Vocabulary size")
plt.ylabel("Frequency of unknown words")
plt.tight_layout()
plt.savefig("german_frequencies.svg")
