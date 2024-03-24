from hashlib import sha256

from beartype import beartype as typed


@typed
def h(text_prompt: str) -> str:
    return sha256(bytes(text_prompt.strip(), encoding="utf-8")).hexdigest()
