# %%
import matplotlib.pyplot as plt
import numpy as np
import openai
import wordfreq as wf
from beartype import beartype as typed
from tqdm import tqdm  # type: ignore

client = None  # openai.Client()


@typed
def ask(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        # response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


@typed
def german_prompt(word: str) -> str:
    few_shot = """
Task:
- Create example of German sentences containing the given word and their English translations.
- If the word has several unrelated meanings or can be of different parts of speech, make sure to show all of them.
- For each meaning provide 2-3 sentences.
- Very important: use the word in many different ways, e.g. different tenses, cases, declensions and so on. The goal is to show in general how to use this word in various grammatical contexts.

Example for "sein":
{
   "German": [
      "Das könnte dein bester Freund sein.",
      "Du könntest arbeitslos gewesen sein.",
      "Sie wird nächstes Jahr wahrscheinlich in London sein.",
      "Sie müssen in der Biblothek gewesen sein.",
      "Wir sind immer noch beste Freunde.",
      "Sie sind überall gewesen.",
      "Es könnte schön sein, eine Weile einfach nichts zu tun.",
      "Es war einmal ein kleines Mädchen.",
      "Wird es dein erstes Mal in Amerika sein?"
   ],
   "English": [
      "That could be your best friend.",
      "You could have been unemployed.",
      "She will probably be in London next year.",
      "You must have been in the library.",
      "We are still best friends.",
      "They have been everywhere.",
      "It could be nice to simply do nothing for a while.",
      "Once upon a time, there was a little girl.",
      "Will it be your first time in America?"
   ]
}

Example for "machen":
{
   "German": [
      "Was machst du gerade?",
      "Er hat das alles alleine gemacht.",
      "Sie werden morgen ihre Hausaufgaben machen.",
      "Sie mussen das Essen gemacht haben.",
      "Wir machen schon immer Sport zusammen.",
      "Sie hat gestern nichts Besonderes gemacht.",
      "Es könnte hilfreich sein, eine Pause zu machen.",
      "Es war das Beste, was ich je gemacht habe.",
      "Wird sie das heute Abend machen?"
   ],
   "English": [
      "What are you doing right now?",
      "He did all of this on his own.",
      "They will do their homework tomorrow.",
      "You must have prepared the food.",
      "We have always played sports together.",
      "She did not do anything special yesterday.",
      "It could be helpful to take a break.",
      "It was the best thing I've ever done.",
      "Will she do it tonight?"
   ]
}

Example for "abheben":
{
   "German": [
      "Ich muss Geld von meinem Bankkonto abheben.",
      "Kannst du bitte 200 Euro vom Automaten abheben?",
      "Der Pilot hat das Flugzeug gerade abgehoben.",
      "Die Rakete hebt gleich ab.",
      "Mit seinem innovativen Design hebt sich das Produkt deutlich von der Konkurrenz ab.",
      "Ihr einzigartiger Stil hebt sie in der Modeszene ab."
   ],
   "English": [
      "I need to withdraw money from my bank account.",
      "Can you please withdraw 200 Euros from the ATM?",
      "The pilot just took off the airplane.",
      "The rocket is about to take off.",
      "With its innovative design, the product clearly stands out from the competition.",
      "Her unique style sets her apart in the fashion scene."
   ]
}""".strip()
    return f'{few_shot}\nYou need to create sentences for the word "{word}".'


# %%
total = np.float64(0)
ylist = []
for word in tqdm(wf.top_n_list("de", 10**6, wordlist="large")):
    if len(duden.search(word)):
        frequency = wf.word_frequency(word, "de", wordlist="large")
        total += frequency
        ylist.append(total)
y = np.array(ylist) / total
y = 1 - y
x = np.arange(1, len(y) + 1)

# %%
plt.figure(figsize=(10, 10), dpi=200)
plt.loglog(x, y, "k", lw=1)
plt.grid("minor")
plt.xlabel("Vocabulary size")

# %%
words = [word for word in wf.top_n_list("de", 10**5, wordlist="large")]


# %%
duden.search("")
# %%

# %%
