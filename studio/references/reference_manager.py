"""Simple reference management for cinematic and historical assets."""


from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Reference:
    name: str
    category: str  # e.g. "historical", "film-still", "concept-art"
    path: str
    notes: str = ""


class ReferenceManager:
    """Lightweight manager for tracking visual references."""

    def __init__(self):
        self._references: Dict[str, Reference] = {}

    def add(self, ref: Reference) -> None:
        self._references[ref.name] = ref

    def get(self, name: str) -> Reference | None:
        return self._references.get(name)

    def list_by_category(self, category: str) -> List[Reference]:
        return [r for r in self._references.values() if r.category == category]

    def search(self, keyword: str) -> List[Reference]:
        keyword = keyword.lower()
        return [
            r for r in self._references.values()
            if keyword in r.name.lower() or keyword in r.notes.lower()
        ]


if __name__ == "__main__":
    manager = ReferenceManager()
    manager.add(Reference("Wes Anderson symmetry example", "film-still", "assets/references/wes_symmetry.jpg", "Perfect planimetric shot"))
    print(manager.list_by_category("film-still"))
