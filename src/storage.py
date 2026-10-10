import json
from pathlib import Path

def save(task):
    task = json.dumps(task)
    path = Path.home() / ".config/TooDoo"
    path.mkdir(parents=False, exist_ok=True)
    path = path / "tasks.md"
    with path.open("a", encoding="utf-8") as file:
        file.write(task)

def load():
    ...