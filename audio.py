import json
import os
import time

import openai  # type: ignore

from beartype import beartype as typed
from tqdm import tqdm  # type: ignore
from utils import h

client = openai.Client()


@typed
def pronounce(text_prompt: str, filename: str) -> None:
    while True:
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice="echo",
                input=text_prompt,
            )
            response.write_to_file(filename)
            return
        except Exception as e:
            print(e)
            time.sleep(1)


if __name__ == "__main__":
    if not os.path.exists("audio"):
        os.mkdir("audio")
    with open("results.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    pairs: list[tuple[str, str]] = []
    for _, result in results.items():
        k = len(result["English"])
        for i in range(k):
            pairs.append((result["German"][i], result["English"][i]))
    print("Sentences loaded")

    existing = set([f[:-4] for f in os.listdir("audio")])

    with open("audio/table.txt", "a", encoding="utf-8") as f:

        def process(text: str):
            hash_value = h(text)
            if hash_value in existing:
                print(f"Skipping {hash_value}")
                return
            print(hash_value, text, file=f, flush=True)
            pronounce(text, f"audio/{hash_value}.mp3")

        for pair in tqdm(pairs):
            process(pair[0])
            process(pair[1])
