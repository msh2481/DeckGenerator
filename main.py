import json

import duden

while True:
    text = input("Enter word: ")
    w = duden.search(text)
    print(w)
    for e in w:
        print(e.meaning_overview)
