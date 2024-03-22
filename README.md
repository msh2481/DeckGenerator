# DeckGenerator
AI-powered generator of Anki decks for language learning.

## Card format
It's very simple. Each word X will spawn two cards.

First one:
```
German sentences with X and their audio
========================================
English translations and their audio
```

And the reverse:
```
English translations and their audio
========================================
German sentences with X and their audio
```

No definitions, grammar information or other extras. The idea is that you can easily learn all the useful information from these diverse usage examples, without having to memorise declension tables and other boring material.

## Installation and usage
Install poetry and do `poetry update`.
Additionally, install German module for spaCy:
```bash
python -m spacy download de_core_news_md
```