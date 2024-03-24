import argparse
import json
import os

from beartype import beartype as typed
from genanki import Deck, Model, Note, Package  # type: ignore
from tqdm import tqdm  # type: ignore
from utils import h

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_pairs", type=int, required=True)
    args = parser.parse_args()

    model = Model(
        1024032024,
        "Sentence pair",
        fields=[
            {"name": "sentence"},
            {"name": "translation"},
            {"name": "sentence_audio"},
            {"name": "translation_audio"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{sentence}} {{sentence_audio}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{translation}} {{translation_audio}}',
            },
            {
                "name": "Card 2",
                "qfmt": "{{translation}} {{translation_audio}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{sentence}} {{sentence_audio}}',
            },
        ],
    )

    with open("results.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    pairs: list[tuple[str, str]] = []
    for _, result in results.items():
        k = len(result["English"])
        for i in range(k):
            pairs.append((result["German"][i], result["English"][i]))
    pairs = pairs[: args.n_pairs]

    deck = Deck(1124032024, "English_German")

    media_files = set()

    existing = set([f for f in os.listdir("audio")])
    counter = 0
    for pair in tqdm(pairs):
        has_audio = True
        for filename in [h(pair[0]) + ".mp3", h(pair[1]) + ".mp3"]:
            if filename in existing:
                media_files.add("audio/" + filename)
            else:
                has_audio = False
        if not has_audio:
            continue
        counter += 1
        note = Note(
            model=model,
            fields=[
                pair[0],
                pair[1],
                f"[sound:{h(pair[0])}.mp3]",
                f"[sound:{h(pair[1])}.mp3]",
            ],
        )
        deck.add_note(note)

    print(f"Added {counter} pairs")
    package = Package(deck)
    package.media_files = list(media_files)
    package.write_to_file("English_German.apkg")
