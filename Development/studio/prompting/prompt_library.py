"""Centralized prompt templates and helpers for cinematic work."""


from typing import Dict


class PromptLibrary:
    """Simple library for storing and retrieving reusable prompt patterns."""

    def __init__(self):
        self._prompts: Dict[str, str] = {}

    def register(self, name: str, prompt: str) -> None:
        self._prompts[name] = prompt

    def get(self, name: str) -> str:
        return self._prompts.get(name, "")

    def list_available(self) -> list[str]:
        return list(self._prompts.keys())


# Example usage / starter library
if __name__ == "__main__":
    library = PromptLibrary()
    library.register("wes_anderson_wide", "Planimetric symmetrical composition...")
    print(library.list_available())
