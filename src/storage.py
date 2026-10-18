import json
from pathlib import Path
import shutil

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

def backup():
    path = Path.home() / ".config/TooDoo"
    path.mkdir(parents=False, exist_ok=True)
    path = path / file_name

    if path.exists():
        shutil.copy2(path, Path.home() / "TooDoo.backup.Jaraare")

    else:
        print("Files doesn't exist!!!")

def imp():
    path = Path.home() / "TooDoo.backup.Jaraare"
    if path.exists():
        shutil.move(path, Path.home() / ".config/TooDoo/tasks.txt")

    else:
        print("File doesn't exist!!!")

def load(what_you_want="task"):
    path = Path.home() / ".config/TooDoo/" / file_name

    if path.exists():
        with open(path) as file:
            task_list = json.loads(file.read())

        match what_you_want:
            case "task":
                return task_list

            case "len":
                return len(task_list)

            case "title":
                task_title_list = [task["title"] for task in task_list]

                return task_title_list

    elif not task_list:
        print("No task is here!!!")
        
        return None

    print("No task added!!!")

    return None