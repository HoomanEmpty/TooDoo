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

def backup(command):
    if command == "-b":
        path = Path.home() / ".config/TooDoo/tasks.txt"
        save_path = Path.home() / "TooDoo.backup.Jaraare"
        shutil.copy2(path, save_path)
        print(f"Backup is saved in {save_path / "TooDoo.backup.Jaraare"}")
        return

    while True:
        save_path = input("Where you want save your backup: ")
        if not save_path:
            save_path = Path.home()

        elif save_path[0] == "~":
            save_path = save_path.replace("~", str(Path.home()), 1)
            save_path = Path(save_path)

        elif save_path == "0":
            return
        
        else:
            save_path = Path(save_path)

        path = Path.home() / ".config/TooDoo/tasks.txt"
        if save_path.exists():
            shutil.copy2(path, save_path / "TooDoo.backup.Jaraare")

            print(f"Backup is saved in {save_path / "TooDoo.backup.Jaraare"}")
            return

        else:
            print("Path doesn't exist!!!")

def imp(command):
    if command == "-i":
        save_path = Path.home() / "TooDoo.backup.Jaraare"
        shutil.move(save_path, Path.home() / ".config/TooDoo/tasks.txt")
        print("Import succsed!!")
        return
    
    while True:
        save_path = input("Where your backup are saved: ")
        if not save_path:
            save_path = Path.home()

        elif save_path[0] == "~":
            save_path = save_path.replace("~", str(Path.home()), 1)
            save_path = Path(save_path)

        elif save_path == "0":
            return

        else:
            save_path = Path(save_path)

        save_path = save_path / "TooDoo.backup.Jaraare"
        if save_path.exists():
            shutil.move(save_path, Path.home() / ".config/TooDoo/tasks.txt")

            print("Import succsed!!")
            return

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