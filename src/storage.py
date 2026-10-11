import json
from pathlib import Path

def save(task):
    tasks = []
    path = Path.home() / ".config/TooDoo"
    path.mkdir(parents=False, exist_ok=True)
    path = path / "tasks.md"

    if path.exists():
        task_list = load()

        for task_element in task_list:
            tasks.append(task_element)

    with path.open("w", encoding="utf-8") as file:
        tasks.append(task)
        tasks = json.dumps(tasks)
        file.write(tasks)

def load():
    path = Path.home() / ".config/TooDoo/tasks.md"

    if path.exists():
        with open(path) as file:
            task_list = json.loads(file.read())

        return task_list

    elif not task_list:
        print("No task is here!!!")
        
        return None

    print("No task added!!!")

    return None