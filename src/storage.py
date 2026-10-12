import json
from pathlib import Path

file_name = "tasks.txt"

def save(task):
    tasks = []    
    path = Path.home() / ".config/TooDoo"
    path.mkdir(parents=False, exist_ok=True)
    path = path / file_name

    if path.exists():
        task_list = load()
        
        for task_element in task_list:
            tasks.append(task_element)

    if type(task) == dict:
        with path.open("w", encoding="utf-8") as file:
            tasks.append(task)
            tasks = json.dumps(tasks)
            file.write(tasks)
    else:
        with path.open("w", encoding="utf-8") as file:
            tasks = json.dumps(task)
            file.write(tasks)

def load(what_you_want="task"):
    path = Path.home() / ".config/TooDoo/" / file_name

    if path.exists():
        with open(path) as file:
            task_list = json.loads(file.read())

        if what_you_want == "task":
            return task_list

        elif what_you_want == "len":
            return len(task_list)

    elif not task_list:
        print("No task is here!!!")
        
        return None

    print("No task added!!!")

    return None